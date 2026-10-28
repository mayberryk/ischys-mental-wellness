# Updating insurance and articles

The website is file-based; it does not currently have a login/dashboard for editing. Changes need a build and an authorized deployment before appearing online. Keith can handle this initially. A CMS can be added later if a browser-based editor is preferred.

## Insurance — one place

1. Open `content/insurance.json` (locally, or GitHub's file editor on a review branch).
2. Find the plan and edit `name`, `details`, `logo`, or `status`.
3. Use `active` only after Laura confirms the plan is effective. `pending` or `inactive` keeps it off both public lists.
4. For a new plan, add an object with a unique `id`, name, logo, status, and details. To display an approved logo, add its SVG file to `assets/insurance/` and set `logo` to `/assets/insurance/filename.svg`. Leave `logo` empty to show the plan name without an image. Do not substitute an unapproved logo.
5. Run `python3 scripts/check_site.py` and inspect `/fees-insurance/` and the footer. Both read the same active list.
6. Ask Keith to review and deploy. Confirm build/publish settings before using GitHub's editor if the hosting service auto-deploys commits.

## Articles — draft first

Existing client-package articles are marked `status: published` and `approved: true` to preserve the current review preview. This does not constitute final website launch approval. New entries missing either field remain unpublished.

1. Add a body file under `content/article-bodies/`, for example `new-topic.json`:
   `{"blocks":[{"type":"h2","text":"Section heading"},{"type":"p","text":"Laura’s supplied wording."}]}`
2. Add metadata to `content/articles.json` with unique `key`, `title`, `path` (e.g. `/learning/new-topic/`), `description`, `services` (related service slugs), `references` (objects with `title` and `url`), `source_file: article-bodies/new-topic.json`, `status: draft`, and `approved: false`.
3. Review drafts locally with `python3 scripts/build.py --include-drafts --output .draft-preview`. This output remains noindex and must not be deployed. Serve that separate directory locally if needed. Default builds exclude drafts from article pages, lists, related links and sitemap, and remove formerly published article HTML on rebuild.
4. Only after Laura approves the article, set `approved: true` and `status: published`. Add `published_at` only for an actual publication date, not a planned date.
5. Run checks and obtain Keith's instruction before pushing/deploying. To unpublish an article, change it back to draft, rebuild and redeploy.

The source wording from the original package is in `content/source-sections.json`. New body files avoid needing to edit that large import. No article content should be rewritten during a visual design update.
