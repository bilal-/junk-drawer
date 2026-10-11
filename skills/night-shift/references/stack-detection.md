# Detect the project before selecting checks

Classify each runnable app, library, service, or tool in scope, including
nested packages. Record three things separately: **framework/language**,
**execution host**, and **data/services**. Next.js on a Node server and Next.js
on Workers need different runtime checks. A mixed repository can need several
rows below. These are starting points, not an exhaustive supported-stack list.

Use manifests and lockfiles, source entry points, build/deploy configuration,
and project instructions together. Read configuration as data; do not execute
setup, deploy, migrations, or live integrations to identify a stack.

## Detection cues and routing

Always apply the [common checks](stack-checks.md#common-checks-any-language-or-backend).

| Target | Corroborating evidence | Additional checks |
| --- | --- | --- |
| React browser app | `react-dom`, browser entry and components; Vite or another bundler configuration | [React](stack-checks.md#react-websites) |
| Next.js | `next` dependency, `next.config.*`, and `app/` or `pages/` routing; inspect output mode, server entry, and actual deployment | [Next.js](service-and-tool-checks.md#nextjs-server-rendered-web-apps), plus the host's checks |
| React Native / Expo | `react-native` or `expo`, app config, Metro, native projects or prebuild configuration | [React Native](stack-checks.md#react-native-including-expo) |
| Native iOS | Xcode targets/build settings, iOS deployment target, Swift/Objective-C source; SwiftPM can also contain libraries | [iOS](stack-checks.md#native-ios-swiftui-uikit-swift-or-objective-c) |
| Native macOS | macOS platform/targets, AppKit/SwiftUI imports, app/helper targets and service configuration | [macOS](stack-checks.md#native-macos-apps-and-helpers) |
| Native Android | Android Gradle plugins, manifest, Kotlin/Java, Compose or XML layouts | [Android](stack-checks.md#native-android-compose-views-kotlin-or-java) |
| Native mobile library | `.podspec`, `codegenConfig`, `expo-module.config.json`, exported native contracts, Objective-C++/C++ or JNI bridges | [Native libraries](stack-checks.md#native-mobile-libraries-and-bridges), plus affected platforms |
| Astro | `astro` dependency, `astro.config.*`, `.astro` routes and integration/adapter configuration | [Astro](stack-checks.md#astro-and-cloudflare-apps) |
| Cloudflare runtime | Wrangler entry/configuration or adapter and deployment scripts targeting Workers; record compatibility settings and binding kinds | [Workers](stack-checks.md#astro-and-cloudflare-apps) and [stateful services](service-and-tool-checks.md#storage-authentication-and-stateful-services) |
| Node.js CLI or service | Runnable Node entry/shebang, start/build scripts, runtime version, Node built-ins or server/socket entry points | [Node and containers](service-and-tool-checks.md#nodejs-services-clis-and-containers) |
| Google Apps Script | `appsscript.json`, `.gs` entry points, `.clasp.json`, Apps Script services or `google.script.run` in HTML clients | [Apps Script](service-and-tool-checks.md#google-apps-script) |
| PHP web app | PHP entry points, `composer.json`/lock, `phpunit.xml`, HTTP/session/database code; framework may be absent | [PHP](service-and-tool-checks.md#php-web-apps) |
| Go CLI or service | `go.mod`/`go.work`, `cmd/` or `main` package, build/test targets | [Go](service-and-tool-checks.md#go-tools-and-services) |
| Shell CLI / installer | Executable scripts and shebangs, sourced libraries, shell tests, installer or packaging entry points | [Shell](service-and-tool-checks.md#shell-tools-and-installers) |
| Python or JS data pipeline | Script/CLI entry points and actual imports, with `pyproject.toml`, requirements, or package metadata where present; document/font/data transformations | [Pipelines](service-and-tool-checks.md#python-and-javascript-data-content-and-font-pipelines) |
| Database, auth, queue, or protocol | ORM/schema/migration files, driver imports, binding kinds, auth middleware, socket handlers, schemas and shared contract fixtures | [Stateful services](service-and-tool-checks.md#storage-authentication-and-stateful-services), in addition to the host/framework |

## Avoid false detection

- Deduplicate Git worktrees and review clones when inventorying projects.
  Dependencies, generated consumers, SDK checkouts, test fixtures, archives,
  and build outputs are not independent first-party stacks. Inspect them only
  when they are themselves in scope or establish a consumer contract.
- A `package.json` can contain only test or deployment tooling. Node tests or
  `clasp` do not make an Apps Script app a Node production service. A Gemfile
  for Fastlane or a Ruby Homebrew formula does not establish a Rails app.
- `wrangler` can upload static assets or serve a separate Worker next to a
  Node app. Follow each deployed entry instead of labeling the whole repo
  Workers-only. A Dockerfile is a host/packaging target, not a web framework.
- A React peer dependency can belong to a native library; SwiftPM can target
  macOS rather than iOS. Source suffixes alone do not determine the product.
- If manifests are missing, inspect script imports, entry points, instructions,
  and CI before concluding that no stack exists. Record uncertainty explicitly.
- For an unlisted stack, derive ownership, contracts, lifecycle, and required
  validation from its own tooling and current authoritative documentation.
  Do not force it into the nearest familiar framework or migrate it to one.
