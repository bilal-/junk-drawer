# Checks for the stack in scope

Read the common checks and only the sections for the targets being reviewed.
These are prompts to investigate, not automatic findings or migration rules.
Use the project's installed versions, supported platforms, architecture, and
commands. Verify version-sensitive advice against authoritative documentation.

## Common checks: any language or backend

- Trace entry points, callers, and dependencies across package boundaries.
  Before deleting or renaming, inspect configuration, reflection, generated
  registries, templates, plugins, and external consumers. No textual caller
  does not establish that something is dead.
- Preserve public contracts, serialization, error behaviour, side-effect
  order, resource ownership, cancellation, and transaction boundaries. A
  shorter async wrapper can change rejection into a synchronous throw;
  parallelizing operations can change order and failure handling. Prove those
  semantics rather than treating such edits as mechanical.
- Reuse helpers only after comparing edge cases and contracts. Consolidate
  knowledge that changes together; keep intentional platform or domain
  differences. Removing an adapter must not lose a test seam or compatibility
  guarantee. Independent flags are not necessarily a mutually exclusive enum.
- Keep a test at the boundary whose contract matters. When the suspected
  defect is in a database, native module, network adapter, or runtime binding,
  a mock of that dependency cannot establish the real integration's behaviour.
- Check schema and API consumers together. Do not change persisted formats,
  schemas, or dependency versions as a side effect of restructuring code.

## React websites

- Before extracting components or hooks, identify who owns state and effects.
  Preserve component identity and keys, state reset behaviour, subscription
  cleanup, effect dependencies, and async cancellation. A hook that just adds
  another pass-through interface needs a concrete benefit.
- Check user interactions and semantic output, including focus and
  accessibility, where the extraction affects them. A snapshot alone cannot
  establish that a form still submits or a dialog returns focus correctly.
- Validate with the affected package's type/build checks and existing
  component or browser tests as appropriate. For performance changes, measure
  the affected interaction; do not apply blanket memoization or compiler
  advice without checking the project's React version and configuration.

## React Native, including Expo

Apply the React checks, then inspect the JavaScript/native boundary.

- Look for `.ios`, `.android`, and `.native` implementations, native module
  registration, codegen, autolinking, and Expo config plugins where present.
  A shared contract may need fixes on both platforms without identical code.
- Preserve list keys and item state, navigation and back handling, keyboard
  behaviour, subscriptions, app foreground/background transitions, and any
  animation work crossing JS and UI threads that the change touches.
- JavaScript component tests do not execute the backing iOS/Android code.
  For native integration changes, use the affected platform build and runtime
  checks; for shared changes affecting both platforms, account for both.
  Record missing simulator, emulator, device, or release-build coverage.
- Measure performance on the same interaction and comparable build/device
  before and after. Inspect the installed library version before applying
  advice about lists, Hermes, animation APIs, or the React Native architecture.

## Native iOS: SwiftUI, UIKit, Swift, or Objective-C

- Preserve state ownership and lifetime, dependency injection, view/controller
  lifecycle, task cancellation, actor or thread isolation, and resource
  ownership. For SwiftUI, extraction can change identity, Observation
  dependencies, or when state is initialized. For UIKit, inspect delegates,
  callbacks, and view-controller containment where affected.
- Check the minimum OS target and availability fallbacks before removing old
  paths or adopting an API. Inspect selectors, storyboard references, and
  Objective-C/runtime registration before declaring code unused.
- Use the project's scheme, configuration, and destination for builds/tests.
  Check the affected interaction on a simulator or device when unit tests
  cannot establish its lifecycle or UI behaviour. Preserve the app's chosen
  architecture; a refactor is not permission to switch MVVM, Observation,
  UIKit, or SwiftUI conventions across the project.

## Native Android: Compose, Views, Kotlin, or Java

- Preserve the owner and lifespan of UI state, stable item keys, saved state,
  lifecycle-aware collection, coroutine scopes, cancellation, and effect
  cleanup. Extraction or state hoisting can change behaviour on recomposition,
  navigation, configuration changes, or process recreation.
- Inspect manifest/resource/XML references, reflection, JNI, generated DI,
  and shrinker rules where relevant. A debug build cannot establish that a
  release variant with R8 still finds a reflectively loaded class.
- Use the affected Gradle modules and variants, with the project's local,
  Robolectric, instrumented, or UI tests as needed. Screenshot tests establish
  appearance; interaction and restoration need behavioural checks. Account
  for supported API levels when platform-specific paths change.

## Native macOS apps and helpers

- Identify SwiftPM/Xcode app and helper targets, AppKit/SwiftUI lifecycles,
  IPC, login/background services, and process ownership. Preserve main-thread
  UI work, shutdown, observer cleanup, and user-approved service registration.
- Check the macOS deployment target, sandbox/entitlement assumptions, and
  packaged resource/helper paths where affected. A Swift unit suite does not
  establish signed app, service registration, or notarization behaviour.
- Build/test the affected targets and exercise isolated adapters or app
  fixtures. Defer changes needing unavailable packaging evidence; do not
  register helpers, change power settings, or replace installed apps to test.

## Native mobile libraries and bridges

- Identify the package's public TypeScript, Swift, Kotlin, Objective-C/C++
  contracts and generated bindings. Preserve exports, platform registration,
  ABI/serialization, threading, callbacks, and ownership across the boundary.
- Inspect codegen specs, Expo module configuration, podspec/Gradle metadata,
  and consumer builds. Do not hand-edit generated bridge or prebuild output;
  change the owning source/configuration and regenerate with project tools.
- Validate the packed/built package through representative consumers on the
  affected platforms. Internal source tests alone cannot establish package
  resolution, autolinking, native linkage, or exported contract compatibility.

## Astro and Cloudflare apps

Apply both sets of checks when Astro renders on Workers.

- **Astro:** preserve server/client boundaries, hydration directives, island
  props, routing, and prerender versus on-demand rendering. Moving code into
  a hydrated component can change when it runs and what reaches the browser;
  keep server-only dependencies and secrets out of client bundles.
- **Workers:** inspect the configured compatibility date/flags, bindings, and
  generated types. Preserve request isolation, streaming/backpressure, cache
  semantics, and the lifetime of awaited work or `ctx.waitUntil()` tasks.
  Do not move request-specific state into shared module globals as cleanup.
- Use the project's Astro build/check commands and Workers runtime tests or
  local preview for the affected routes and bindings. Node-only tests cannot
  establish workerd-specific behaviour. Include Durable Objects or other
  stateful bindings when the touched code depends on them.
- Do not advance compatibility dates, replace adapters, deploy, or alter
  remote resources as incidental refactoring. Follow repository account and
  environment routing for any separately authorized remote operation.
