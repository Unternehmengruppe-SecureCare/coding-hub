"""Kopplung des Grok/Cursor-Plugins coding-hub prüfen.

Die Tests sind offline und brauchen keine Extra-Pakete. Ein optionaler
Live-Abgleich gegen das Hub-ZIP läuft nur, wenn der Tunnel erreichbar ist.
"""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG = "Unternehmengruppe-SecureCare"
PLUGIN_NAME = "coding-hub"
HUB_ZIP_URL = os.environ.get(
    "HUB_PLUGIN_ZIP_URL",
    "https://administrators-revised-finance-interracial.trycloudflare.com/api/grok-plugin/zip",
)

REQUIRED_FILES = (
    "plugin.json",
    ".cursor-plugin/plugin.json",
    ".grok-plugin/plugin.json",
    ".grok/config.toml",
    ".grok/skills/cursor-dispatch/SKILL.md",
    "skills/cursor-dispatch/SKILL.md",
    "agents/cursor-dispatch.md",
    ".mcp.json",
    "mcp.json",
    "orchestrate/grok-bot/BOT.md",
    "orchestrate/grok-bot/ROUTINES.md",
    "orchestrate/grok-bot/ADD_MCP.md",
    "README.md",
    ".github/workflows/cursor-dispatch.yml",
    ".github/ISSUE_TEMPLATE/cursor-task.yml",
    ".github/cursor-dispatch/SYSTEM.md",
    ".github/cursor-dispatch/AGENTS.md",
)

HUB_ZIP_FILES = (
    "plugin.json",
    ".grok-plugin/plugin.json",
    ".grok/config.toml",
    ".grok/skills/cursor-dispatch/SKILL.md",
    "skills/cursor-dispatch/SKILL.md",
    "agents/cursor-dispatch.md",
    ".mcp.json",
    "mcp.json",
    ".github/workflows/gitleaks.yml",
    ".github/workflows/cursor-dispatch.yml",
    ".github/ISSUE_TEMPLATE/cursor-task.yml",
    ".github/cursor-dispatch/SYSTEM.md",
    ".github/cursor-dispatch/AGENTS.md",
    "orchestrate/grok-bot/BOT.md",
    "orchestrate/grok-bot/ROUTINES.md",
    "orchestrate/grok-bot/ADD_MCP.md",
    "README.md",
)


def _read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8")


def _json(rel: str) -> dict:
    return json.loads(_read(rel))


def _mcp_url(config: dict) -> str:
    server = (config.get("mcpServers") or {}).get("coding-hub") or {}
    return str(server.get("url") or "")


