# CMS production preparation — November 2, 2026

## Current status

The local editor works against an isolated Git repository. The public site remains static. No production editor, authentication service, permissions, GitHub changes or hosting changes have been deployed.

The verified repository remote is `https://github.com/mayberryk/ischys-mental-wellness`. Render is a known review preview. Joe's final hosting provider, domain, deployment branch/settings and Laura's GitHub account remain unknown. There is no Render, Vercel or Netlify deployment configuration in the repository that establishes Joe's setup.

## Dependency review

`npm audit` reports **38 affected dependency entries: 11 high, 26 moderate, 1 low, 0 critical**. These totals include propagation through parent packages, not 38 independent vulnerabilities. The direct advisory-bearing packages are:

- `@hapi/joi`: prototype pollution and email-validation denial of service; appears in the local proxy's CLI dependencies.
- `zod`: excessive memory use during constrained collection validation; appears in the local CLI dependency tree.
- `trim`: regular-expression denial of service in the Markdown dependency chain.
- `@platejs/core`: HTML deserialization can trigger browser behavior; relevant to reviewing rich-text paste/import handling.
- `deepmerge`: prototype poisoning of merged objects.
- `minimatch`: denial of service during glob processing.
- `uuid`: missing buffer bounds checks in certain UUID functions.

This is dependency triage, not proof that every issue is exploitable in this application's flow. Both `decap-cms@3.17.3` and `decap-server@3.11.6` were the current registry releases at review time. `npm audit fix --dry-run --json` proposed **zero changes** and left the counts unchanged. Force recommendations include downgrades; they have not been applied.

The public website does not load these CMS packages. The local proxy is restricted to loopback and must never be deployed. The prospective admin uses Decap's prebuilt browser bundle: npm overrides to nested packages do not rebuild that bundle, so a lower dependency-tree audit count alone would not establish a fixed editor. Before live admin release, use a verified patched upstream bundle or a reviewed custom rebuild with regression tests; otherwise record an explicit, informed risk decision. The packaging gate defaults to blocked. No security approval is implied by local functional tests.

Advisory evidence is recorded in `cms/dependency-review.json`. Refresh the audit when preparing the actual release.

## Prepared configuration

`cms/production-settings.example.json` contains the known repository and unresolved public settings. Copy it to ignored `cms/production-settings.json` after confirming the values. No OAuth client secrets or access tokens belong in either file.

`python3 scripts/prepare_cms.py --settings cms/production-settings.json` prepares `.cms-release/admin/` only after HTTPS origins and the dependency-review decision are supplied. It switches to the GitHub backend, removes `local_backend`, uses production URLs, preserves the collections/editorial workflow, and bundles the editor assets locally. It does not create an OAuth service, copy itself into the public build, invite anyone, commit, push or deploy. Existing output must be archived before regenerating.

Once approved and connected, the host build should install the pinned Node dependencies, build the website using the correct preview/production mode, generate the CMS package, and copy `.cms-release/admin/` into `dist/admin/`. Implement the exact host configuration only after Joe's setup is known. The current Python-only build remains unchanged and excludes the admin.

GitHub-backed login requires repository push access and an OAuth service. The browser gets only the service URL; the OAuth client secret stays server-side. Confirm the selected service's callback URL, exact allowed editor origin, state validation, token handling and account ownership before setup. Review branch protection and publishing privileges with Joe; the approval checkbox is an editorial control, not authorization enforcement.

## Information needed from Joe / Laura

1. Hosting provider, project/site name, final domain, and whether it already builds from GitHub.
2. Deployment branch, build command and publish directory currently configured.
3. Laura's and Joe's GitHub usernames, or confirmation they need accounts.
4. Who may publish articles and who maintains the authentication service.

Do not request passwords or secrets by email. Share project/account invitations through the providers after the access scope is agreed.

## Release acceptance checks

- Sign in as Laura; verify an unauthorized account cannot edit the repository.
- Save a draft and confirm it is absent from the public site, listings and sitemap. Test an edit to an existing published article as a draft too.
- Approve, mark Ready, publish; confirm GitHub changes and the correct hosting deployment complete.
- Check topic badges, all seven filters, service links, image/file uploads and mobile display.
- Edit insurance once and verify both public lists. Unpublish an article and confirm its old page is removed.
- Verify failed builds leave the last successful live deployment available and someone receives the failure notice.
- Restore a prior revision in a staging copy and rebuild. Deliver source ZIP and documented asset/content backups; a source ZIP excludes OAuth secrets and hosting/account settings.
- Confirm outstanding practice address, referral route, final domain and policy approvals before using the production launch build.

References: https://decapcms.org/docs/github-backend/ and https://decapcms.org/docs/external-oauth-clients/

## Follow-up assessment and release scope

Closer inspection of the shipped `decap-cms.js.map` found patched `trim@0.0.3` in the browser bundle despite vulnerable `trim@0.0.1` in the installed dependency tree. Plate 49.2.21 remains bundled; Decap's normal HTML paste handler uses its own rehype parsing pipeline. Fallback reachability has not been conclusively tested. Decap 3.17.3 release notes explicitly include security work. The raw audit count is not a verdict on the deployed browser bundle.

Keith authorized proceeding with Decap and pushing the website/CMS source on November 2. This release retains the existing Render review-preview behavior. It does not publish an admin login or provision authentication. Laura's GitHub username and an OAuth hosting project remain unavailable and must be requested. Do not supply invented credentials or publish the local login proxy. Final patient-facing launch approvals remain separate.
