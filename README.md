# Jesús Sánchez — Personal Portfolio

Professional web portfolio of Jesús Sánchez (Mobile Engineer & AI Engineering), built with [Astro](https://astro.build), TypeScript, and native CSS under a modular content-driven architecture and Vostok workflow.

- **Website:** [jesusdonaldosanchezinzunza.com](https://jesusdonaldosanchezinzunza.com)
- **GitHub:** [@GenSoftMX](https://github.com/GenSoftMX)
- **Email:** [isc.sanchez.94@gmail.com](mailto:isc.sanchez.94@gmail.com)

---

## Features

- **High-fidelity and responsive design:** 7 structured sections (`#inicio`, `#proyectos`, `#trayectoria`, `#investigacion`, `#habilidades`, `#sobre-mi`, `#contacto`), adaptable across mobile, tablet, and desktop viewports.
- **Native bilingual support:** Full static routes in Spanish (`/`) and English (`/en/`), with canonical links and `hreflang` tags.
- **Accessibility and performance:** Accessible modal dialog (`<dialog>`) with keyboard navigation (Escape key, focus trap/management), skip link, `prefers-reduced-motion` compliance, and high-performance static output.
- **SEO & Indexing:** Open Graph metadata, Twitter Cards, `robots.txt`, and static generation of `sitemap.xml`.
- **Decoupled architecture:** Strict layer separation (`pages`, `layouts`, `components`, `styles`, `site-config`, `public`) complying with the project architecture contract.

---

## Development Commands

Prerequisites: Node.js (v18+) and npm:

```sh
# Install dependencies
npm install

# Start local development server
npm run dev

# Strict type and component checking
npm run check

# Build static site for production (outputs to dist/)
npm run build

# Preview static build locally
npm run preview
```

> **Note for strict sandbox environments:**  
> If executing in environments where user system directory access is restricted, you can run `ASTRO_TELEMETRY_DISABLED=1 npm run check` or `build`.

---

## Static Deployment Guide

The `npm run build` command generates a 100% static build in the `dist/` directory. No runtime Node.js server is required.

### 1. Cloudflare Pages
- **Build command:** `npm run build`
- **Build output directory:** `dist`
- **Node.js version:** `20` (or higher via environment variable `NODE_VERSION=20`).

### 2. GitHub Pages
- The automated pipeline is configured in `.github/workflows/deploy.yml` using the official `withastro/action`.
- **GitHub Configuration:**
  1. Go to your GitHub repository and navigate to **Settings** > **Pages**.
  2. Under **Build and deployment** > **Source**, select **GitHub Actions** (instead of *Deploy from a branch*).
  3. When using a custom domain, set `jesusdonaldosanchezinzunza.com` in **Custom domain** (the `public/CNAME` file preserves the domain on each deployment).
- Pushing to the `main` branch or manually triggering the workflow from the **Actions** tab will automatically build and deploy the site.

### 3. Vercel
- **Framework Preset:** Astro
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### 4. Netlify
- **Build command:** `npm run build`
- **Publish directory:** `dist`

---

## Project Structure

```text
├── public/                 # Static public assets (favicon, portrait, robots.txt)
├── src/
│   ├── components/         # Decoupled visual sections (HomeContent.astro)
│   ├── layouts/            # Document shell, layout, and modals (BaseLayout.astro)
│   ├── pages/              # Static routes (/index.astro, /en/index.astro, /sitemap.xml.ts)
│   ├── site-config/        # Type contracts and bilingual site data (portfolio.ts)
│   └── styles/             # Design tokens and global stylesheets (global.css)
└── .vostok/                # Specifications, architecture contracts, and policies
```
