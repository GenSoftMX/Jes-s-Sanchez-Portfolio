---
id: 0005-tema-claro-oscuro-auditoria
task: 0005-tema-claro-oscuro
updated: 2026-11-19
verdict: approved_with_limits
isolation_mode: separate_agent_or_session
---

# Auditoría independiente — H4: Tema claro y oscuro

## Dictamen

**`approved_with_limits`** — no quedan hallazgos abiertos. La auditoría fue realizada por un subagente separado a partir de los archivos entregados, diff, contrato y resultados de verificación. La remediación corrigió contraste bajo en texto secundario y selector de idioma, foco visible y desbordamiento horizontal del encabezado móvil.

| Eje | Hallazgos abiertos | Evidencia |
| --- | ---: | --- |
| Funcional | 0 | Control bilingüe visible y operable con teclado; alterna `data-theme`, `aria-pressed`, icono y `theme-color`; la selección manual se conserva entre `/` y `/en/`. |
| Arquitectura | 0 | Implementación en el layout compartido y estilos globales; corresponde a las unidades `layouts` y `styles` del contrato. |
| Seguridad | 0 | Solo se aceptan los valores `light` y `dark`; LinkedIn abre con `rel="noopener noreferrer"`. |
| Verificación | 0 | `npm run check` y `npm run build`: 0 errores, advertencias o hints; rutas `/`, `/en/` y `sitemap.xml`. A 320 px `scrollWidth` es 320 px. |
| Riesgos residuales | 0 | La herramienta Vostok no está presente; queda declarada la limitación de verificación automatizada. |

## Contraste medido

- ES/EN, claro: 4.75:1; seleccionado: 6.9:1.
- ES/EN, oscuro: 8.19:1; seleccionado: 8.05:1.
- Foco del tema, claro: 6.9:1; oscuro: 7.77:1. Contorno visible de 3 px.
- Texto secundario representativo: 4.70:1–5.61:1 claro y 5.10:1–8.59:1 oscuro.

## Límites

- No se aisló en navegador una primera visita sin elección guardada para emular explícitamente las dos preferencias del sistema; se revisó el código de inicio temprano y el uso de `prefers-color-scheme`.
- No se ejecutó un barrido automatizado exhaustivo de todos los píxeles y estados hover. El muestreo cubrió las superficies y controles principales.
- `.vostok/tools/vostok_cli.py` no existe en esta copia del repo aunque `AGENTS.md` lo menciona; por tanto `vostok verify`, `arch-check` y `risk-check` no estuvieron disponibles.
- La auditoría de un subagente de IA no equivale a aceptación humana (`D-H`) ni a revisión humana independiente.

## Telemetría M3

```yaml
audit_duration_s: 925
isolation_mode: separate_agent_or_session
verdict: approved_with_limits
findings_count_by_axis:
  functional: 0
  architecture: 0
  security: 0
  tests: 0
  risks: 0
remediation_triggered: true
```
