# Project Architecture Contract

- **Architectural style:** Modular content-driven static site (base implemented; full content pending)
- **Detected bootstrap state:** `partially_defined`
- **ADR / Decision link:** Stack decision agreed with user, 2026-11-19; starting point `Initial bootstrap (vostok init)`.

## Scope and Status

This contract describes the portfolio architecture. The base site — routes, common structure, and project schema — is implemented. Full content, trajectory, and publication remain pending. Astro generates static HTML and assets at build time; TypeScript and native CSS organize the code and presentation. No application server or database is required for the initial scope. Content is updated via a rebuild and redeployment. Publication requires separate authorization.

The reference design organizes the site into a bilingual main page featuring an introduction, projects, trajectory, publications, skills, personal profile, and contact. Its visual direction and primary interactions are preserved, subject to accessibility review. Content, veracity, and asset decisions are not considered verified solely by appearing in the design mockup.

## 1. Layers and Modules Catalog

| Unit (Layer / Module) | Kind | Physical Path | Responsibility | Local Contract |
| :--- | :--- | :--- | :--- | :--- |
| `pages` | routes | `src/pages` | Composes pages and per-language metadata. | No access to secrets or server logic. |
| `layouts` | presentation | `src/layouts` | Passive document shell and global HTML elements (`BaseLayout.astro`). | Consumes components and styles; strictly forbidden to mutate section content or inject `innerHTML`. |
| `components` | presentation | `src/components` | High-level section composition (`HomeContent.astro`). | Receives `lang`; delegates to atomic section modules. |
| `components/sections` | presentation | `src/components/sections` | Autonomous page sections (`HeroSection`, `ProjectsSection`, `CareerSection`, etc.). | Encapsulates self-contained markup and progressive enhancement without destroying SSR DOM. |
| `components/ui` | presentation | `src/components/ui` | Reusable UI atoms and interactive controls (`ProjectModal.astro`). | Encapsulates control behavior (e.g. native `<dialog>`); receives explicit typed props. |
| `content` | content | `src/content` | Markdown projects and structured site content. | Data without secrets; content validated at build time. |
| `styles` | presentation | `src/styles` | Semantic design tokens and global styles (`global.css`). | Centralizes light, dark, and no-JS fallback tokens without duplicated component selectors. |
| `assets` | assets | `src/assets` | Images processed by Astro when appropriate. | Authorized publication material only. |
| `public` | assets | `public` | Static public files served directly. | Authorized publication material only. |
| `content-config` | configuration | `src/content-config` | Content collection schemas. | Does not store credentials. |
| `site-config` | configuration | `src/site-config` | Single source of truth for portfolio data (`portfolio.ts`). | Does not store credentials or orphaned duplicate files. |

## 2. Dependency Rules (Verifiable Matrix)

| Source Unit | May Depend On (Allowed) | Must Not Depend On (Forbidden) | Verification Rule |
| :--- | :--- | :--- | :--- |
| `pages` | layouts, components, content, content-config, site-config, assets | content importing pages or secret handling | Review of imports and build output. |
| `layouts` | components, components/ui, styles, site-config, assets | pages, mutating page content via innerHTML, or simulating SPA routing | Review of imports and DOM behavior. |
| `components` | components/sections, styles, assets, site-config | pages, layouts, and direct access to external services | Review of imports. |
| `components/sections` | components/ui, styles, assets, site-config | pages, layouts, and external service mutations | Review of imports. |
| `components/ui` | styles, site-config, assets | pages, layouts, and components/sections | Review of imports. |
| `content` | schema and local content files | pages, layouts, and components | Build-time schema validation and review. |
| `styles` | other stylesheets and visual assets | pages, components, content, and application logic | Review of imports. |
| `content-config` | types and local configuration | pages, layouts, and components | Review of imports. |
| `site-config` | types and local configuration | pages, layouts, and components | Review of imports. |

These rules represent proposed architectural design boundaries; no automated enforcement tool is asserted.

## Content and Languages

- Projects: Local Markdown collection, with schema defined in `src/content-config`. Astro requires `src/content.config.ts` to register the collection; this file enforces the schema without introducing its own fields. Each language has its own entry, linked by a stable project identifier and language code. Thus, each text entry can be updated without relying on browser automated translation.
- Minimum fields per entry: shared identifier, language, title, description, technologies, links, optional images with alt text, and case study body. Status and date are included once verified. Links and assertions must be verified prior to publication.
- Trajectory, publications, skills, and profile: Structured local data per language; each section consumes this data through components. Avoid duplicating content inside interaction logic.
- Proposed routes: `/` for Spanish and `/en/` for English, with equivalent section anchors. The language switcher links to the equivalent version; the document declares its locale, and each route provides its own metadata. Navigation must remain accessible without JavaScript.
- Images: Reviewed and authorized assets; preserve the portrait from the design mockup only after validation. The necessity and behavior of any photo selection control remain pending decision; the reviewed HTML contains no functional upload control.

## Interaction and Accessibility

Essential content and links must be available in the generated HTML. The mobile menu, trajectory selection, and project details may use targeted JavaScript scoped to each function; no additional UI framework is added until a concrete requirement emerges. Detail views may use accessible dialogs with managed focus and keyboard dismissal. Without JavaScript, core details must remain accessible via alternate content or links. Animations respect reduced-motion preferences. Contrast, keyboard navigation, accessible names, states, and mobile viewports are verified during implementation.

## Delivery and Evolution

Static output is generated in `dist/`. The hosting provider and deployment procedure will be finalized once domain management details are established. Analytics, forms with processing, authentication, databases, and dynamic server services remain outside the initial scope; incorporating any requires separate decision and scope. The initial contract definition of `core` in `src` was a generic bootstrap description, replaced here with planned product responsibilities rather than already-implemented modules.

## Exceptions

| ID | From | To | Reason | ADR / Spec | Expires On |
| :--- | :--- | :--- | :--- | :--- | :--- |
