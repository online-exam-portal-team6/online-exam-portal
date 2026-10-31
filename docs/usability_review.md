# Usability heuristic evaluation

**Scope:** source-based review of the current Django templates and CSS. This is not represented as a live browser study or screenshot-based responsive test.

## Method
Nielsen's ten usability heuristics were applied. High means a core task is blocked or data may be lost; Medium means avoidable friction; Low means cosmetic or wording improvement.

| Heuristic | Observation | Impact / recommendation |
|---|---|---|
| Visibility of system status | Timed exam exposes a countdown and answer-save feedback. | Positive; keep failed saves visible until retry succeeds. |
| Match to real world | Duration and availability labels are familiar. | Keep time zones and date formats consistent. |
| User control | Students can change a selected option before submission. | Keep confirmation before final submit. |
| Consistency | Shared navigation, typography, cards and status styles. | Reuse shared components and tokens. |
| Error prevention | Start and submit are POST actions; server validates availability/deadline. | Explain unavailable states and preserve entered data. |
| Recognition | Exam/result cards show key details in context. | Keep actions adjacent to the item they affect. |
| Flexibility | Autosave reduces separate save actions. | Keep keyboard-accessible radio groups and visible save status. |
| Minimalist design | Restrained accent colour and section hierarchy. | Keep dense tables scrollable on small screens. |
| Error recovery | Django messages and field errors provide feedback. | Add consistent inline error summary; avoid generic errors. |
| Help and documentation | Rules appear before an attempt. | Explain timer, one-attempt policy and expiry behaviour. |

## Responsive source inspection
The shared dashboard stylesheet has breakpoints at 900px and 600px. At the smaller breakpoint the sidebar moves into page flow, content margins are removed and exam cards become a single column. The exam page stacks its toolbar and timer panel on narrow screens.

## Accessibility checks
Inputs need programmatic labels; status updates should use appropriate live regions; focus must remain visible; pass/fail must use text as well as colour; buttons need descriptive labels and adequate touch targets; tables need header cells and horizontal-scroll support.

## Priority actions
1. Keep save failures visible until retry succeeds.
2. Confirm final submission.
3. Give all result states text labels in addition to colour.
4. Perform live desktop/mobile browser checks and attach screenshots.

## Evidence limitation
No browser screenshot evidence is included in this source-only review. The screenshot requirement remains open until rendered pages are captured at desktop and mobile widths and committed or attached.
