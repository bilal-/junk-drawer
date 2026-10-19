# Hot-path discovery

Read this when scope includes UI rendering, scrolling, request handling, or another frequently repeated operation, regardless of whether the requested focus is bugs or refactoring. This is a search guide, not a mandate to add caches or dependencies. Keep the structural review required by `refactor` and `both` alongside it.

## Trace the repeated work

Pick representative interactions and follow the call path, including computed properties and helpers. Ask what runs per frame, list row, recomposition, appearance, keystroke, or request; how often it runs; and whether cost grows with data size. Inspect both platforms when they implement the same operation. Include failure paths: a missing resource can be retried more often than a successful load.

Look for repeated hashing or crypto, file and bundle access, parsing, formatting, regex compilation, font or image creation, full-size decoding for small displays, sorting or flattening collections, and linear lookup by key. Check whether a cache is large enough for the working set, stores failures appropriately, and lives as long as the data it caches. A `remember`ed object or view-local cache may still be recreated for each row. Consider an index, precomputed value, correctly owned cache, or a simpler data flow only after identifying the work and its lifetime. Preserve invalidation, identity, memory bounds, concurrency, and error behaviour.

Framework prompts, applied to installed versions and actual usage:

- **SwiftUI:** inspect work reached from `body`, row builders, `onAppear`, and image loaders. Check stable identity and where state or cached resources live. Confirm images decode near display size when that affects cost.
- **Compose:** inspect composables, lazy item builders, effects, and work reached during recomposition. Check `remember` scope, stable keys, derived state, and whether expensive resources are built for each item.
- **React:** inspect render functions, list rows, selectors, and effect retries. Check render purity, stable keys, and the actual benefit and lifetime of memoization.
- **Request-serving code:** inspect per-request parsing, loading, serialization, repeated database or remote lookups, and work multiplied by fan-out. Account for cache isolation and invalidation.

## Establish impact before changing performance code

Discovery does not require a profiler before a candidate enters the ledger. Record the reachable path and why it repeats. Before keeping a performance change, establish a repeatable baseline and compare the same interaction, data set, build, and device or runtime after the change. Use a profiler or counters to attribute cost when possible; record latency, frame timing, allocations, decode count, or call count relevant to the finding. Correctness and lifecycle checks still apply. If a realistic target is unavailable, report the candidate and defer changes whose benefit or safety cannot be verified. Do not treat software-rendered emulator frame times as device performance.

## Assets and infrastructure

Inspect unusually large bundled assets used in hot paths. Confirm actual use and any smaller equivalent already present or documented before replacing an asset; check rendering and licensing constraints. If hand-built loading or caching infrastructure creates the problem and a maintained library is a plausible replacement, record the library as an option with its payoff and migration cost. Do not add or upgrade dependencies without authorization. Look for an in-scope local fix when one can be measured and verified.
