# Project Architecture Contract

- **Architectural style:** Modular Monolith
- **Detected bootstrap state:** `unidentified`
- **ADR / Decision link:** `Initial bootstrap (vostok init)`

## 1. Layers and Modules Catalog

| Unit (Layer / Module) | Kind | Physical Path | Responsibility | Local Contract |
| :--- | :--- | :--- | :--- | :--- |
| `core` | module | `src` | Primary application code | None |

## 2. Dependency Rules (Verifiable Matrix)

| Source Unit | May Depend On (Allowed) | Must Not Depend On (Forbidden) | Verification Rule |
| :--- | :--- | :--- | :--- |
| `core` | None | None | Baseline preserved by vostok init |

## Exceptions

| ID | From | To | Reason | ADR / Spec | Expires On |
| :--- | :--- | :--- | :--- | :--- | :--- |
