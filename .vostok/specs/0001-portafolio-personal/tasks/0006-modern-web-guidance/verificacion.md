---
id: 0006-modern-web-guidance-verificacion
task: 0006-modern-web-guidance
updated: 2026-11-19
status: accepted
---

# Verificación — H5: Modern Web Guidance

## Resultado

- La skill oficial quedó instalada en `.agents/skills/modern-web-guidance/`; el instalador detectó Codex y copió la skill localmente. No se agregó configuración global.
- `npm run check`: 11 archivos Astro, 0 errores, 0 advertencias y 0 hints.
- `npm run build`: correcto; produjo `/`, `/en/` y `/sitemap.xml` como salida estática.
- `git diff --check`: correcto, sin errores de whitespace.
- `legacy-scan . --json`: resultado final 0 en 38 guías/52 reglas deterministas. La cobertura del scanner se limita a aproximadamente 20% del catálogo y no demuestra ausencia de todos los problemas web.
- Navegador: `/` y `/en/` presentan el contenido correcto y etiquetas accesibles localizadas. Revisé 1440×960, 390×844 y 320×780; a 320 px `scrollWidth` coincide con `innerWidth` (320 px). Los cuatro controles del encabezado midieron 44×44 px.
- Teclado: Tab enfoca el enlace de salto; Enter mueve el foco al `main`. El menú móvil expone su estado y cambia la etiqueta accesible a «Cerrar menú» / «Close menu». El diálogo modal abre con nombre accesible y Esc lo cierra devolviendo foco al botón que lo abrió.
- Tema: comprobé el toggle y el restablecimiento a seguir el sistema. Al volver al tema de sistema, el meta queda como `light dark`; el tema computado y el control siguen la preferencia oscura activa.
- Después de la aceptación, corregí el fondo oscuro del menú superior para limitarlo al menú móvil (hasta 760 px); en escritorio oscuro el fondo computado de `#navlinks` es transparente. `npm run build` volvió a completarse y `git diff --check -- src/styles/global.css` no reportó problemas.
- Recursos externos: `meta[name=referrer]` quedó en `strict-origin-when-cross-origin`; las dos conexiones de Google Fonts se anticipan con `preconnect`.
- Guía e interpretación keep/drop: [hallazgos.md](hallazgos.md). Salidas del escaneo: [legacy-scan-initial.json](legacy-scan-initial.json) y [legacy-scan-final.json](legacy-scan-final.json).
- Auditoría independiente I2: `approved_with_limits`, sin hallazgos abiertos. Ver [auditoria.md](auditoria.md).

## Límites

- No se ejecutó lector de pantalla ni análisis automatizado integral de contraste; teclado, nombres accesibles y layout se revisaron en navegador.
- La comprobación en 320 px usó viewport reducido en navegador de escritorio; no es una prueba en dispositivo físico táctil.
- No se aisló en navegador la ejecución sin JavaScript. Por inspección del código, la paleta CSS incluye fallback con `prefers-color-scheme` cuando falta `data-theme`; el botón aparece solo tras el arranque JS, para no mostrar un control inoperable. El script añade persistencia y evita destello al leer la preferencia guardada.
- La revisión de SRI y CSP se limitó al CSS externo de Google Fonts; por su respuesta dinámica no se fijó un hash SRI.
- La instalación npm reportó una alerta de bajo riesgo de Socket para el paquete de skill. No se instaló dependencia de runtime; el CLI se invocó mediante `npx` y la skill contiene el flujo de consulta. El detalle del lock está en `skills-lock.json`.
- La herramienta Vostok enumerada en `AGENTS.md` (`.vostok/tools/vostok_cli.py`) no existe en esta copia; no se ejecutaron `verify`, `arch-check` ni `risk-check`.

## Estado

Implementación, verificaciones y auditoría independiente completadas. El usuario aceptó la entrega (`D-H`) el 2026-11-19: «Sí, acepto la entrega». No se publicó ni desplegó el sitio.
