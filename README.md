# Total CMS Plugins

The Total CMS plugin for the two AI plugin directories:

- **Claude** — Anthropic's directory (claude.ai, the desktop and mobile apps,
  Cowork, and Claude Code), which reads the plugin straight from this repo
- **OpenAI** — the directory shared by ChatGPT and Codex, which takes a ZIP
  upload

Both get the same plugin: a read-only connection to the public Total CMS
documentation server at `https://totalcms.co/mcp`, and the Total CMS agent
skill. The MCP server itself is the Total CMS docs extension running on
totalcms.co; changes to its tools reach both directories without a new plugin
version.

## Layout

```
package/                          # the plugin folder, shared by both directories
  .claude-plugin/plugin.json      # Claude manifest
  .codex-plugin/plugin.json       # OpenAI manifest: listing, review test cases, demo URL, release notes
  .mcp.json                       # the one MCP server: https://totalcms.co/mcp
  skills/totalcms/                # synced from core's resources/skill — don't edit here
  assets/logo.png                 # square icon (1024×1024)
  README.md                       # user-facing: Claude shows it as the listing description
  LICENSE                         # Claude requires one in the plugin folder
bin/
  build.sh                        # sync skill → validate → dist/totalcms-openai-plugin-<version>.zip
  validate.py                     # both directories' submission requirements
review/
  tool-justifications.md          # OpenAI annotation justifications, paste-ready
```

`.mcp.json` carries `"type": "http"` because Claude requires it; the build drops
it from the OpenAI ZIP, whose Codex format doesn't use it. The OpenAI ZIP also
leaves out the Claude manifest, README, and LICENSE.

Keep the plugin `name` as `totalcms` in both manifests — it's the listing's
identity in both directories.

## Building

```bash
bin/build.sh
```

The skill is copied from `../totalcms/resources/skill` (set `TOTALCMS_CORE` for
another checkout), so build from a core checkout on the release you want the
skill to describe. With Claude Code installed, the build also runs
`claude plugin validate`.

Commit the synced skill: Claude installs the plugin from this repo, not from a
build.

## Releasing to Claude

Claude's directory follows a branch or tag of this repo and publishes each new
commit on it after scanning it. Point the listing at a release tag, not
`master`, so a commit only reaches users when it's tagged.

1. Bump `version` in `package/.claude-plugin/plugin.json` — users stay on a
   version until it changes.
2. Run `bin/build.sh`, commit, and push.
3. Tag the release and push the tag.
4. Follow the scan in the developer portal at https://claude.ai/directory/manage.

The first submission is made from that portal: **Submit new → Plugin bundle**,
repository `totalcms/totalcms-plugins`, plugin folder `package`.

## Releasing to OpenAI

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

The two manifests version independently; each directory has its own release
history.

## The connector listing

The MCP server is also listed on its own in Claude's directory as a connector
(**Submit new → MCP connector**, URL `https://totalcms.co/mcp`). It isn't part
of this repo; the plugin's `.mcp.json` points at the same URL so the two
listings can be paired.

## Privacy

What the connector receives and returns is covered by the Total CMS privacy
policy: https://totalcms.co/privacy (see "AI connector"). Keep that policy in
step with what `https://totalcms.co/mcp` exposes anonymously — OpenAI rejected the
first plugin because the connector returned customer names the policy didn't
disclose (see CHANGELOG). OAuth must stay off on totalcms.co: with OAuth
discoverable, both directories try to make users sign in.
