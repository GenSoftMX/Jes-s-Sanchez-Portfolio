---
id: 0005-tema-claro-oscuro
title: H4 — Tema claro y oscuro
revision: r1
grade: I2
status: complete
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — H4: Tema claro y oscuro

Revisión vigente: **r1**. Estado: **complete**. La creación y la implementación fueron autorizadas de forma combinada por el usuario el 2026-11-19; el usuario aceptó la entrega el 2026-11-19.

## Objetivo

Permitir que cada visitante use el portafolio en tema claro u oscuro, con una primera visita que respete la preferencia del sistema y una selección manual que se recuerde en visitas posteriores.

## Incluye

- Selector accesible en el encabezado, disponible en las rutas española (`/`) e inglesa (`/en/`) y en escritorio y móvil.
- Modo inicial derivado de `prefers-color-scheme` si no hay una elección guardada; en ausencia de esa API, usar tema claro.
- Guardar la selección manual en `localStorage` para reutilizarla al recargar y al cambiar de idioma.
- Aplicar el tema antes del primer pintado para evitar que se vea brevemente el tema incorrecto.
- Adaptar fondos, texto, bordes, controles, tarjetas, trayectoria, publicación, contacto, pie y diálogo de proyectos; actualizar `meta[name="theme-color"]`.
- Etiqueta accesible bilingüe, estado `aria-pressed`, operación con teclado y conservación del foco visible y movimiento reducido.
- Verificación de contraste de texto normal (4.5:1), texto grande y controles (3:1) en ambos temas.

## Fuera de alcance

- Sincronización entre dispositivos o almacenamiento en servidor/cuenta.
- Temas adicionales, cambios de tipografía, reorganización del contenido o rediseño de secciones.
- Dependencias nuevas.

## Criterios observables

| ID | Criterio |
| --- | --- |
| C1 | El selector aparece en ambas rutas, presenta una etiqueta accesible en el idioma actual y se opera por teclado. |
| C2 | Sin elección guardada, el primer render usa la preferencia del sistema (o claro como fallback); una elección guardada prevalece sin destello inicial. |
| C3 | El selector cambia inmediatamente el tema, actualiza `aria-pressed` y `theme-color`, y persiste tras recarga y cambio de ruta/idioma. |
| C4 | Las superficies enumeradas en «Incluye» se distinguen en ambos temas; el contraste cumple los mínimos indicados y el foco sigue visible. |
| C5 | `npm run check` y `npm run build` finalizan correctamente; las rutas y el selector se revisan en móvil y escritorio. |

## Decisión de diseño aprobada

Opción A — preferencia del sistema como valor inicial, con cambio manual persistido localmente. El usuario aprobó el alcance y el desarrollo combinados el 2026-11-19; la comparación y el motivo quedan registrados en `decision-brief.md`.
