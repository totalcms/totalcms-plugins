# Total CMS

Total CMS is a flat-file PHP CMS. This plugin lets Claude search and read the
Total CMS documentation while answering your questions about it, and adds a
skill with guidance on how Total CMS sites are built.

Documentation: https://docs.totalcms.co

## What's included

**Documentation connector.** A read-only connection to https://totalcms.co/mcp
— the public Total CMS documentation server. Claude can search and read
documentation pages, and look up reference entries — Twig functions and
filters, field types, REST API endpoints, schema configuration keys, and CLI
commands — with their signatures, options, and examples. It can also read
release notes, the extensions catalog, product comparisons, and buying guides.

**Total CMS skill.** Reference guidance on how Total CMS sites are built:
collections and schemas, the Site Builder, the `tcms` CLI, the frontend
pipeline, and going live. In Claude Code it applies when you work in a Total
CMS project.

## Example prompts

- How do I resize and crop an image in a Total CMS Twig template?
- What options does the tcms builder:init command take?
- What's new in the latest Total CMS release?

## Limitations

The connector is read-only and serves only Total CMS's published documentation
and product content. It can't see, change, or troubleshoot your own Total CMS
site, and answers are only as current and complete as the published
documentation. No account, login, or API key is required.

## Privacy Policy

Privacy policy: https://totalcms.co/privacy (see "AI connector").

When Claude calls a documentation tool, the plugin sends the tool's inputs — a
search phrase, a documentation path, or the id of a published page — to
https://totalcms.co/mcp, along with standard request data such as IP address
and user agent. Nothing else is sent, and the plugin runs no local code. Request
logs are kept for 14 days, and the connector returns no personal data.

## Support

https://totalcms.co/support
