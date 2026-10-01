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

if errors:
	print("Validation failed:", file=sys.stderr)
	for e in errors:
		print(f"  - {e}", file=sys.stderr)
	sys.exit(1)

print(f"Valid: {manifest['name']} {manifest['version']} — {len(positive)} positive / {len(negative)} negative cases")
