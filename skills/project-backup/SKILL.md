---
name: project-backup
description: "Back up project files that Git cannot recover: signing keys, API credentials, private configuration, and persistent state. Audit selected projects or nested workspaces and prepare a documented, verified folder for manual cloud upload or laptop migration."
---

# Project backup

Create a folder for important files outside Git at the destination the user chooses. Accept multiple
workspace roots and projects from any organization. Write `Projects`,
`Credentials`, `Computers`, and `Tools` directly under that destination; do not
insert an organization wrapper. Keep organizational account rules in the local
profile and project instructions, outside this skill.

The default scope excludes repository copies, Git bundles, source snapshots,
tracked documentation, branding, screenshots, dependencies, and rebuildable
applications/artifacts. Read repository guides to understand credential usage;
write concise new recovery notes instead of copying those guides. Repository
archival is outside this skill. A repository hosted in Git does not need a
duplicate backup merely because its credentials do.

## Discover and explain

Read applicable `AGENTS.md` / `CLAUDE.md` instructions. Recursively inventory the
roots, including nested clients, apps, repositories, linked Git worktrees, and
non-Git projects. Deduplicate worktrees by Git common directory. Identify private
configuration or persistent state outside the detected projects.

Use `scripts/project_backup.py inventory --root <path> --output <private-json>`
for discovery. Review project READMEs, hosting configuration and recovery
runbooks to identify what Git cannot recover: ignored configuration,
signing identities, service-account keys, encryption keys, databases, object
storage, domain ownership, account access, and machine-bound state. Trace any
external credential paths named in those files. Inspect values locally only when
necessary; report names and status, never secret values.

For repeated use, keep a private JSON profile using
[references/profile.md](references/profile.md). Profiles contain paths, copy
descriptions, account-selection notes and known gaps; they must not contain
credential values. Refresh discovery and pending items on each invocation.

## Assemble

Build a new dated destination for each refresh. An explicitly requested update to
an existing package may use `--extend`, preserving prior files and refreshing its
manifest. Never silently overwrite an unrelated directory or delete originals.

`scripts/project_backup.py build --profile <private-json> --destination <path>`
copies selected credentials, private configuration and persistent state, and
writes project-specific restore notes. Inspect ignored files across linked
worktrees without copying their source. Add associated keys/configuration from
outside the workspace through the profile. Capture production or user data when
it belongs in the requested scope; skip local fixtures that can be recreated
from Git. A names-only provider inventory or an empty credential folder is not
a backup of its secret values.

Use account rules from each workspace for any read-only provider inspection.
Export hosted databases or objects when requested backup scope and account access
support it. Do not deploy, upload to a cloud drive, rotate keys, grant access,
restart services or restore over running data merely to build a backup. Do not
scrape browser sessions, password managers or an entire keychain. If an identity
needs an export, identify the particular certificate and private key first.

Use SQLite's online backup API rather than copying a live database without its
WAL. Hash copied files against stable source reads. Capture changing sources with
bounded attempts; report a source that does not stabilize. Explain which snapshots
are live, historical, local, production, or final stopped-service migration
captures. Never label a live copy as a qualified cold handoff or a checksum check
as a tested restore.

## Verify and deliver

Require owner-only permissions, independent regular-file copies, a README in
each folder, `MANIFEST.json`, `SHA256SUMS.txt`, a standalone verifier and a projects
index. Inspect generated notes for actual recovery steps and specific remaining
gaps. Verify copied credentials and data snapshots. Run the packaged checksum verifier
from a different working directory and, when practical, rehearse a non-destructive
configuration/data restore in a temporary directory.

Keep plaintext secrets confined to the private package. Leave rebuildable
dependencies, caches, logs and temporary sockets out. Do not commit the package
to a source repository.

Report the destination, covered projects, verification result and material gaps.
For manual cloud upload, tell the user to download the uploaded folder and rerun
its verifier before deleting the local copy. Do not claim the upload occurred.
This skill runs when invoked; it does not install a scheduler or monitor projects.
