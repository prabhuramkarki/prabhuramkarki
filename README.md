<h1>
<picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/hero/hero-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/hero/hero-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/hero-dark.svg">
  <img src="assets/hero/hero-light.svg" width="100%" alt="Prabhuram Karki. Full-Stack Software Engineer in Kathmandu, Nepal. Build products. Understand systems.">
</picture>
</h1>

**[Portfolio](https://www.prabhuramkarki.com.np)** &nbsp; / &nbsp; [Selected work](#selected-engineering-work) &nbsp; / &nbsp; [LinkedIn](https://linkedin.com/in/prabhuramkarki) &nbsp; / &nbsp; [Email](mailto:prabhuramkarki07@gmail.com)

I build across the interface, API, and data model, primarily with **Vue, Nuxt, Quasar, and Laravel**. I care about a feature’s whole path: what people experience, the rules behind it, and the code someone will maintain next.

## Selected engineering work

Four public builds, from product interfaces to developer tools and Linux runtimes. Open a card to explore its source.

<p align="center">
<a href="https://github.com/prabhuramkarki/code-shell-rs"><picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/projects/code-shell-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/projects/code-shell-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects/code-shell-dark.svg">
  <img src="assets/projects/code-shell-light.svg" width="48%" alt="Code Shell: a native Rust coding agent. Streaming providers, permission checks, diff-based edits, and a terminal REPL.">
</picture></a>
<a href="https://github.com/prabhuramkarki/easy-invoice"><picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/projects/easy-invoice-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/projects/easy-invoice-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects/easy-invoice-dark.svg">
  <img src="assets/projects/easy-invoice-light.svg" width="48%" alt="Easy Invoice: a React and Django image OCR prototype. Tesseract extracts fields for database records and CSV output.">
</picture></a>
<a href="https://github.com/prabhuramkarki/manducart-v2"><picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/projects/manducart-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/projects/manducart-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects/manducart-dark.svg">
  <img src="assets/projects/manducart-light.svg" width="48%" alt="ManduCart v2: Vue, Pinia, and Laravel storefront prototype with catalog, accounts, and cart operations. Checkout remains unfinished.">
</picture></a>
<a href="https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux"><picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/projects/linux-runtime-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/projects/linux-runtime-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects/linux-runtime-dark.svg">
  <img src="assets/projects/linux-runtime-light.svg" width="48%" alt="Windows application runtime on Linux: an experimental Rust project using Wine, per-app prefixes, and sandbox policies.">
</picture></a>
</p>

[Code Shell](https://github.com/prabhuramkarki/code-shell-rs) · [Easy Invoice](https://github.com/prabhuramkarki/easy-invoice) · [ManduCart v2](https://github.com/prabhuramkarki/manducart-v2) · [Windows runtime](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux)

<details>
<summary>Implementation notes, contributions, and source links</summary>

### [Code Shell](https://github.com/prabhuramkarki/code-shell-rs)

**A coding agent in a native Rust CLI.** Work with a codebase through an interactive terminal or scripted prompts. Four crates separate the agent loop, streaming providers, tools, and CLI; tool calls pass through a permission engine, file edits produce diffs, and the shell tool has a timeout. My contributions include the terminal REPL and command handling.

`Rust` `Tokio` `SSE` `CLI` `LLM tool calling`

[Repository](https://github.com/prabhuramkarki/code-shell-rs) · [Agent loop](https://github.com/prabhuramkarki/code-shell-rs/blob/main/crates/core/src/agent.rs) · [Terminal REPL](https://github.com/prabhuramkarki/code-shell-rs/blob/main/crates/cli/src/repl.rs)

### [Easy Invoice](https://github.com/prabhuramkarki/easy-invoice)

**Reduce manual invoice transcription.** A React upload interface sends an image to Django; Pillow prepares it for Tesseract, regular expressions extract fields, and the backend saves a database record and appends a CSV row. This prototype processes images and retains uploads and extracted data.

`React` `TypeScript` `Django REST Framework` `MySQL` `Tesseract`

[Repository](https://github.com/prabhuramkarki/easy-invoice) · [Upload interface](https://github.com/prabhuramkarki/easy-invoice/blob/main/frontend/src/components/InvoiceForm.tsx) · [Processing pipeline](https://github.com/prabhuramkarki/easy-invoice/blob/main/backend/invoices/views.py)

### [ManduCart v2](https://github.com/prabhuramkarki/manducart-v2)

**Connect a storefront to its product and account data.** A Vue application with Pinia and Tailwind CSS sits over Laravel APIs for products, signup, login, and cart operations. It is an e-commerce prototype; checkout, payments, and complete access controls remain unfinished.

`Vue 3` `TypeScript` `Pinia` `Tailwind CSS` `Laravel` `Sanctum`

[Repository](https://github.com/prabhuramkarki/manducart-v2) · [Storefront](https://github.com/prabhuramkarki/manducart-v2/blob/main/manducart-v2-frontend/src/pages/shop.vue) · [API routes](https://github.com/prabhuramkarki/manducart-v2/blob/main/manducart-v2-backend/routes/api.php)

### [Windows application runtime on Linux](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux)

**Explore the boundary between an application and its host.** A Rust workspace connects a CLI, a local JSON-RPC daemon, and GTK controls, with per-app Wine prefixes, permission policies, and sandboxed execution. **Experimental:** Wine is the only implemented backend, and compatibility evidence is limited.

`Rust` `Linux` `Wine` `GTK 4` `JSON-RPC` `bubblewrap`

[Repository](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux) · [Architecture](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux/blob/main/docs/ARCHITECTURE.md) · [Validation record](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux/blob/main/docs/VALIDATION.md)

</details>

## Public engineering console

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/dashboard/overview-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/dashboard/overview-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/dashboard/overview-dark.svg">
  <img src="assets/dashboard/overview-light.svg" width="100%" alt="Dated public GitHub console: repository, star, original, and featured-project counts, a 30-day public-event plot, and language byte shares. Exact values and definitions are available in the linked snapshot.">
</picture>

A dated view of public GitHub data, refreshed weekly. Events are returned activity, not commit or contribution totals; the feed is capped and may omit activity. Language bytes describe original repositories, excluding this profile, and are not skill ratings.

[Public data snapshot](assets/dashboard/data.json) · [Metric definitions and refresh schedule](docs/dashboard.md) · [GitHub activity](https://github.com/prabhuramkarki?tab=overview)

<details>
<summary>Detailed language, activity, and repository archive charts</summary>

These charts use the same snapshot as the console. The archive counts currently public originals by creation year, including experiments; it is not a count of shipped products.

<picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/dashboard/languages-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/dashboard/languages-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/dashboard/languages-dark.svg">
  <img src="assets/dashboard/languages-light.svg" width="600" alt="Language byte distribution across original public repositories, excluding forks and this profile.">
</picture>

<picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/dashboard/activity-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/dashboard/activity-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/dashboard/activity-dark.svg">
  <img src="assets/dashboard/activity-light.svg" width="600" alt="Returned public GitHub events across 30 dated UTC days. Events may be incomplete and are not commits or contributions.">
</picture>

<picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/dashboard/timeline-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/dashboard/timeline-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/dashboard/timeline-dark.svg">
  <img src="assets/dashboard/timeline-light.svg" width="600" alt="Currently public original repositories by creation year; forks, private, and deleted repositories are excluded.">
</picture>

</details>

## How I build

Start with the user’s task. Make the boundaries clear. Keep a feature understandable from its first interaction to its stored data, and test the behavior those boundaries promise.

<picture>
  <source media="(max-width: 480px) and (prefers-color-scheme: dark)" srcset="assets/architecture/engineering-flow-mobile-dark.svg">
  <source media="(max-width: 480px)" srcset="assets/architecture/engineering-flow-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/architecture/engineering-flow-dark.svg">
  <img src="assets/architecture/engineering-flow-light.svg" width="100%" alt="Illustrative system map: components and state connect through application APIs, validation, and authorization to queues, cache, and databases. Delivery supports all layers. This is a conceptual pattern, not a deployed topology.">
</picture>

| Area | What I pay attention to |
| :--- | :--- |
| Frontend | Component boundaries, responsive layouts, predictable state, useful feedback. |
| Backend | REST APIs, validation, authentication, authorization, business logic, background work. |
| Data and infrastructure | Data models, queries, caching, deployment configuration, performance. |
| End to end | The path from a product decision through architecture, implementation, testing, and delivery. |

## Technology ecosystem

| Role | Tools |
| :--- | :--- |
| Primary | Vue.js, Nuxt.js, Quasar, Laravel, PHP, TypeScript, JavaScript |
| Interface and state | React, Tailwind CSS, Pinia, Redux |
| APIs and services | Node.js, Express, Django REST Framework, REST APIs |
| Data | MySQL, PostgreSQL, MongoDB, Redis |
| Delivery | Linux, Git, Docker, Nginx, GitHub Actions |
| Exploring | Rust, Linux internals, Flutter, React Native, developer tooling |


## Below the interface

I’m interested in the work between layers: turning a document into records, a prompt into a controlled tool call, or a desktop action into a process with explicit permissions. Rust, developer tools, and Linux internals give me different ways to explore those boundaries.

<details>
<summary>Watch the invoice pipeline — a short source-based illustration</summary>

This animation illustrates Easy Invoice’s processing sequence. It is not a recording of the application or an accuracy benchmark. Close this section to hide motion, or [open the static frame](assets/animations/ocr-pipeline-static.png).

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/animations/ocr-pipeline-static.png">
  <img src="assets/animations/ocr-pipeline.gif" width="600" alt="Illustrated pipeline: invoice image, Tesseract OCR, extracted fields, then a saved database record and CSV row.">
</picture>

</details>

## Let’s build something useful

I’m open to full-stack engineering roles, freelance projects, and open-source collaboration. Bring a product to build, a system to improve, or an engineering problem worth investigating.

**[prabhuramkarki07@gmail.com](mailto:prabhuramkarki07@gmail.com)**

[Portfolio](https://www.prabhuramkarki.com.np) &nbsp; / &nbsp; [LinkedIn](https://linkedin.com/in/prabhuramkarki) &nbsp; / &nbsp; [GitHub](https://github.com/prabhuramkarki)

---

Custom artwork and a public-data dashboard, built for this profile. [How it is maintained](docs/design.md).
