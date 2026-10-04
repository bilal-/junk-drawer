# Private backup profiles

Pass a JSON file to `project_backup.py build --profile`. Keep profiles outside
public source trees with permission `0600`. Use absolute paths or `~`; update
paths after moving laptops. Never put credential values in a profile.

```json
{
  "schema_version": 1,
  "roots": ["~/workspace/organization", "~/workspace/personal/app"],
  "account_notes": "Use the account selected by each workspace's AGENTS.md.",
  "projects": {
    "app": {
      "notes": "Keep the exact application encryption key with its database.",
      "missing": ["Production encryption key has no local export."],
      "files": [
        {
          "source": "~/.config/app/service-account.json",
          "destination": "Private Configuration/service-account.json",
          "description": "Service account used by the background service.",
          "restore": "Restore outside Git and set the service's credential path."
        }
      ]
    }
  },
  "shared_files": [
    {
      "source": "~/.config/releases/upload.p12",
      "destination": "Credentials/Android Upload Signing/upload.p12",
      "description": "Shared Android upload signing key.",
      "restore": "Keep its password, alias and certificate fingerprint together."
    }
  ],
  "loose_areas": [],
  "tool_files": [],
  "missing": ["Provider recovery codes are held separately."]
}
```

Discovery uses the repository folder name as the project ID; duplicate names
get a short path suffix. `projects` uses those IDs. Project `files` destinations
are relative to that project's folder. `shared_files`, `loose_areas` and
`tool_files` destinations are relative to the package root. Every selected file
needs `description` and `restore` instructions. Missing required files stop the
build; list unavailable assets in `missing` instead of creating placeholders.
Set `exclude: true` for reviewed projects with no private assets to capture;
they remain in the discovery inventory.

The default copies untracked signing material and private configuration. It
does not copy repositories, tracked guides, branding, screenshots, dependencies
or rebuildable application artifacts. Read the guides in Git to write restore
notes. Select external credential files explicitly. For a project without a
Git/package marker, select its private files through `shared_files`; never add
its whole source directory as a `loose_areas` entry.

Select hosted production data exports explicitly through a project's `files`.
State the environment, capture time and encryption-key dependencies. Refresh
exports before building a new backup; a path to a previous export is not a
new capture. Object storage needs original keys, bytes, metadata and an inventory.
Provider records listing secret names do not back up their values.

Local development databases and old exports are excluded by default. Opt in
with `include_local_data` or `include_historical_exports` only when the user
needs unique data that cannot be recreated. `loose_areas` is for reviewed
private configuration/state folders or the backup tooling itself.

`--extend` adds reviewed projects to a verified package and refuses project-folder
collisions. Prefer a new dated destination for future refreshes. Review profiles
each time rather than blindly replaying old paths and provider records.
