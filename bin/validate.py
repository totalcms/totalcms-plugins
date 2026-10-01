#!/usr/bin/env python3
"""Check the plugin package against OpenAI's submission requirements.

Limits come from https://developers.openai.com/plugins/deploy/submission
(manifest field reference). Exits non-zero on any failure.
"""
import json
import re
import sys
from pathlib import Path

pkg = Path(sys.argv[1] if len(sys.argv) > 1 else "package")
errors: list[str] = []


def check(ok: bool, message: str) -> None:
	if not ok:
		errors.append(message)


manifest = json.loads((pkg / ".codex-plugin/plugin.json").read_text())
mcp = json.loads((pkg / ".mcp.json").read_text())
ui = manifest.get("interface", {})
openai = manifest.get("extensions", {}).get("com.openai", {})

# Package identity
check(bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", manifest.get("name", ""))) and len(manifest["name"]) <= 64, "name: lowercase letters, numbers and single hyphens, at most 64 chars")
check(bool(re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", ""))), "version: semantic version required")
check(0 < len(manifest.get("description", "")) <= 4000, "description: required, at most 4000 chars")
check(bool(manifest.get("author", {}).get("name")), "author.name: required")

# Listing
for field, limit in {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}.items():
	value = ui.get(field, "")
	check(0 < len(value) <= limit, f"interface.{field}: required, at most {limit} chars (is {len(value)})")
check(bool(ui.get("category")), "interface.category: required")
for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
	check(str(ui.get(field, "")).startswith("https://"), f"interface.{field}: HTTPS URL required for MCP review")
prompts = ui.get("defaultPrompt", [])
check(len(prompts) <= 3 and all(len(p) <= 128 for p in prompts), "interface.defaultPrompt: up to 3 prompts, 128 chars each")
check(isinstance(ui.get("capabilities"), list) and len(ui["capabilities"]) <= 20 and all(len(c) <= 120 for c in ui["capabilities"]), "interface.capabilities: at most 20, 120 chars each")
for field in ("logo", "composerIcon"):
	check(bool(ui.get(field)) and (pkg / ui[field]).is_file(), f"interface.{field}: file missing")

# MCP server — plugin-level test cases need exactly one
check(len(mcp.get("mcpServers", {})) == 1, ".mcp.json: exactly one MCP server")

# Review cases
cases = openai.get("review", {}).get("test_cases", {})
positive, negative = cases.get("positive", []), cases.get("negative", [])
check(len(positive) == 5, f"review: exactly 5 positive cases (has {len(positive)})")
check(len(negative) == 3, f"review: exactly 3 negative cases (has {len(negative)})")
for n, case in enumerate(positive, 1):
	for field in ("description", "prompt", "tools_triggered", "expected_behavior"):
		check(bool(case.get(field)), f"positive case {n}: {field} required")
for n, case in enumerate(negative, 1):
	for field in ("description", "prompt"):
		check(bool(case.get(field)), f"negative case {n}: {field} required")
check(str(openai.get("review", {}).get("demo_recording_url", "")).startswith("https://"), "review.demo_recording_url: required for MCP review, and must be in the ZIP")
check("test_credentials" not in openai.get("review", {}) and "reviewer_instructions" not in openai.get("review", {}), "review: credentials belong in the dashboard, not the ZIP")

# Skills need name + description frontmatter
for skill in sorted((pkg / "skills").glob("*/SKILL.md")):
	head = skill.read_text().split("---")
	front = head[1] if len(head) > 2 else ""
	check(re.search(r"^name:\s*\S", front, re.M) is not None and re.search(r"^description:\s*\S", front, re.M) is not None, f"{skill.relative_to(pkg)}: name and description frontmatter required")

# Claude directory — https://claude.com/docs/plugins/pre-submission-checklist
claude_path = pkg / ".claude-plugin/plugin.json"
check(claude_path.is_file(), ".claude-plugin/plugin.json: required for the Claude directory")
if claude_path.is_file():
	claude = json.loads(claude_path.read_text())
	check(claude.get("name") == manifest.get("name"), ".claude-plugin name must match .codex-plugin name")
	check(bool(re.fullmatch(r"[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?", claude.get("name", ""))), ".claude-plugin name: lowercase letters, digits and hyphens, at most 64 chars")
	for field in ("version", "description", "license"):
		check(bool(claude.get(field)), f".claude-plugin {field}: set it (license is required for listing)")
	check(bool(claude.get("author", {}).get("name")), ".claude-plugin author.name: set it")
	check(str(claude.get("privacyPolicyUrl", "")).startswith("https://"), ".claude-plugin privacyPolicyUrl: the directory requires an HTTPS privacy policy URL")
readme = pkg / "README.md"
words = len(re.sub(r"```.*?```", "", readme.read_text(), flags=re.S).split()) if readme.is_file() else 0
check(words >= 40, f"README.md: Claude shows it as the listing and needs 40+ words outside code blocks (has {words})")
check(readme.is_file() and re.search(r"^#+\s*Privacy Policy\s*$", readme.read_text(), re.M | re.I) is not None and "https://totalcms.co/privacy" in readme.read_text(), "README.md: needs a 'Privacy Policy' section linking https://totalcms.co/privacy")
check((pkg / "LICENSE").is_file(), "LICENSE: required in the plugin folder for the Claude directory")
check(not (pkg / "bin").exists(), "bin/: claude.ai and Cowork won't install a plugin with a top-level bin/ folder")
for name, server in mcp.get("mcpServers", {}).items():
	check(server.get("type") in ("http", "sse", "ws"), f".mcp.json {name}: Claude needs type http, sse or ws")
	check(str(server.get("url", "")).startswith("https://"), f".mcp.json {name}: url must be https://")
junk = [p.relative_to(pkg) for p in pkg.rglob("*") if p.name in (".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX")]
check(not junk, f"system files block the Claude directory: {junk}")
large = [p.relative_to(pkg) for p in pkg.rglob("*") if p.is_file() and p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg") and p.stat().st_size > 256 * 1024]
check(not large, f"non-image files over 256 KiB are held for a Claude reviewer: {large}")

if errors:
	print("Validation failed:", file=sys.stderr)
	for e in errors:
		print(f"  - {e}", file=sys.stderr)
	sys.exit(1)

print(f"Valid: {manifest['name']} — OpenAI {manifest['version']} ({len(positive)} positive / {len(negative)} negative cases), Claude {claude['version']}, README {words} words")
