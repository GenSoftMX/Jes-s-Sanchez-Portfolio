---
id: 0002-base-sitio-astro
title: H1 — Base del sitio y scaffolding en Astro
revision: r1
grade: I2
status: completed
created: 2026-11-19
updated: 2026-11-19
supersedes_revision: null
---

# Intent — Base del sitio y scaffolding en Astro

Revisión vigente: **r1**. Estado: **incomplete**. La creación de esta tarea no autoriza su implementación ni constituye aceptación del resultado.

## Objetivo

Crear una base funcional de Astro y TypeScript que respete el contrato de arquitectura y permita desarrollar después el contenido y las interacciones del portafolio.

## Incluye

- Inicializar el proyecto con Astro, TypeScript y CSS nativo; configurar las dependencias y comandos necesarios para desarrollo y compilación.
- Crear las unidades previstas en el contrato: páginas, layouts, componentes, contenido, estilos, recursos y configuración.
- Preparar las rutas `/` y `/en/`, con idioma declarado y navegación entre versiones.
- Construir una estructura visual común y adaptable a móvil y escritorio, guiada por el diseño compartido: encabezado, navegación, contenido principal y pie.
- Preparar el esquema de proyectos en Markdown y los puntos de organización para contenido bilingüe.
- Incorporar contenido mínimo de base claramente identificable, sin dar por validadas afirmaciones biográficas o de proyectos.
- Documentar cómo instalar dependencias, ejecutar el sitio localmente y generar la versión estática.

## Fuera de alcance

- Cargar y validar todos los textos, casos de estudio, publicaciones y trayectoria: corresponden a H2.
- Implementar la trayectoria interactiva y los detalles completos de proyectos: se abordarán con el contenido en H2.
- Formularios con procesamiento, cuentas, base de datos, integraciones externas, hosting y publicación.
- Cambiar el contrato de arquitectura sin presentar y acordar la necesidad.

## Plan

1. Inicializar Astro y TypeScript y organizar las carpetas según el contrato.
2. Crear la estructura compartida, las rutas por idioma y el esquema de contenido.
3. Verificar compilación, tipos y arquitectura; revisar visualmente la base en escritorio y móvil, incluyendo navegación por teclado.
4. Ejecutar la auditoría independiente aplicable a I2 y presentar el resultado para aceptación humana.

## Criterios observables

| ID | Criterio |
| --- | --- |
| C1 | El proyecto instala sus dependencias y genera una compilación estática sin errores. |
| C2 | `/` y `/en/` se generan con el idioma correcto y permiten navegar entre sí. |
| C3 | La estructura común se adapta a móvil y escritorio; sus enlaces principales son utilizables con teclado. |
| C4 | Las unidades y configuraciones acordadas existen y su organización es coherente con el contrato de arquitectura. |
| C5 | El esquema inicial de proyectos permite validar los campos definidos en H0; el contenido completo queda para H2. |
| C6 | El README explica los comandos de instalación, desarrollo y compilación. |
| C7 | Se presentan los resultados de verificación y de la auditoría independiente antes de solicitar aceptación. |

## Decisiones pendientes no bloqueantes para H1

Exactitud de fechas y textos, enlaces definitivos, tratamiento final del retrato y proveedor de hosting.

## Aceptación humana (D-H)

- Fecha: 2026-11-19
- Autoridad: Usuario
- Decisión: Aceptado (H1 completado). Se autoriza en vía rápida combinada crear e implementar H2 (0003-contenido-y-fidelidad-diseno).
