# Total CMS OpenAI Plugin

The package behind the Total CMS listing in OpenAI's plugin directory, which is
shared by ChatGPT and Codex. It connects them to the public Total CMS
documentation server at `https://totalcms.co/mcp` and bundles the Total CMS
agent skill.

This repo holds only the listing: metadata, review test cases, the logo, and a
copy of the skill. The MCP server itself is the Total CMS docs extension running
on totalcms.co, and changes to its tools reach ChatGPT through OpenAI's daily
MCP scans — no new upload needed. Upload a new ZIP only when something in
`package/` changes.

## Layout

```
package/                  # exactly what goes in the ZIP
  .codex-plugin/plugin.json   # listing, review test cases, release notes
  .mcp.json                   # the one MCP server: https://totalcms.co/mcp
  assets/logo.png             # square listing + composer icon (1024×1024)
  skills/totalcms/            # synced from core's resources/skill — don't edit here
bin/
  build.sh                # sync skill → validate → dist/totalcms-openai-plugin-<version>.zip
  validate.py             # OpenAI's submission limits and required fields
```

The manifest uses the Codex package format (`.codex-plugin/plugin.json`).
The plugin `name` is `totalcms`; keep it stable across uploads.

## Building

```bash
bin/build.sh
```

The skill is copied from `../totalcms/resources/skill` (set `TOTALCMS_CORE` for
another checkout), so build from a core checkout on the release you want the
skill to describe.

## Releasing an update

1. Edit `package/.codex-plugin/plugin.json`: bump `version`, update
   `extensions.com.openai.publication.release_notes`, and re-check the test
   cases against the live server (test case 4 names the current release).
2. Run `bin/build.sh`.
3. At https://platform.openai.com/plugins, open **Total CMS** → **Upload plugin**
   and choose the ZIP from `dist/`.
4. Resolve anything under **Metadata & Skills → Issues detected**, confirm the
   imported demo recording URL in **Review details**, then **Submit for review**.
5. Once approved, choose **Publish plugin**.

Test cases and the demo recording URL (`review.demo_recording_url`) are imported
from the ZIP and read-only in the dashboard — change them here and upload again.
The dashboard refuses to submit without the demo URL in the package.

## Privacy

What the connector receives and returns is covered by the Total CMS privacy
policy: https://totalcms.co/privacy (see "AI connector"). Keep that policy in
step with what `https://totalcms.co/mcp` exposes anonymously — OpenAI rejected the
first plugin because the connector returned customer names the policy didn't
disclose (see CHANGELOG).
