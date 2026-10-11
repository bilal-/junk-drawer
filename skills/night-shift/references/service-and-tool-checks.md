# Checks for services, tools, and data pipelines

Read only the sections selected by [stack detection](stack-detection.md), in
addition to the common checks. Use installed versions and project commands.
These questions apply only to code and contracts touched by the finding.

## Next.js server-rendered web apps

- Apply the React checks and identify the router, server/client module
  boundaries, route handlers/actions, and host. Moving an import across a
  client boundary can change bundling and expose server-only dependencies.
- Preserve route/base-path behaviour, request-scoped auth, serialization,
  caching/revalidation, rendering mode, and server-action contracts. Check
  version-specific semantics; do not apply the latest Next conventions to a
  project pinned to an earlier version as incidental cleanup.
- Run the production build and affected route/interaction checks for the
  actual deployment target. A standalone Node/Docker output, static export,
  and a Workers adapter are different targets; account for each affected one.

## Node.js services, CLIs, and containers

- Preserve stdout/stderr and exit codes for CLIs, signal handling and child
  lifetimes, connection cleanup, stream backpressure, and bounded queues.
  For WebSocket/WebRTC or IPC changes, inspect handshake, reconnect, ordering,
  cancellation, and disconnect paths. An HTTP-only test may miss these.
- Check the Node version, native add-ons/binaries, module format and package
  exports used by the shipped artifact. Test the built CLI/server as well as
  source where bundling or resolution is affected.
- For container changes, validate the affected image, entry point, OS/CPU
  assumptions, writable paths, persistent volumes, and graceful shutdown in
  an isolated environment. A host build does not establish Linux image or
  native-binary compatibility. Avoid touching installed services or real
  terminal sessions to obtain test evidence.

## Google Apps Script

- Distinguish Apps Script server code, its HTML/browser client, and local
  Node tooling. Preserve callable function names, `doGet`/`doPost`, trigger
  handlers, and `google.script.run` contracts; textual callers may be absent.
- Preserve manifest runtime/scopes, execution identity, access rules, service
  authorization, per-user state, quotas, and lock scope. When refactoring
  Sheets/Drive/mail flows, keep idempotency, freshness checks, and unknown
  outcome handling around external effects.
- V8 language support does not supply Node APIs. Local Node harnesses validate
  modeled behaviour, not Google identity, permissions, quotas, or delivery.
  Use existing platform checks when available; otherwise record or defer the
  affected integration. Do not push a script, deploy, send mail, or mutate
  live Sheets/Drive as an incidental validation step.

## PHP web apps

- Identify the supported PHP version/extensions, entry points, include and
  autoload boundaries, sessions, and database engine. A procedural app need
  not have a framework. Preserve globals and include-time effects when moving
  code; output before headers can change redirects or downloads.
- Preserve auth/CSRF checks, session behaviour, HTTP status/headers, form and
  AJAX responses, transaction boundaries, and file/mail side effects. Confirm
  that an extraction does not bypass a guard on another entry path.
- Use the existing PHPUnit and HTTP/integration checks against an isolated
  database with the intended engine. SQLite doubles cannot establish MySQL
  semantics. Do not change schema, interpreter requirements, or framework as
  a side effect of cleanup.

## Go tools and services

- Inspect modules/workspaces, build tags, OS-specific files, CLI and plugin
  contracts. Preserve error wrapping, cancellation, goroutine/channel
  ownership, file locks, and atomic state updates when restructuring.
- Use the project's vet/test/build gate and race detector where required or
  relevant; exercise the concurrent path rather than treating compilation as
  race evidence. Check affected OS/build-tag variants.
- Test CLI output, subprocess exit/timeout handling, and plugins through the
  public contract with isolated homes and fake external commands. Keep real
  user configuration, account tools, and background services out of tests.

## Shell tools and installers

- Identify the declared shell and minimum version: POSIX `sh`, Bash 3.2, and
  current Bash are not interchangeable. Preserve quoting, argument boundaries,
  pipeline/exit status, traps, cleanup, locks, and subprocess lifetime.
- Inspect sourced helpers, executable modes, install paths, symlink handling,
  and macOS/GNU utility differences. A shell linter is useful but cannot prove
  behaviour under every supported interpreter.
- Run the project's shell/interpreter matrix and isolated installer/CLI tests
  for the affected paths. Avoid writing into the real home or installing,
  launching, or updating the user's tools just to verify an extraction.

## Python and JavaScript data, content, and font pipelines

- Identify the actual interpreter/imports and entry points even without a
  manifest. Preserve encoding, Unicode normalization, text ordering, units,
  numeric coercion/rounding, missing-value rules, schema and output formats.
- For spreadsheets/reports, check stable fixtures at input/output boundaries,
  including formulas and presentation when part of the contract. For fonts,
  readers, or text shaping, preserve glyph coverage, shaping, reading order,
  and native consumers; parsing successfully is not rendering evidence.
- Use synthetic or approved fixtures and temporary outputs for batch tools.
  Preserve subprocess arguments, exit/timeout handling, and atomic writes;
  avoid overwriting source datasets, reports, or original font assets during
  validation. Do not turn a standalone pipeline into a framework project.

## Storage, authentication, and stateful services

- Identify each concrete driver/ORM, engine, migration owner, auth adapter,
  binding and remote API. SQLite files, D1, MySQL, object storage, and durable
  state can share interfaces without sharing transactions or lifecycle.
- Preserve authorization/tenant scoping, constraints, ordering, atomicity,
  retries, idempotency, recovery, and queue/message acknowledgement. Treat
  crypto/wire formats and key ownership as public contracts, not cleanup.
- When extracting shared policy from runtime adapters, run contract fixtures
  against every affected adapter and keep runtime-specific tests. A shared
  mock passing cannot establish both adapters. Do not unify intentional host
  differences or hand-edit generated schemas, protocol vectors, or copied
  shared sources; change their owner and regenerate with existing tools.
- Validate against disposable databases, buckets, queues, and identities.
  Required checks still gate the change; missing live-service evidence is a
  limitation, not permission for migrations, deliveries, or remote mutations.
