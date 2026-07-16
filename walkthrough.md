# Walkthrough: Dynamic Margins for Right-Side Prompt Alignment

We have corrected the right-side alignment of the query prompt input bar while preserving the left-side indentation offset during active chat states.

## Changes Made

### 1. Left-Offset & Right-Bound Alignment
- **Centering Correction:** Reverted the asymmetrical form padding hacks. Kept the `#message-form` container width centered at `860px` with equal `16px` padding on both sides.
- **Asymmetric Margins on Input Wrapper:** Set `.input-wrapper` inside the active message form to have `margin-left: 56px` and `margin-right: 0`.
- **Result:** 
  - **Left Edge:** Indented by `56px` to align perfectly with the chatbot's message text starting column (skipping the left-side bot avatars/loaders).
  - **Right Edge:** Spans all the way to the right border of the `860px` centered column (matching the right boundary of the user message bubble).
- **Landing Page Centering:** Reset `.input-wrapper` to `margin-left: auto; margin-right: auto; max-width: 860px;` during `.centered-layout` states, keeping the box perfectly centered and symmetrical on the initial landing/empty page.

---

## Verification Results

- **Django System Check:** Checked successfully:
  ```bash
  System check identified no issues (0 silenced).
  ```
