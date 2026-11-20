---
id: 0005-tema-claro-oscuro-verificacion
task: 0005-tema-claro-oscuro
updated: 2026-11-19
status: accepted
---

# Verificación — H4: Tema claro y oscuro

## Resultado

- `npm run check`: correcto; 11 archivos Astro, 0 errores, 0 advertencias y 0 hints.
- `npm run build`: correcto; se generaron `/` y `/en/`.
- `git diff --check`: correcto; sin errores de whitespace.
- Prueba en navegador: el selector se ofrece en español e inglés, cambia `data-theme`, `aria-pressed`, icono y etiqueta accesible. La preferencia oscura se conservó al recargar y cambiar entre rutas.
- Teclado: `Space` activa el control y alterna el tema. El foco tiene contorno de 3 px; en tema claro usa `#295c92` y en oscuro `#91bee7`.
- Responsive: revisado a 320 px, 390 px y 1280 px. `scrollWidth` coincide con `innerWidth` a 320 px; el encabezado no se desborda. El enlace de LinkedIn se ve en ambos idiomas y apunta a `https://www.linkedin.com/in/jdsanchez94/`.
- Contraste computado en muestras representativas de texto secundario: claro 4.70:1–5.61:1 en fondos relevantes; oscuro 5.10:1–8.59:1. El foco del toggle mide 6.90:1 en claro y 7.77:1 en oscuro. ES/EN da 4.75:1 en claro y 8.19:1 en oscuro; el estado seleccionado da 6.9:1 y 8.05:1, respectivamente.
- El selector ES/EN usa el token secundario en estado normal; el seleccionado mantiene el azul de enlace. El enlace de LinkedIn es visible en ambas rutas, con `target="_blank"` y `rel="noopener noreferrer"`.
- Auditoría independiente: `approved_with_limits`, sin hallazgos abiertos. Ver [auditoria.md](auditoria.md).
- Después de la aceptación, a petición del usuario, se añadió el `meta name="color-scheme"` recomendado por Modern Web Guidance y se aclaró la descripción bilingüe de Enersí sobre backend y soluciones para soporte. `npm run check`, `npm run build` y `git diff --check` volvieron a pasar.

## Límites de evidencia

- El comando de proyecto `python3 .vostok/tools/vostok_cli.py verify` no se pudo ejecutar: `.vostok/tools/vostok_cli.py` no existe en esta copia, aunque `AGENTS.md` lo enumera. Se usaron `astro check`, compilación, revisión visual y auditoría independiente como evidencia disponible.
- Las mediciones de contraste cubren las zonas principales y las superficies identificadas por la auditoría; no representan una auditoría automatizada exhaustiva de cada píxel y estado hover.
- El cambio de enlace de LinkedIn se añadió a petición explícita del usuario como ajuste I1 local, además del alcance I2 de tema.
- El CLI Vostok indicado por `AGENTS.md` no estaba disponible al verificar; su ausencia no bloqueó los checks Astro ni la inspección del navegador.
- La publicación sigue fuera de esta autorización y se mantiene separada de la aceptación del tema.

## Estado

Implementación y verificaciones disponibles completadas, con auditoría `approved_with_limits` y aceptación humana final (`D-H`) recibida el 2026-11-19: «se aprueba y se acepta alcance y desarrollo».
