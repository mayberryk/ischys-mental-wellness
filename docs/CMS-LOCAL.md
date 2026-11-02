# Local CMS trial

Run `npm ci`, then `npm run cms` (Node 20+ and Python 3.12+ for the local sandbox runner).
Open **http://localhost:8090/admin/** and click **Login**. This is a local simulated login, not a real account/password check. The published sandbox preview is **http://localhost:8090/**. The usual site preview remains on port 8080.

## Try an article

1. Open Articles and select an existing article, or choose **+ Article**.
2. Enter a title, URL name (lowercase words with hyphens), short introduction, article topics, and article text. The editor supports headings, formatting, links, and images. Keep existing URL names unchanged.
3. Optionally upload a cover image and its description, or a downloadable attachment. Uploading a Word/PDF file attaches it; it does not import its text. Paste the article text into the visual editor.
4. **Save** retains a draft. Find saved drafts under **Workflow**.
5. After Laura approves publication, enable **Approved for publication**. Save, change the top workflow status from Draft to **Ready**, then choose **Publish → Publish now** and confirm. The local published preview rebuilds automatically in a few seconds.
6. To take an article off the preview, turn off Approved for publication, save, and publish that change. An ordinary build also requires approval to be true. These controls prevent accidental visibility; they are not an account permission system.

## Try insurance

Open Insurance → Insurance plans. Edit a name, upload a logo, change status or add details. Only active plans appear. Save, move its workflow status to Ready, then publish and confirm the change. Both the footer and insurance page read this same list.

## Where edits go

The first run copies content and assets into `.cms-local/repository/`, an ignored, isolated Git repository with **no remote**. Decap uses local branches and commits for its editorial workflow. These are trial history only: no commits are made to the website's main Git repository and nothing is pushed to GitHub.

The watcher exports only the sandbox's `main` branch into `.cms-local/preview/` and rebuilds it. Draft branches never enter that preview. Trial edits persist between restarts. They do **not** change the real source under `content/`. To start fresh, stop the trial, rename `.cms-local/` as a backup, then restart. This avoids deleting trial edits accidentally.

The source migration itself is in `content/articles/*.json`: one article per file, with a Markdown body. Existing URLs, references, approval flags and wording are preserved. `docs/content-before-cms/articles.json` retains the original metadata, and `content/source-sections.json` retains original article wording for comparison. Only the per-article files drive the build now. Tests verify this migration.

## Before connecting to a live site

- Confirm Joe's hosting and automatic build/deployment setup.
- Configure a real GitHub/OAuth login, authorized accounts, and publishing permissions. Do not expose the local proxy online.
- Create a production CMS config. The current local-only admin is deliberately excluded from `dist/`; normal site builds do not publish it.
- Test actual GitHub branch/PR publishing, host build failures, media, backups and recovery.
- Review the dependency advisories before release. The pinned Decap packages currently report transitive vulnerabilities, including high-severity advisories; the local trial is not a production security sign-off. Do not blindly force-downgrade the proxy: the pinned release has localhost binding protections.
- Confirm Laura finds the workflow comfortable. The editor has one approval control; the hidden visibility field follows it automatically on save. Decap still requires Ready → Publish.

No CMS subscription is introduced by this trial. Production authentication/hosting costs and maintenance remain to be scoped.

## Checks and rollback

Run `npm test`, `python3 scripts/check_client_revisions.py`, and `npm run test:cms`.
The public site still builds with `python3 scripts/build.py`; Mistune 3.2.0 is vendored under `scripts/vendor/` with its BSD license, so no Python package installation is needed on the host.

To roll back, stop `npm run cms`, review the local diff, and revert only the CMS-related changes. Restore the original article metadata from `docs/content-before-cms/articles.json` along with the previous build adapter. Keep any unrelated local work and trial edits. No remote rollback is needed because this work has not been pushed.
