# Verificación de H2 — revisión r1

Fecha: 2026-11-19. Grado: I2. Esta verificación no acepta el resultado.

## Criterios

| ID | Resultado observado |
| --- | --- |
| C1 | Las 7 secciones (`#inicio`, `#proyectos`, `#trayectoria`, `#investigacion`, `#habilidades`, `#sobre-mi`, `#contacto`) están generadas en el HTML estático con la estructura, clases, tipografía (*Manrope* y *DM Sans*) y variables visuales del diseño de referencia interactivo. |
| C2 | Se extrajo el retrato fotográfico real del usuario (`public/portrait.webp`, 93.5 KB) y se integró en el hero con estilos de centrado (`object-position: center 33%`), adaptabilidad en escritorio y móvil, y soporte para pantallas reducidas. |
| C3 | La trayectoria cuenta con las 7 posiciones completas estructuradas en `src/site-config/portfolio.ts` (Enersí, Wadi, HLC, Sam's Club, Ucall, Coppel A/D). `renderTimeline()` inyecta los selectores y el panel reactivo con viñetas, notas contextuales y tags. |
| C4 | Se implementó el modal `<dialog id="projectModal">` nativo accesible para los 4 proyectos (Vostok, JIntent, Support Triage AI, Lakam Flow), con títulos, problema, enfoque, estado, enlaces y gestión de foco accesible (retorno a `previousFocus`). |
| C5 | El botón `#copyEmail` transfiere `isc.sanchez.94@gmail.com` al portapapeles con `navigator.clipboard.writeText` (y respaldo textarea), alternando el texto a "¡Correo copiado!" / "Email copied!" durante 2.5 segundos. |
| C6 | El menú móvil tipo drawer `#menuBtn` conmuta `#navlinks.open` y sincroniza `aria-expanded`. El selector de idioma enlaza `/` y `/en/` con actualización reactiva en cliente. `npm run check` reportó 0 errores, 0 avisos y 0 hints; `npm run build` generó exitosamente `dist/index.html` y `dist/en/index.html`. |

## Comandos

| Comando | Resultado |
| --- | --- |
| `npm run check` | Ejecutado con `ASTRO_TELEMETRY_DISABLED=1`. 0 errores, 0 avisos, 0 hints en 10 archivos. |
| `npm run build` | Ejecutado con `ASTRO_TELEMETRY_DISABLED=1`. Compilación estática exitosa en `dist/` (2 páginas, `dist/portrait.webp` presente). |
| Inspección de `dist/` | Verificados `dist/index.html` (`lang="es"`, 37.8 KB) y `dist/en/index.html` (`lang="en"`, 37.4 KB), sin valores `undefined` y con las 7 secciones presentes. |

## Límites

- La publicación y configuración de dominios/DNS quedan delimitadas para H3.
- Las afirmaciones biográficas y fechas en la trayectoria provienen íntegramente de la referencia aprobada por el usuario.
