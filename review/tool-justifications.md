# OpenAI plugin submission — tool annotation justifications

> Paste into the plugin dashboard when it asks for annotation justifications. Checked against the live server's 19 tools on 2026-09-30.

Paste-ready text for the 19 tools × 3 annotations on totalcms.co/mcp.
Every tool is Read Only: true, Open World: false, Destructive: false.

**Shared truths** (woven into each entry rather than repeated verbatim, so the
reviewer sees tool-specific confirmation):

- The server is a Total CMS site. All data lives in flat JSON files and
  markdown on that server; there is no external API call in any code path.
- The 19 tools listed are the **public, anonymous** surface. Every
  create/update/delete tool in Total CMS requires an API key or OAuth token
  and is not exposed to unauthenticated callers, so nothing in this list has
  a write path available to it.
- All results are deterministic for the same inputs and site state; repeated
  calls change nothing.

---

## describe_collection

**Read Only — true:** Returns a collection's stored metadata and the property
definitions from its schema file. It reads schema and collection JSON only;
there is no code path from this tool to any writer.

**Open World — false:** Operates strictly on collections defined in this one
site's data directory. The set of possible answers is fully enumerable from
this server; it makes no network request and touches no third-party service.

**Destructive — false:** Nothing is written, modified, or deleted. Calling it
repeatedly returns the same description and leaves the site byte-identical.

## describe_view

**Read Only — true:** Returns a data view's metadata (id, name, last built,
item count) and its output shape, read from the view's cached definition. No
writer is reachable from this tool, and it does not trigger a rebuild.

**Open World — false:** Limited to data views defined on this site. Views are
Twig-defined queries over the site's own collections — no external data source
is involved.

**Destructive — false:** Read-only inspection of an existing cached view.
Nothing is created, invalidated, or removed.

## docs_get

**Read Only — true:** Reads one documentation markdown file that ships inside
the Total CMS package and returns its text. File reads only; no write path.

**Open World — false:** The path is validated against the shipped
documentation index before any file is read, so it can only return pages from
this fixed, versioned corpus — not arbitrary files or URLs.

**Destructive — false:** Opens a file for reading and returns its contents.
Nothing on disk changes.

## docs_lookup

**Read Only — true:** Looks up an entry in a pre-generated reference index
(Twig functions and filters, field types, REST endpoints, schema keys, CLI
commands, extension and builder APIs) that ships with the package. It reads
one JSON file and returns a matching entry.

**Open World — false:** Answers come only from that bundled index, which is
generated at build time from this version's source and documentation. There is
no lookup against any external registry or network service.

**Destructive — false:** A dictionary lookup. No data is written or removed,
and the index itself is never modified at runtime.

## docs_search

**Read Only — true:** Scores a query against a pre-built search index of the
documentation that ships with the package and returns matching page paths and
titles. Reading only.

**Open World — false:** Searches a fixed, bundled corpus — the documentation
for the exact Total CMS version this site runs. It is not a web search and
reaches no external index.

**Destructive — false:** Computes relevance scores in memory and returns
matches. Nothing is stored, logged as content, or altered.

## fetch

**Read Only — true:** Returns the full stored document for an id previously
returned by `search` — title, readable body text, URL, and metadata. It reads
existing site content and returns it.

**Open World — false:** Despite the name, this fetches from **this site's own
content**, not from the internet. It accepts an id from this server's own
search results and resolves it against local collections; it cannot be pointed
at an arbitrary URL and makes no outbound HTTP request.

**Destructive — false:** Retrieval only. The document is returned unchanged
and nothing is written.

## find_comparison

**Read Only — true:** A site-defined saved query over the `comparisons`
collection: matches a competitor name and returns the stored comparison page.
The query layer it uses is read-only by construction.

**Open World — false:** Bounded to comparison pages published on this site.
The filters and result limit are fixed in the site's own configuration; the
tool cannot query anything else or reach outside the collection.

**Destructive — false:** A filtered read of published content. No records are
created, changed, or removed.

## get_object

