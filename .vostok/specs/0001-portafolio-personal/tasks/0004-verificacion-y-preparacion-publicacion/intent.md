---
id: 0004-verificacion-y-preparacion-publicacion
title: H3 — Verificación y preparación para publicación
revision: r1
grade: I2
status: incomplete
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — H3: Verificación y preparación para publicación

Revisión vigente: **r1**. Estado: **incomplete**. La creación e implementación fueron autorizadas por el usuario en vía rápida combinada el 2026-11-19.

## Objetivo

Preparar el portafolio para su despliegue y auditoría final mediante la integración de metadatos SEO y sociales enriquecidos, sitemap, robots.txt, accesibilidad con enlace de salto (*skip-link*), y documentación de despliegue agnóstica para proveedores estáticos.

## Incluye

- Creación de `public/robots.txt` para indexación de motores de búsqueda.
- Creación de endpoint estático `src/pages/sitemap.xml.ts` para generar `sitemap.xml` bilingüe con soporte `xhtml:link`.
- Enriquecimiento del `<head>` en `src/layouts/BaseLayout.astro` con canonicals, `hreflang` bilingüe (`es`, `en`, `x-default`), Open Graph completo y Twitter Cards.
- Enlace accesible de salto al contenido principal (`.skip-link` a `#main`) con estilos accesibles de foco.
- Documentación de despliegue estático en `README.md` cubriendo Cloudflare Pages, GitHub Pages, Netlify y Vercel.
- Verificación estricta de compilación y tipos con `npm run check` y `npm run build`.

## Fuera de alcance

- Configuración de registros DNS en el registrador de dominio o publicación efectiva en cuentas personales (reservado como decisión separada).
- Funcionalidades dinámicas de servidor.

## Criterios observables

| ID | Criterio Observable |
| --- | --- |
| C1 | `robots.txt` y `sitemap.xml` se generan correctamente en `dist/`. |
| C2 | `BaseLayout.astro` incluye metaetiquetas canonical, `hreflang` bilingües y tarjetas OpenGraph/Twitter. |
| C3 | Existe un enlace de salto al contenido principal accesible con foco de teclado (`.skip-link`). |
| C4 | `README.md` documenta los comandos y la guía de despliegue para proveedores estáticos. |
| C5 | `npm run check` y `npm run build` terminan con 0 errores, 0 avisos y 0 hints. |
