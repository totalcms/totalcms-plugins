# Total CMS OpenAI Plugin Changelog

All notable changes to the Total CMS OpenAI plugin listing will be documented in this file.

## [1.0.0] - 2026-09-30

Initial release as a new plugin in the plugin dashboard.

- **Connector**: One read-only MCP server, `https://totalcms.co/mcp` — documentation search and pages, reference lookups (Twig functions and filters, field types, REST API endpoints, schema configuration keys, CLI commands), release notes, the extensions catalog, comparisons, and buying guides
- **Skill**: The Total CMS site-building skill, synced from core's `resources/skill`
- **Review**: Five positive and three negative test cases, run against the live server on 2026-09-30

### Background

An earlier plugin, created through OpenAI's previous submission form, was not approved (v1.0.0, August 2026) and was replaced by this one. Its lessons are built in:

- **Privacy policy covers the connector**: The review found that totalcms.co/privacy did not disclose what the connector collects, why, who receives it, or how long it's kept. The policy now has an "AI connector (MCP server)" section: tool inputs and request data received, used only to answer the request, 60-second rate-limit counters, 14-day request logs, Cloudflare as the network provider, and how to disconnect
- **No personal data**: Testimonials, showcase entries, and Site Builder page records had been exposed to anonymous callers, returning customers' names and businesses plus nested image metadata. Those collections are now admin-only on totalcms.co
- **No promises the plugin can't keep**: The automated metadata check flagged guarantee language ("official", "complete documentation", "always match the current release"). The description now says what the tools do, and that answers are only as current and complete as the published documentation
- **Why a new plugin**: The old plugin kept an MCP server from the previous submission form that the new dashboard can't configure or remove, and only one MCP server can be connected per plugin
