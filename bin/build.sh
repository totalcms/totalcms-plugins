#!/usr/bin/env bash
# Build and check the Total CMS plugin for both directories.
#
#   bin/build.sh
#
# package/ is one plugin folder that serves both:
#   - Claude's directory reads it straight from GitHub (.claude-plugin/plugin.json)
#   - OpenAI's directory takes a ZIP upload (.codex-plugin/plugin.json)
#
# 1. Syncs the Total CMS skill from core (resources/skill is the source of truth).
# 2. Validates against OpenAI's limits, Claude's directory checks, and
#    `claude plugin validate` when Claude Code is installed.
# 3. Zips the OpenAI package to dist/totalcms-openai-plugin-<version>.zip.
#
# Set TOTALCMS_CORE to point at a core checkout other than ../totalcms.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORE="${TOTALCMS_CORE:-$ROOT/../totalcms}"
PKG="$ROOT/package"

if [[ ! -f "$CORE/resources/skill/SKILL.md" ]]; then
	echo "Core skill not found at $CORE/resources/skill — set TOTALCMS_CORE." >&2
	exit 1
fi

echo "Syncing skill from $CORE/resources/skill"
/bin/rm -rf "$PKG/skills/totalcms"
mkdir -p "$PKG/skills/totalcms"
cp -R "$CORE/resources/skill/." "$PKG/skills/totalcms/"
find "$PKG" -name .DS_Store -delete

python3 "$ROOT/bin/validate.py" "$PKG"

if command -v claude >/dev/null 2>&1; then
	claude plugin validate "$PKG"
else
	echo "Claude Code not installed — skipping 'claude plugin validate'."
fi

# OpenAI's ZIP takes only its own files, and its .mcp.json without Claude's
# "type" key, which the Codex format doesn't use.
VERSION="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$PKG/.codex-plugin/plugin.json")"
STAGE="$(mktemp -d)"
trap '/bin/rm -rf "$STAGE"' EXIT
cp -R "$PKG/.codex-plugin" "$PKG/assets" "$PKG/skills" "$STAGE/"
python3 - "$PKG/.mcp.json" "$STAGE/.mcp.json" <<'PY'
import json, sys
config = json.load(open(sys.argv[1]))
for server in config["mcpServers"].values():
	server.pop("type", None)
with open(sys.argv[2], "w") as out:
	json.dump(config, out, indent=2)
	out.write("\n")
PY

mkdir -p "$ROOT/dist"
ZIP="$ROOT/dist/totalcms-openai-plugin-$VERSION.zip"
/bin/rm -f "$ZIP"
(cd "$STAGE" && zip -q -X -r "$ZIP" .codex-plugin .mcp.json assets skills)

echo "Built $ZIP"
unzip -l "$ZIP" | tail -n +4 | sed '$d' | sed '$d' | awk '{print "  " $4}'
