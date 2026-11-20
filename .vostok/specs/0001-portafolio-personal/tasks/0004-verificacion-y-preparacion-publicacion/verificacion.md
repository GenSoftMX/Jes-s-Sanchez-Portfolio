# Verificación de H3 — revisión r1

Fecha: 2026-11-19. Grado: I2. Esta verificación no acepta el resultado.

## Criterios

| ID | Resultado observado |
| --- | --- |
| C1 | `robots.txt` y `sitemap.xml` se generan correctamente en `dist/`. `robots.txt` permite indexación general y enlaza a `sitemap.xml`. `sitemap.xml` incluye las dos rutas (`/` y `/en/`) con prioridades, marcas temporales y enlaces cruzados `xhtml:link` con `hreflang` y `x-default`. |
| C2 | En `dist/index.html` y `dist/en/index.html` se verificó la presencia de etiquetas `<link rel="canonical">`, `<link rel="alternate" hreflang="...">`, metadatos Open Graph (`og:site_name`, `og:title`, `og:description`, `og:image`, `og:url`, `og:locale`, `og:locale:alternate`) y Twitter Card (`summary_large_image`). |
| C3 | Se implementó el enlace de salto accesible `<a class="skip-link" href="#main">` con estilos `:focus-visible` visibles en `src/styles/global.css` que llevan directamente al contenedor principal. |
| C4 | `README.md` documenta los comandos de desarrollo y la guía completa de despliegue estático para Cloudflare Pages, GitHub Pages, Vercel y Netlify. |
| C5 | `npm run check` completó con 0 errores, 0 avisos y 0 hints en 11 archivos. `npm run build` generó exitosamente todas las rutas estáticas (`/`, `/en/`, `/sitemap.xml`, `/robots.txt`) con 0 advertencias. |

## Comandos

| Comando | Resultado |
| --- | --- |
| `npm run check` | Ejecutado con `ASTRO_TELEMETRY_DISABLED=1`. 0 errores, 0 avisos, 0 hints. |
| `npm run build` | Ejecutado con `ASTRO_TELEMETRY_DISABLED=1`. Compilación estática limpia en `dist/` con 0 warnings. |
| Verificación de activos | Verificada la existencia y validez de `dist/robots.txt`, `dist/sitemap.xml`, `dist/portrait.webp` y metaetiquetas en los HTML generados. |

## Límites

- La publicación y configuración de dominios/DNS en el registrador de dominio se mantienen como decisión y acción separadas.
