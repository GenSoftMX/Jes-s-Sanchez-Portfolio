# Hallazgos — H5 Modern Web Guidance

## Decisiones keep/drop

| Guía / hallazgo | Decisión | Evidencia y razón |
| --- | --- | --- |
| `dark-mode-toggle` / `dark-mode` | Keep y aplicado | El escaneo reportó ausencia de sincronización con `color-scheme`. El tag estático `light dark` ya existía, así que era falsa la parte que afirmaba que faltaba el tag; sí faltaba sincronizar dinámicamente las preferencias. Esa sincronización se corrigió: el control refleja override o valor del sistema en meta y CSS, permite volver a seguir el sistema y escucha cambios entre pestañas. Sin JavaScript, `prefers-color-scheme` aplica la paleta oscura sin quitar contenido y el toggle queda oculto para no mostrar una acción inoperable. |
| `accessibility` | Keep y aplicado | El enlace de salto lleva el foco al `main` programáticamente enfocable. Se conservaron controles HTML nativos, nombres bilingües para navegación/idioma/menú/diálogo, foco visible y estructura semántica. |
| `form-factor-adaptation` | Keep y aplicado | Se aumentaron a 44×44 px los controles del encabezado y a 44 px la altura de enlaces de navegación; 320 px no produce desplazamiento horizontal. |
| `improve-text-layout-and-legibility` | Keep y aplicado | `text-wrap: balance` se limita a encabezados; `text-wrap: pretty` se limita a textos introductorios. Navegadores sin `pretty` conservan el ajuste normal. |
| `typography` | Keep y aplicado | Los tamaños de fuente CSS se expresan en `rem` con equivalencia visual para la base de 16 px; los tamaños fluidos preservan `clamp()`. Se mantiene `overflow-wrap` para texto y enlaces largos. |
| `visually-stable-font-fallbacks` | Keep y aplicado | `font-size-adjust: from-font` permite que las fuentes de respaldo se aproximen a la x-height de las fuentes web. |
| `dialog` | Keep y aplicado | El diálogo de proyecto ya era `<dialog>` modal; se eliminó el retorno de foco manual que duplicaba el comportamiento del navegador y se añadió contención de scroll y `closedby="any"` como mejora progresiva. |
| `secure-external-subresources` | Keep parcial / drop SRI | Se estableció `strict-origin-when-cross-origin` y preconexión a Google Fonts. No se añadió SRI: el CSS de Google Fonts es una respuesta dinámica sin URL inmutable que permita fijar un digest confiable; tampoco se añadió CSP de servidor porque el sitio es estático y eso ampliaría el alcance. |
| `optimize-image-priority` | Keep, sin cambio | El retrato LCP ya tiene `fetchpriority="high"`, `width` y `height`; no se agregó carga diferida a la imagen principal ni se duplicó la prioridad. |
| `responsive-design` | Drop container queries y unidades nuevas | Las rejillas y breakpoints existentes se adaptan a este sitio. A 320 px no hay overflow; introducir container queries o `dvh` no resuelve un problema observado. |
| `typography` — límite de líneas | Drop límite uniforme de 80ch | La portada es una composición editorial de varias columnas; hay límites locales de ancho de lectura y no se observó desborde. No se cambió el ancho de las secciones completas. |

## Escaneo

- El resultado inicial quedó guardado en [legacy-scan-initial.json](legacy-scan-initial.json). Su único hallazgo se verificó contra el código y la rúbrica `dropWhen`: el meta sí estaba presente. Se conservó el hallazgo funcional real sobre sincronizar cambios entre HTML, CSS y JavaScript.
- Resultado final en [legacy-scan-final.json](legacy-scan-final.json): 0 coincidencias en 38 guías y 52 reglas deterministas, aproximadamente 20% del catálogo. Esto no equivale a una auditoría completa de las 262 funciones upstream.

## Guías recuperadas

`dark-mode-toggle`, `dark-mode`, `accessibility`, `responsive-design`, `form-factor-adaptation`, `optimize-image-priority`, `performance`, `html`, `typography`, `improve-text-layout-and-legibility`, `visually-stable-font-fallbacks`, `natural-interactions`, `secure-external-subresources`, `dialog` y `platform-controls-dismiss-dialog`.

La skill quedó bloqueada al commit upstream `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65` en `skills-lock.json`; se conserva el texto Apache-2.0 en `.agents/skills/modern-web-guidance/LICENSE`.
