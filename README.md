# Ischys Integrative Mental Wellness

Static website generated from shared templates and structured content. Requires Python 3.10 or newer; the website build uses only the standard library.

## Local development

Run `python3 scripts/dev.py`, then open http://localhost:8080. Source changes rebuild automatically.

Run `python3 scripts/check_site.py` to build and validate pages, internal links, metadata, article coverage, and PDF availability.

## Build and hosting

Run `python3 scripts/build.py`. Publish **dist/**, not the repository root. On Render Static Sites, set Build Command to `python3 scripts/build.py` and Publish Directory to `dist`. Existing service settings must be updated manually if they still publish the old HTML files from the repository root.

This default build is a review preview: search indexing and analytics are disabled. Scheduling, consultation, portal, and referral destinations remain placeholders until configured in `content/site.json`.

For a public launch, configure the production domain, approved integration URLs, original logo, and clinical approval in `content/site.json`, then use `python3 scripts/build.py --production`. The production build fails when required configuration is missing. Optional analytics also requires its configuration and review. Configure the host to honor the generated `_redirects` and `_headers`, or translate them into the host's equivalent rules. HTML redirect fallbacks are generated for legacy pages.

## Editing

The homepage features three Learning Center articles. Add an optional `published_at` date (`YYYY-MM-DD`) to an article in `content/articles.json` to place newer published posts first. Undated slots use the article keys in `homepage_featured_articles` in `content/site.json`, then the remaining article order. Only use actual publication dates; undated articles display “Patient education.”

- `content/`: site settings, client content, articles, and resource definitions.
- `templates/page.html`: shared page shell.
- `scripts/build.py`: page assembly and metadata.
- `static/`: CSS, JavaScript, favicon, images, and locally hosted font with license.
- `assets/`: original logo and insurance artwork.
- `output/pdf/`: downloadable patient resources copied into the build.

Keep client-directed wording unchanged during visual design work. PDF regeneration uses `scripts/build_pdfs.py` and requires ReportLab and suitable fonts; generated PDFs are already included. PDF visual/editorial review remains part of launch preparation.

Do not commit or push changes unless explicitly requested.
