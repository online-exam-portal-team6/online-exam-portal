# Usability heuristic evaluation

**Scope:** source review plus visual inspection of eight rendered screenshots supplied for the OEP-71 review. The captures cover administrator dashboard and examination listing, student dashboard, examination-taking, results, login, and desktop/mobile layouts.

## Screenshot evidence inventory

The following rendered captures were inspected. They were supplied in the review conversation; the PNG binaries still need to be committed under `docs/images/usability/` before this repository contains the actual image evidence.

| Capture | Viewport | Dimensions |
|---|---:|---:|
| `admin_dashboard_desktop.png` | Desktop | 1440 × 1449 |
| `admin_exams_desktop.png` | Desktop | 1440 × 935 |
| `exam_take_desktop.png` | Desktop | 1440 × 1137 |
| `login_desktop.png` | Desktop | 1440 × 900 |
| `login_mobile.png` | Mobile | 390 × 844 |
| `results_desktop.png` | Desktop | 1440 × 900 |
| `student_dashboard_desktop.png` | Desktop | 1440 × 1323 |
| `student_dashboard_mobile.png` | Mobile | 390 × 1741 |

## Method

Nielsen's ten usability heuristics were applied to the rendered screens and the current Django templates/CSS. High means a core task is blocked or data may be lost; Medium means avoidable friction; Low means cosmetic or wording improvement.

| Heuristic | Observation | Impact / recommendation |
|---|---|---|
| Visibility of system status | The timed exam exposes a countdown and explains that the server deadline is authoritative. Dashboard cards expose account and exam status. | Positive; keep failed saves visible until retry succeeds. |
| Match to real world | Exam duration, start/end times, and result history use familiar labels. | Keep time zones and date formats consistent. |
| User control | Students can select answers and submit from the exam page. | Keep confirmation before final submit and explain whether submission can be reversed. |
| Consistency | Shared dark theme, navigation, typography, cards, status pills and violet primary actions appear across screens. | Continue using shared components and tokens. |
| Error prevention | The exam page explains automatic saving and server-authoritative expiry. | Explain unavailable states and preserve entered data after recoverable errors. |
| Recognition | Exam and result cards show titles, durations, status and relevant actions in context. | Keep actions adjacent to the item they affect. |
| Flexibility | The login page adapts from a two-panel desktop layout to a single-column mobile layout; student dashboard cards stack on mobile. | Keep keyboard-accessible controls and visible focus. |
| Minimalist design | Restrained accent colour and clear section hierarchy keep the dark interface focused. | Keep dense tables scrollable on small screens. |
| Error recovery | Screenshots show normal states but do not exercise validation failures or network errors. | Add consistent inline error summaries and avoid generic errors. |
| Help and documentation | The exam page communicates autosave and deadline behaviour. | Explain timer, one-attempt policy and expiry behaviour before an attempt starts. |

## Responsive visual inspection

- Login: desktop uses a split-screen form/brand layout; the 390px mobile capture removes the decorative panel and keeps the form within the viewport.
- Student dashboard: desktop uses a persistent side navigation and three-column summary cards; mobile moves navigation above the content and stacks summary/exam/history cards into one column.
- Administrator dashboard and examination listing: the desktop layouts use consistent side navigation, card grids, clear section hierarchy and prominent primary actions. A mobile administrator capture was not included in the supplied evidence.
- Exam-taking: the 1440px capture presents the timer, question cards, answer choices and submit action in a clear vertical sequence. A mobile exam-taking capture was not included.
- Results: the desktop result-history card clearly separates completion/evaluation labels from score and percentage. The captured example displays dashes for score and percentage, so the UI must not imply that an unevaluated attempt has a final score.

## Functional observations requiring follow-up

1. **Student dashboard history count:** the captured dashboard reports zero completed exams while the supplied results screen shows one submitted result. Recheck the dashboard and result-history queries against the integrated attempt/result data.
2. **Evaluation state:** the results card labels the attempt “Evaluated” while score and percentage are both blank. Verify that the current UI now shows a pending state until a persisted Result exists.
3. **Authorization error presentation:** wrong-role or non-owner access should render the designed 403 page; verify the integrated handler and object-ownership behaviour.
4. **Question management integration:** question create, edit and delete implementation is now merged (PRs #17, #20 and #21). The remaining task is end-to-end browser verification of the list/form/delete flows with administrator permissions and validation errors.
5. **Administrator mobile coverage:** add mobile screenshots for administrator dashboard/exam management and exam-taking if responsive acceptance requires those roles/flows.

## Accessibility checks

Inputs need programmatic labels; status updates should use appropriate live regions; focus must remain visible; pass/fail must use text as well as colour; buttons need descriptive labels and adequate touch targets; tables need header cells and horizontal-scroll support.

## Priority actions

1. Recheck the dashboard completed-attempt count against the results history using the integrated result model.
2. Confirm pending versus evaluated state using a submitted attempt with and without a persisted Result.
3. Verify authorization failures render the designed 403 page and student result ownership is enforced.
4. Browser-test question create/edit/delete, including invalid input and delete confirmation.
5. Add administrator and exam-taking mobile captures if required by acceptance criteria.
6. Commit the eight supplied PNG files under `docs/images/usability/` so reviewers can inspect the actual image evidence in the repository.

## Evidence limitation

Eight rendered screenshots were visually inspected for this review. The screenshots are not yet committed to this repository; the inventory above records the supplied filenames and dimensions, not repository-hosted image links. The live screenshots support visual/responsive inspection but do not replace automated accessibility testing, mobile interaction testing, or acceptance testing with representative user accounts.
