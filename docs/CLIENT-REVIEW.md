# Client review — October 28, 2026

This revision is for review, not final publication. Do not push or deploy without Keith's instruction. Preview builds remain noindex and analytics stays disabled.

## Implemented

- Utah-only service wording; consistent American Fork address, phone, and public practice name.
- Original logo artwork preserved; two client-supplied photos used unchanged with CSS framing.
- New-patient booking uses exactly https://laura-jane-hyte-garner7671.clientsecure.me/ . No patient data is submitted by this site.
- Consultation calls 801-796-2552 and remains distinct from an evaluation or treatment visit.
- Existing-patient portal independently verified through the practice-branded SimplePractice Sign In page: https://laura-jane-hyte-garner7671.clientsecure.me/sign-in . No sign-in or patient information was submitted. Referral route remains telephone assistance until verified.
- Insurance names, logos, status, and notes now come from content/insurance.json for both footer and insurance page. The active list matches the September client package; pending plans are not displayed.
- New articles default to draft unless explicitly approved and published; current package articles retain their existing visibility.
- Privacy/legal pages are review drafts describing the actual public-site setup, rather than asserting unverified policies. Old policy wording is archived under docs/policy-review, not published.

## Unresolved — ask Laura / Keith

- Confirm the exact legal entity name. Do not assume an LLC name from the previous text.
- Confirm privacy@ischysmentalwellness.com and legal@ischysmentalwellness.com before using them. Neither is displayed as a verified contact.
- Approve final privacy/legal wording and policy effective dates; verify hosting logs/retention, third-party arrangements, and patient privacy policies. Production is gated on these confirmations.
- Confirm a secure referral destination. No referral form or appointment-within-three-days promise is present.
- SimplePractice currently displays “802 E Bamberger Rd” without Suite D on its sign-in page; Laura requested “802 E Bamberger Dr, Suite D.” Website follows her supplied address; ask her to reconcile the portal listing.
- Confirm final domain, account owner identities, and who should receive GitHub/hosting invitations. No ownership or permissions have been changed.
- Confirm whether article uploading is included in Keith's commercial arrangement. Do not promise an included service without that confirmation.
- Obtain final content and launch approval separately.

## Repository and hosting

Repository: https://github.com/mayberryk/ischys-mental-wellness (main).
Known Render preview: https://ischys-mental-wellness.onrender.com/ . The exact dashboard service ID, owner and current build settings have not been verified from an authenticated Render account.
No Vercel project configuration is present in this repository. A Vercel account/project may exist elsewhere; its relationship to Render remains unverified. Do not imply that they synchronize automatically.
To prepare an owner handoff, confirm Laura's GitHub username and hosting account email, inspect the existing owner/project, then arrange the requested invitation or transfer with Keith. No credentials belong in this repository or email.
Build: python3 scripts/build.py; publish: dist. Preview is not the final production domain. The public preview is unchanged by local edits until deployment is requested.
