---
id: 0006-modern-web-guidance
title: H5 — Adopción de Modern Web Guidance
revision: r1
grade: I2
status: complete
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — H5: Adopción de Modern Web Guidance

## Objetivo

Incorporar Modern Web Guidance al flujo de trabajo de este repositorio y aplicar las recomendaciones actuales que sean pertinentes al portafolio, con cambios verificados y compatibles con su arquitectura Astro estática.

## Autorización

El usuario aprobó de forma combinada crear e implementar el alcance H5 el 2026-11-19. La skill se instalará en el repositorio, no en ajustes globales del usuario.
El usuario aceptó la entrega el 2026-11-19.

## Incluye

- Añadir la skill oficial `modern-web-guidance` en `.agents/skills/modern-web-guidance/` para que agentes de trabajo del repositorio puedan buscar y recuperar sus guías.
- Ejecutar el `legacy-scan` oficial y recuperar guías pertinentes a accesibilidad/teclado, CSS adaptable, tipografía, imágenes y rendimiento, diálogos y recursos externos.
- Revisar cada resultado con los criterios oficiales de aplicabilidad y compatibilidad; dejar rastro de hallazgos aplicados y descartados con motivo.
- Aplicar hallazgos demostrables que mejoren este sitio, sin cambiar Astro, TypeScript ni CSS nativo, y sin agregar dependencias de ejecución.
- Mantener el comportamiento estático y bilingüe; usar mejora progresiva y alternativas para funciones recientes.
- Verificar compilación, ambas rutas e interacciones principales en móvil/escritorio y teclado; registrar límites de pruebas y auditoría independiente I2.

## Fuera de alcance

- Instalar plugins en la configuración global de Codex o modificar ajustes del usuario.
- Adoptar de forma indiscriminada las 262 funciones listadas por el repositorio upstream.
- APIs experimentales, Origin Trials, funciones volátiles de un solo motor, modelos locales de IA, servicios externos o dependencias de runtime.
- Reestructurar contenido o diseño sin un hallazgo que lo justifique; cambios a otros repositorios; publicación del sitio.

## Criterios observables

| ID | Criterio |
| --- | --- |
| C1 | La skill oficial queda en `.agents/skills/modern-web-guidance/` y apunta al CLI y las guías upstream actuales. |
| C2 | Se conserva la salida del escaneo y una tabla keep/drop para hallazgos pertinentes, con motivo y fuente de guía. |
| C3 | Los hallazgos aplicados tienen evidencia en el código o navegador y no añaden dependencias de ejecución ni APIs excluidas. |
| C4 | El sitio sigue generando `/` y `/en/`; `npm run check` y `npm run build` pasan y se revisa el navegador en móvil/escritorio, tema y teclado. |
| C5 | La auditoría independiente I2 queda registrada antes de solicitar aceptación humana final. |

## Límite de entrega

Esta autorización no incluye publicación. La aceptación del resultado y la autorización de despliegue son decisiones separadas.
