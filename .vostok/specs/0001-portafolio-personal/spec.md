---
id: 0001-portafolio-personal
title: Portafolio personal de Jesús Sánchez
status: incomplete
created: 2026-11-19
---

# Portafolio personal

## Objetivo

Crear un portafolio que presente a Jesús Sánchez, su forma de trabajar y sus proyectos de forma clara, accesible y fácil de mantener. La audiencia prevista incluye posibles colaboradores, clientes y empleadores; es una hipótesis por validar.

## Punto de partida

El README presenta el perfil y los proyectos JIntent y Vostok IA Workflow. El repositorio aún no contiene una aplicación web ni una arquitectura de producto formalizada. El diagnóstico inicial es **arquitectura no identificada**; no se observó contradicción entre el propósito documentado y el código existente. El diseño de referencia aportado por el usuario es `/Users/jesus/Downloads/portafolio_jesus_sanchez_interactivo_actualizado.html`; es un archivo externo al repositorio, no un artefacto del producto.

## Alcance

- Sitio adaptable a móvil y escritorio, en español e inglés, basado en la dirección visual y la organización general del diseño de referencia.
- Página principal con presentación, proyectos, trayectoria, publicaciones, habilidades, información personal y contacto.
- Menú móvil, selector de idioma, trayectoria interactiva y detalles de proyectos, conforme al diseño y sujetos a revisión de accesibilidad.
- Selector bilingüe de tema claro/oscuro; la preferencia inicial sigue el sistema y una elección manual se recuerda en el navegador.
- Textos, proyectos, trayectoria, publicaciones e imágenes organizados para facilitar su actualización. Proyectos en Markdown.
- Metadatos básicos para buscadores y para compartir enlaces.
- Preparación para publicación estática en el dominio del usuario.

## Fuera de alcance inicial

Blog, panel de administración, base de datos, cuentas de usuario, procesamiento de formularios, integración con redes sociales y publicación efectiva del sitio. Agregar cualquiera requiere acordar su alcance.

## Hitos

| Hito | Resultado esperado |
| --- | --- |
| H0 — Arquitectura y contratos | Decisiones técnicas, estructura, límites y criterios de calidad documentados. |
| H1 — Base del sitio | Proyecto Astro organizado, navegación y estructura visual común. |
| H2 — Contenido y proyectos | Secciones y contenido bilingüe revisables, incluidas las interacciones acordadas. |
| H3 — Verificación y preparación | Revisión de compilación, accesibilidad y presentación en móvil y escritorio; preparación para publicar. |
| H4 — Preferencia visual | Selector claro/oscuro accesible, con preferencia del sistema y elección manual persistida. |
| H5 — Prácticas web modernas | Modern Web Guidance disponible para el repo y recomendaciones pertinentes aplicadas con evidencia. |

## Criterios de aceptación del producto

- El sitio presenta el perfil, proyectos y secciones acordadas en español e inglés.
- Se puede navegar en móvil y escritorio y con teclado; se revisan las interacciones y el cambio de idioma.
- El tema se adapta a la preferencia del sistema, permite elegir claro u oscuro y conserva la elección entre visitas y rutas de idioma.
- Se revisan recomendaciones web modernas pertinentes al sitio y se aplican solo hallazgos confirmados, manteniendo su generación estática y compatibilidad progresiva.
- El contenido se puede mantener desde el repositorio y la compilación termina correctamente.
- Las afirmaciones biográficas, fechas, enlaces y estados de proyectos se revisan antes de publicar.
- La aceptación del resultado y la autorización para publicar son decisiones separadas.

## Decisiones y dudas pendientes

- Validar fechas profesionales, afirmaciones y medios de contacto antes de publicar.
- Resolver la diferencia entre el diseño, que describe la implementación de Vostok como privada, y el README, que enlaza a un repositorio; no asumir que son el mismo repositorio.
- Decidir si hace falta un control de cambio de retrato y definir el tratamiento de la imagen; el HTML revisado no contiene un control funcional de carga.
- Elegir proveedor de hosting tras conocer la administración actual del dominio.

## Decisión técnica aceptada

El usuario aceptó Astro, TypeScript y CSS nativo, con generación estática y contenido de proyectos en Markdown. El 2026-11-19 autorizó el alcance y el desarrollo del tema claro/oscuro como extensión de esta especificación; la decisión de preferencia del sistema queda registrada en la tarea 0005.
