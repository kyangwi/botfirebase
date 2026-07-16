# Walkthrough: Text Bar Width Alignment

We have updated the user question input text field's width constraint to match the exact boundaries of the messages text content column.

## Changes Made

### 1. Unified Max-Width Alignment
- **Width Correction:** Modified `#message-form .input-wrapper` in [index.html](file:///d:/JOSH/AgenticSQLChatBot/chat/templates/chat/index.html) and [templates/index.html](file:///d:/JOSH/AgenticSQLChatBot/templates/index.html) to restrict `max-width` to **`748px`** (down from `860px`).
- **Symmetric Centering:** The prompt box remains symmetrically centered via `margin: 0 auto`.
- **Result:** Since bot response messages start after a 36px avatar and 14px gap (56px offset on the left) and user messages end 56px before the right edge, the actual text content column spans exactly `860px - 56px - 56px = 748px` on desktop. The prompt box now aligns perfectly with the starting boundary of the text, avoiding any overlaps on the left (such as with the loading avatar).

---

## Verification Results

- **Django System Check:** Checked successfully:
  ```bash
  System check identified no issues (0 silenced).
  ```