**Read Only — true:** Fetches one object by id from a collection and returns
its fields. Non-public fields are stripped before the response; no write path
exists from this tool.

**Open World — false:** Resolves ids only within this site's collections, and
only those a caller is permitted to see. No external identifier space is
involved.

**Destructive — false:** Single-record read. The object is returned as stored
and remains unchanged.

## get_resource

**Read Only — true:** Resolves a `tcms://{collection}/{id}` URI to the
underlying object — functionally identical to `get_object`, addressed by URI
instead of arguments. Read-only.

**Open World — false:** The `tcms://` scheme addresses this server's own
objects exclusively. It cannot resolve `http(s)://` or any other scheme, so no
external resource can be reached.

**Destructive — false:** URI resolution followed by a read. Nothing is
modified.

## get_view

**Read Only — true:** Returns a data view's cached result set. It reads the
stored cache; it does not rebuild the view or write to it.

**Open World — false:** Data views are Twig-defined aggregations over this
site's own collections. The result set is precomputed and local.

**Destructive — false:** Reads a cache entry. It is neither invalidated nor
regenerated by this call.

## latest_release

**Read Only — true:** A site-defined saved query returning the most recent
entry from the `changelog` collection — version, title, date, and body.

**Open World — false:** Fixed to one collection on this site with the sort and
limit defined in the site's configuration. It cannot be redirected to other
data and makes no external request.

**Destructive — false:** Returns published release notes as stored. Nothing is
written.

## list_collections

**Read Only — true:** Enumerates the collections visible to the caller with
their id, display name, and schema id. Metadata read only.

**Open World — false:** Lists only what exists on this site, filtered to what
the caller's persona may see. There is no discovery of external systems.

**Destructive — false:** Enumeration. Nothing is created or deleted, and
collection metadata is untouched.

## list_views

**Read Only — true:** Enumerates the data views visible to the caller. Reads
view definitions and returns a lean overview.

**Open World — false:** Limited to views defined on this site; no external
source is consulted.

**Destructive — false:** Read-only listing; no view is built, rebuilt, or
removed.

## needs_review

**Read Only — true:** A site-defined saved query ordering comparison pages by
how long ago their facts were verified. It reads and sorts stored records.

**Open World — false:** Queries one collection on this site with fixed
filters. The optional date argument narrows results within that collection and
cannot widen scope beyond it.

**Destructive — false:** Sorting and filtering a read result. It does not mark
anything as reviewed or change any record.

## query_collection

**Read Only — true:** Returns paginated items from a collection with total,
limit, offset, and has_more. Query execution runs against a read-only index;
non-public fields are stripped before the response.

**Open World — false:** Queries only this site's collections, restricted to
those the caller may see. Filters and sorting operate on local indexed data
with no external query federation.

**Destructive — false:** Reading with pagination. No item is created, updated,
or deleted, and the index is not modified.

## query_view

**Read Only — true:** Paginated query against a data view's cached result,
using the same read-only query vocabulary as `query_collection`.

**Open World — false:** Restricted to precomputed views over this site's own
collections. No external data is queried and the view is not rebuilt.

**Destructive — false:** Reads and paginates cached data. Nothing is written
or invalidated.

## search

**Read Only — true:** Full-text search across the collections the caller can
see, returning `{id, title, url}` for each hit. It reads the site's search
index only.

**Open World — false:** Searches this site's content exclusively. It is the
site-scoped search companion to `fetch`, not a web search — no external search
provider or network call is involved.

**Destructive — false:** Computes matches and returns references. Nothing is
stored or altered.

## search_collection

**Read Only — true:** Free-text search within one named collection, returning
matching items with a public URL. Read-only against the search index.

**Open World — false:** Scoped to a single collection on this site, and only
if the caller may see it. No external corpus is searched.

**Destructive — false:** Search and return. No records change.

## search_collections

**Read Only — true:** Full-text search across every collection the caller can
see in one call, labelling each hit with its source collection. Read-only.

**Open World — false:** Spans this site's collections only — "all collections"
means all collections *on this server*, not any external system.

**Destructive — false:** Returns matches from stored content; nothing is
written or removed.
