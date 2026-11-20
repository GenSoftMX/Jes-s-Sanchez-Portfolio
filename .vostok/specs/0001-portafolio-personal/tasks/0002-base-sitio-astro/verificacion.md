# Verificación de H1 — revisión r1

Fecha: 2026-11-19. Grado: I2. Esta verificación no acepta el resultado.

## Criterios

| ID | Resultado observado |
| --- | --- |
| C1 | `npm run check` terminó con 0 errores, 0 avisos y 0 hints. `npm run build` generó `/` y `/en/` en `dist/`. En `astro check` y en la primera compilación apareció el aviso de que no hay archivos `*.md` en `src/content/projects`. |
| C2 | El HTML generado declara `lang="es"` en `/` y `lang="en"` en `/en/`. En el navegador, activar EN llevó a `http://127.0.0.1:4321/en/` y activar ES volvió a `/`. |
| C3 | A 1280 px de ancho el encabezado queda en una fila (78 px, sin salto de línea) y el inicio usa dos columnas (594 px y 486 px). A 390 px el inicio, los proyectos y el contacto pasan a una columna; la navegación muestra Projects, About y Contact; el documento no desborda en horizontal (`scrollWidth` 390). El enlace Proyectos actualizó la dirección a `/en/#projects`. Los enlaces principales son anclas con `tabIndex` 0. Enter sobre el enlace EN, ya enfocado, cambió de idioma. La tecla Tab enviada por la automatización no movió el foco: ese canal emite un evento de teclado y no recorre el foco del navegador. |
| C4 | Existen `src/pages`, `src/layouts`, `src/components`, `src/content`, `src/styles`, `src/assets`, `public`, `src/content.config.ts` y `src/site.config.ts`. `HomeContent.astro` ya no importa `site.config`; recibe los textos por propiedades. Páginas y layout sí usan esa configuración, como permite el contrato. |
| C5 | El esquema de `projects` declara identificador, idioma, título, descripción, tecnologías, enlaces, imágenes opcionales con texto alternativo, estado y fecha. No hay entradas Markdown; la validación de un caso real queda para H2. |
| C6 | El README documenta `npm install`, `npm run dev`, `npm run check`, `npm run build` y `npm run preview`. |
| C7 | Esta nota registra la verificación. La auditoría independiente se presenta aparte, antes de pedir aceptación. |

## Comandos

| Comando | Resultado |
| --- | --- |
| `npm run check` | Ejecutado. 0 errores. Aviso del cargador: ningún `*.md` en `src/content/projects`. |
| `npm run build` | Ejecutado. Salida estática con `/index.html` y `/en/index.html`. |
| `vostok arch-check --root <repo> --stage verify --json` | Fallido. Dos unidades rechazadas porque su ruta es un archivo, no un directorio: `content-config` (`src/content.config.ts`) y `site-config` (`src/site.config.ts`). `cycles: []`. El grafo de las carpetas quedó vacío (`graph_files_scanned: 0`); las dependencias se revisaron leyendo los imports. |
| `vostok verify --root <repo> --stage verify --current-grade I2 --cmd static_lint_types="npm run check" --json` | Estado `failed`. Tipos ejecutados con salida 0. Secretos ejecutados, sin escalar el grado. Arquitectura fallida por las dos rutas de archivo. Documentación fallida: `AGENTS.md` marcado `needs_review` por el cambio de `src/content.config.ts` y `src/site.config.ts`. Sin pruebas unitarias, de integración ni de extremo a extremo configuradas (`unavailable`). Sin contratos OpenAPI (`unconfigured`). |
| `vostok risk-check --root <repo> --current-grade I2 --json` | Grado mínimo recomendado I2. `escalate_ds: false`. Tres señales de límites de arquitectura, por el contrato, `package.json` y cambios que cruzan varias carpetas. La política pide auditoría independiente y marca la puerta `architecture_change` porque el contrato ya está modificado en el árbol de trabajo. |
| `vostok docs-impact --root <repo> --json` | `AGENTS.md` en `needs_review`. Ese archivo describe el flujo de trabajo, no la configuración del sitio. El README ya cubre los comandos. No se modificó `AGENTS.md` para silenciar el aviso. |

## Revisión en navegador

Servidor ya en marcha en `http://127.0.0.1:4321`. Se recorrió la página en español y en inglés, el cambio de idioma en ambos sentidos y el ancla de proyectos. La captura del escritorio salió a 681 px de ancho, así que la columna derecha no entró en la imagen; las medidas a 1280 px sí confirman las dos columnas y la navegación en la misma fila. La captura a 390 px muestra el encabezado, el texto en inglés y, al desplazar, las especialidades en dos columnas y la sección de proyectos.

La barra de desarrollo de Astro informó que no detectó problemas de accesibilidad o rendimiento en esa página. Esa revisión es la de la herramienta de desarrollo, no una auditoría completa.

## Límites

- El comprobador de arquitectura no acepta las rutas de archivo acordadas en H0. Los archivos existen. Cambiar el contrato para convertirlas en carpetas queda fuera de esta tarea.
- La colección de proyectos está vacía a propósito hasta H2.
- No se recorrió con Tab nativo toda la secuencia de enlaces.
- Publicar el sitio no forma parte de esta verificación.