class PluginCouplingTests(unittest.TestCase):
    def test_required_plugin_files_exist(self) -> None:
        missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).is_file()]
        self.assertEqual(missing, [], f"fehlende Plugin-Dateien: {missing}")

    def test_plugin_json_identifies_coding_hub(self) -> None:
        manifest = _json("plugin.json")
        self.assertEqual(manifest["name"], PLUGIN_NAME)
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertIn("description", manifest)
        self.assertEqual(
            manifest.get("$schema"),
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )
        self.assertIn("cursor", manifest.get("keywords") or [])
        variables = (manifest.get("variables") or {}).get("properties") or {}
        self.assertIn("HUB_PUBLIC_URL", variables)
        self.assertEqual(
            (variables.get("GITHUB_ORG") or {}).get("default"),
            ORG,
        )

    def test_cursor_plugin_manifest_mirrors_plugin(self) -> None:
        cursor = _json(".cursor-plugin/plugin.json")
        root = _json("plugin.json")
        self.assertEqual(cursor["name"], root["name"])
        self.assertEqual(cursor["version"], root["version"])
        self.assertEqual(cursor["description"], root["description"])
        self.assertEqual(cursor["author"]["name"], ORG)
        self.assertEqual(cursor["skills"], "./skills/")
        self.assertEqual(cursor["agents"], "./agents/")
        self.assertEqual(cursor["mcpServers"], "./mcp.json")
        self.assertTrue((ROOT / "skills").is_dir())
        self.assertTrue((ROOT / "agents").is_dir())
        self.assertTrue((ROOT / "mcp.json").is_file())

    def test_grok_plugin_mirror_matches_name(self) -> None:
        grok = _json(".grok-plugin/plugin.json")
        self.assertEqual(grok["name"], PLUGIN_NAME)
        self.assertEqual(grok["version"], "0.1.0")
        self.assertIn("plugin.json", grok.get("description") or "")
        self.assertIn(".cursor-plugin/plugin.json", grok.get("description") or "")

    def test_mcp_configs_use_https_mcp_path(self) -> None:
        for rel in (".mcp.json", "mcp.json"):
            with self.subTest(rel=rel):
                config = _json(rel)
                servers = config.get("mcpServers") or {}
                self.assertIn("coding-hub", servers)
                url = _mcp_url(config)
                self.assertTrue(url.startswith("https://"), url)
                self.assertTrue(url.endswith("/mcp"), url)
                self.assertNotIn("localhost", url)
        grok_mcp = _json(".mcp.json")
        agent_mcp = _json("mcp.json")
        self.assertEqual(_mcp_url(grok_mcp), _mcp_url(agent_mcp))
        self.assertEqual(
            agent_mcp.get("$schema"),
            "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        )

    def test_grok_config_points_at_same_mcp(self) -> None:
        text = _read(".grok/config.toml")
        mcp_url = _mcp_url(_json(".mcp.json"))
        self.assertIn("[mcp_servers.coding-hub]", text)
        self.assertIn(mcp_url, text)
        self.assertIn("startup_timeout_sec", text)

    def test_skill_copies_are_identical_and_forbid_local_coding(self) -> None:
        grok_skill = _read(".grok/skills/cursor-dispatch/SKILL.md")
        portable_skill = _read("skills/cursor-dispatch/SKILL.md")
        self.assertEqual(grok_skill, portable_skill)
        self.assertIn("name: cursor-dispatch", portable_skill)
        self.assertIn("Claude Code nicht", portable_skill)
        self.assertIn("Keinen Anwendungscode schreiben", portable_skill)
        self.assertIn("run_outer_loop_tick", portable_skill)
        self.assertIn(ORG, portable_skill)
        self.assertIn("GitHub ist die Source of Truth", portable_skill)
        self.assertIn("build_cursor_mention", portable_skill)

    def test_agent_and_bot_prompt_stay_on_outer_loop(self) -> None:
        agent = _read("agents/cursor-dispatch.md")
        bot = _read("orchestrate/grok-bot/BOT.md")
        for text, label in ((agent, "agent"), (bot, "bot")):
            with self.subTest(label=label):
                self.assertIn("Claude Code", text)
                self.assertIn("keinen Anwendungscode", text.lower())
                self.assertIn(ORG, text)
                self.assertIn("@cursor", text)
        self.assertIn("name: cursor-dispatch", agent)
        self.assertIn("Cursor Dispatch", bot)
        self.assertIn("autoCreatePR", bot)
        self.assertIn("get_coupling_status", bot)

    def test_grok_bot_routines_and_mcp_docs_exist(self) -> None:
        routines = _read("orchestrate/grok-bot/ROUTINES.md")
        add_mcp = _read("orchestrate/grok-bot/ADD_MCP.md")
        self.assertIn("run_outer_loop_tick", routines)
        self.assertIn("Org pollen", routines)
        self.assertIn("/mcp", add_mcp)
        self.assertIn("coding-hub://handoff", add_mcp)
        mcp_url = _mcp_url(_json(".mcp.json"))
        self.assertIn(mcp_url, add_mcp)

    def test_inner_loop_workflow_mentions_cursor_without_merge(self) -> None:
        workflow = _read(".github/workflows/cursor-dispatch.yml")
        self.assertIn("@cursor", workflow)
        self.assertIn("autoCreatePR", workflow)
        self.assertIn("Kein Commit auf die Default-Branch", workflow)
        self.assertIn("Kein Claude Code", workflow)
        self.assertNotIn("gh pr merge", workflow)

    def test_repo_has_no_application_source_tree(self) -> None:
        forbidden_roots = ("src", "app", "lib", "backend", "frontend")
        present = [name for name in forbidden_roots if (ROOT / name).exists()]
        self.assertEqual(present, [], f"unerwarteter Anwendungscode: {present}")


class HubZipCouplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.zip_bytes: bytes | None = None
        cls.skip_reason: str | None = None
        if os.environ.get("SKIP_HUB_ZIP") == "1":
            cls.skip_reason = "SKIP_HUB_ZIP=1"
            return
        try:
            request = urllib.request.Request(
                HUB_ZIP_URL,
                headers={"User-Agent": "coding-hub-plugin-tests"},
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                cls.zip_bytes = response.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            cls.skip_reason = f"Hub-ZIP nicht erreichbar: {exc}"

    def test_hub_zip_contains_required_plugin_files(self) -> None:
        if self.skip_reason:
            self.skipTest(self.skip_reason)
        assert self.zip_bytes is not None
        with zipfile.ZipFile(BytesIO(self.zip_bytes)) as archive:
            names = set(archive.namelist())
        missing = [rel for rel in HUB_ZIP_FILES if rel not in names]
        self.assertEqual(missing, [], f"Hub-ZIP ohne Dateien: {missing}")

    def test_checked_in_hub_files_match_zip(self) -> None:
        if self.skip_reason:
            self.skipTest(self.skip_reason)
        assert self.zip_bytes is not None
        with zipfile.ZipFile(BytesIO(self.zip_bytes)) as archive:
            for rel in HUB_ZIP_FILES:
                with self.subTest(rel=rel):
                    expected = archive.read(rel)
                    actual = (ROOT / rel).read_bytes()
                    self.assertEqual(
                        actual,
                        expected,
                        f"{rel} weicht vom Hub-ZIP ab",
                    )


if __name__ == "__main__":
    unittest.main()
