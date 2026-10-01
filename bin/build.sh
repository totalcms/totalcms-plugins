#!/usr/bin/env bash
# Build the OpenAI plugin ZIP for upload at https://platform.openai.com/plugins.
#
#   bin/build.sh
#
# 1. Syncs the Total CMS skill from core (resources/skill is the source of truth).
# 2. Validates the manifest against OpenAI's submission limits.
# 3. Zips package/ to dist/totalcms-openai-plugin-<version>.zip.
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

VERSION="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$PKG/.codex-plugin/plugin.json")"
mkdir -p "$ROOT/dist"
ZIP="$ROOT/dist/totalcms-openai-plugin-$VERSION.zip"
/bin/rm -f "$ZIP"
(cd "$PKG" && zip -q -X -r "$ZIP" .codex-plugin .mcp.json assets skills)

echo "Built $ZIP"
unzip -l "$ZIP" | tail -n +4 | sed '$d' | sed '$d' | awk '{print "  " $4}'
