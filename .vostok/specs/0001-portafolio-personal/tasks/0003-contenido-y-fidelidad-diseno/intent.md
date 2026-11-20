---
id: 0003-contenido-y-fidelidad-diseno
title: H2 — Contenido, fidelidad visual e interactividad acordada
revision: r1
grade: I2
status: completed
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — H2: Fidelidad total al diseño de referencia

Revisión vigente: **r1**. Estado: **incomplete**. La creación e implementación fueron autorizadas por el usuario en vía rápida combinada el 2026-11-19.

## Objetivo

Implementar en Astro la totalidad visual, de contenido e interactividad del diseño de referencia interactivo (`portafolio_jesus_sanchez_interactivo_actualizado.html`), manteniendo la arquitectura estática modular y la estructura bilingüe (`/` y `/en/`).

## Incluye

- Integración de fuentes *DM Sans* y *Manrope*, variables de diseño, espaciados y reglas responsivas del diseño de referencia.
- Integración y optimización del retrato fotográfico real del usuario (`portrait.webp`) en el Hero.
- Sección de Hero bilingüe con llamada a la acción y barra de 4 especialidades.
- Sección de proyectos con 4 tarjetas, tags de tecnologías, enlace a investigación técnica y diálogo modal accesible (`<dialog>`) para casos de estudio con soporte de teclado (Escape, enfoque).
- Sección de trayectoria interactiva con selector de roles y panel dinámico de detalle (resumen, viñetas de logros, nota contextual y tags).
- Sección de publicación técnica (paper Vostok) con portada gráfica, enlaces DOI a Zenodo y llamada a lectura.
- Sección de habilidades (4 pilares técnicos) y sección "Sobre mí" con cita, biografía bilingüe y formación académica.
- Sección de contacto con botón funcional para copiar correo (`isc.sanchez.94@gmail.com`) con confirmación temporal ("¡Correo copiado!") y enlaces de redes.
- Navegación superior con selector de idioma sincronizado con Astro, menú móvil desplegable y barra de progreso de scroll.
- Validación estricta con TypeScript (`npm run check`) y generación estática (`npm run build`).

## Fuera de alcance

- Panel de administración, blog dinámico, formularios con backend y base de datos.
- Despliegue en producción y configuración de DNS (reservado para H3).

## Criterios observables

| ID | Criterio |
| --- | --- |
| C1 | Las 7 secciones reproducen la fidelidad visual, tipografía y paleta del diseño de referencia. |
| C2 | El retrato fotográfico real del usuario está integrado y se adapta a pantallas de escritorio y móviles. |
| C3 | La trayectoria interactiva permite cambiar entre roles y actualiza el panel de experiencia. |
| C4 | El modal `<dialog>` de proyectos abre y cierra de manera accesible mediante botón y tecla Escape. |
| C5 | El botón de copiar correo transfiere la dirección al portapapeles y emite confirmación visual temporal. |
| C6 | El menú móvil y el selector de idioma operan limpiamente; `npm run check` y `npm run build` terminan con 0 errores. |

## Aceptación humana (D-H)

- Fecha: 2026-11-19
- Autoridad: Usuario
- Decisión: Aceptado (H2 completado). La totalidad visual, de contenido bilingüe y de interactividad acordada fue verificada y aceptada formalmente.
