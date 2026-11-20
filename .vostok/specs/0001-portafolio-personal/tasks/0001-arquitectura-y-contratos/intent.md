---
id: 0001-arquitectura-y-contratos
title: H0 — Arquitectura y contratos del portafolio
revision: r1
grade: I2
status: completed
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — Arquitectura y contratos del portafolio

Revisión vigente: **r1**. Estado: **completed**. La creación de esta tarea no autoriza su ejecución ni constituye aceptación del resultado.

## Objetivo

Documentar una base técnica coherente con la spec y el diseño de referencia antes de implementar el sitio.

## Incluye

- Registrar la elección de Astro, TypeScript, CSS nativo, generación estática y Markdown; su justificación y las alternativas consideradas.
- Definir la estructura del repositorio y la separación de páginas, componentes, estilos, contenido e imágenes.
- Definir la organización del contenido bilingüe y de las interacciones del diseño.
- Definir el modelo inicial de proyecto: título, descripción, tecnologías, enlaces, imágenes y contenido del caso de estudio.
- Documentar límites, criterios de calidad y decisiones pendientes para la implementación. Evaluar el contrato de arquitectura del proyecto como resultado de H0.

## Excluye

Implementar o configurar la aplicación, instalar dependencias, publicar el sitio y alterar archivos de producto fuera del resultado de arquitectura acordado. Las tareas posteriores se autorizan por separado.

## Plan

1. Revisar el diseño de referencia y el contexto del repositorio con el detalle necesario.
2. Elaborar el contrato de arquitectura y el modelo de contenido, registrando las decisiones y dudas.
3. Verificar coherencia con la spec, criterios y límites; aplicar la revisión independiente exigida por la política antes de solicitar aceptación humana.

## Criterios

| ID | Condición observable |
| --- | --- |
| C1 | Existe un contrato de arquitectura coherente con la spec que describe estructura, responsabilidades y límites. |
| C2 | Se describe el modelo de proyectos, la organización bilingüe y el tratamiento previsto de las interacciones. |
| C3 | Las decisiones aceptadas, sus razones y las alternativas consideradas están registradas. |
| C4 | Las decisiones que afecten la implementación están identificadas, incluidas las cuestiones de contenido y retrato. |
| C5 | Se presenta la verificación y la auditoría independiente aplicable para revisión humana; la aceptación y el despliegue se mantienen separados. |

## Decisiones registradas

| Decisión | Acuerdo | Razón | Alternativas consideradas | Confirmación |
| --- | --- | --- | --- | --- |
| Stack y generación | Astro, TypeScript y CSS nativo; generación estática y proyectos en Markdown. | Ajuste a un sitio orientado a contenido, con componentes e interactividad puntual. | Next.js y HTML/CSS/JavaScript; respectivamente, mayor alcance de aplicación y mayor trabajo manual de organización a medida que crece el sitio. | Usuario aceptó la dirección técnica en conversación, 2026-11-19. |
| Diseño de referencia | Página principal por secciones, español e inglés y las interacciones principales del HTML compartido. | Refleja la referencia proporcionada y sus necesidades visibles. | La propuesta inicial de rutas separadas y español solamente. | Usuario aceptó el alcance actualizado en conversación, 2026-11-19. |

## Pendientes

Validar fechas, afirmaciones y contactos; aclarar la referencia al repositorio de Vostok; definir el tratamiento del retrato y la elección de hosting. La ejecución de H0 requiere autorización expresa posterior a la creación de estos documentos.
