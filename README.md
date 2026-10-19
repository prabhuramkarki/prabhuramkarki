<!-- Keep assets/profile beside this file when publishing it as README.md. -->
<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile/hero-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="./assets/profile/hero-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/profile/hero-dark.svg">
  <img src="./assets/profile/hero-light.svg" width="100%" alt="Prabhuram Karki. Full-stack software engineer. Kathmandu, Nepal.">
</picture>

# From the interface to the machinery.

I’m **Prabhuram**, a full-stack software engineer in **Kathmandu, Nepal**. I build web applications with **Vue, Nuxt, Quasar and Laravel**, with attention to the data model, the API and the experience on screen. My side projects take that curiosity further into Linux runtimes and developer tools.

**[Explore my portfolio](https://www.prabhuramkarki.com.np)** · [Email me](mailto:prabhuramkarki07@gmail.com) · [LinkedIn](https://linkedin.com/in/prabhuramkarki)

---

<!-- Work comes before the toolbox. -->
## Selected engineering work

### [ManduCart v2](https://github.com/prabhuramkarki/manducart-v2)

**A storefront and its application backend.** Product browsing, customer accounts and a shopping cart bring the interface and application data into the same workflow.

- **My implementation:** a Vue 3 and TypeScript frontend alongside a Laravel API, with Pinia for application state and Tailwind CSS for styling.
- **Inside the code:** product and cart endpoints, signup/login flows, Sanctum authentication and an admin route guarded by role middleware.

`Vue 3` · `TypeScript` · `Pinia` · `Tailwind CSS` · `Laravel` · `Sanctum`

[Frontend source](https://github.com/prabhuramkarki/manducart-v2/tree/main/manducart-v2-frontend) · [API routes](https://github.com/prabhuramkarki/manducart-v2/blob/main/manducart-v2-backend/routes/api.php)

### [Windows application runtime on Linux](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux)

**Making Windows application environments explicit.** A personal runtime project that brings installation, per-app environments, dependency management and diagnostics behind a CLI, local daemon and GTK client.

- **My implementation:** a Rust workspace around Wine, with an isolated Wine prefix per application and a typed JSON-RPC interface over a local Unix socket.
- **Inside the code:** bubblewrap sandboxing, dependency verification and a documented compatibility matrix that separates tested behavior from intended support.

`Rust` · `Linux` · `Wine` · `JSON-RPC` · `GTK` · `bubblewrap`

<sub>Pre-1.0. Wine is the current execution backend; application compatibility remains limited. The linked validation record documents the evidence and open checks.</sub>

[Architecture and commands](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux#readme) · [Validation record](https://github.com/prabhuramkarki/native-windows-application-runtime-on-linux/blob/main/docs/VALIDATION.md)

### [Code Shell · Rust edition](https://github.com/prabhuramkarki/code-shell-rs)

**A coding agent that lives in the terminal.** A native Rust implementation that brings model streaming, tool calls and code editing into an interactive REPL or a scripted command.

- **My implementation:** separate crates for the agent loop, model providers, developer tools and CLI, built around an asynchronous Tokio engine.
- **Inside the code:** streamed OpenAI/OpenRouter and Anthropic providers, permission checks for writes and commands, diff-based edits and an offline mock provider.

`Rust` · `Tokio` · `SSE` · `CLI` · `Tool calling`

[Source and usage](https://github.com/prabhuramkarki/code-shell-rs#readme)

## How I approach a full stack

| Layer | What I pay attention to |
| :--- | :--- |
| **Interface** | Component boundaries, responsive layouts, SSR where useful and application state that stays understandable. |
| **Application** | REST APIs, authentication, validation, background jobs and business logic with clear ownership. |
| **Data & delivery** | Relational modeling, database choices, deployment environments and useful diagnostics. |
| **The seams** | How a user action reaches the backend, how failures reach the user and how the next developer will change it. |

<details>
<summary>My working principles</summary>

- Give validation, permissions and business rules a clear home.
- Make loading states, errors and recovery part of the interface.
- Prefer code someone can follow over abstractions they must decode.
- Keep experiments honest: document what works, what was tested and what remains open.

</details>

## The toolbox

| Where it fits | Technologies |
| :--- | :--- |
| **Primary web stack** | Vue · Nuxt · Quasar · Laravel · PHP |
| **Interface & state** | TypeScript · JavaScript · Tailwind CSS · Pinia |
| **Also used** | React · Redux · Node.js · Express · React Native |
| **Data & deployment** | MySQL · MongoDB · Firebase · Azure |
| **Everyday tools** | Git · GitHub · Linux |
| **Learning through projects** | Rust · Linux application runtimes · Terminal tooling |

## Following the work

The repositories above are the best starting point for my code, architectural decisions and project limitations. For ongoing work, explore my [public repositories](https://github.com/prabhuramkarki?tab=repositories) and [GitHub contributions](https://github.com/prabhuramkarki#overview).

## Beyond the web stack

I’m learning Rust by building tools I want to use. I’m interested in what happens below a web application: processes, permissions, runtime boundaries and the operating system. I also enjoy experimenting with Arduino and discussing practical open-source ideas.

---

## Have something worth building?

I’m open to **full-stack engineering roles, freelance projects and open-source collaboration**. Tell me about the product, the problem or the part of the system that needs care.

**[prabhuramkarki07@gmail.com](mailto:prabhuramkarki07@gmail.com)**

[Portfolio](https://www.prabhuramkarki.com.np) · [LinkedIn](https://linkedin.com/in/prabhuramkarki) · [GitHub](https://github.com/prabhuramkarki)

<img src="./assets/profile/signature.svg" width="100%" alt="">

<sub>Kathmandu, Nepal · UTC+05:45</sub>
