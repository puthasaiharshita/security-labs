# Reflected XSS in Canonical Link Tag

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Browser DevTools (Chrome required — lab intentionally only
solvable in Chrome), key-combination testing
**Status:** ✅ Solved

---

## Objective

The application reflects user input directly into a `<link rel="canonical">`
tag in the page's `<head>`, but angle brackets are escaped. The goal is to
inject a new attribute into that existing tag that calls `alert()` when the
simulated victim presses a specific key combination (one of `Alt+Shift+X`,
`Ctrl+Alt+X`, or `Alt+X`, per the lab's requirements) — this lab is
intentionally Chrome-only.

## Vulnerability Overview

Since angle brackets are escaped, a fresh tag can't be injected — but the
reflected value lands inside the existing `<link>` tag itself, meaning a new
**attribute** can be added to that tag instead. The `accesskey` attribute,
combined with an `onclick` handler, lets a specific keyboard shortcut trigger
JavaScript execution once the correct modifier-key combination is pressed —
without needing any interaction beyond the keypress itself.

## Methodology

1. Viewed the page source and found the reflected input placed inside a
   `<link rel="canonical" href="...REFLECTED...">` tag, and confirmed angle
   brackets in the input were HTML-escaped when tested.
2. Since angle brackets were blocked, focused on breaking out of the
   existing `href` attribute value instead, using an unescaped double quote
   to close it and introduce new attributes on the same `<link>` tag.
3. Added a random alphanumeric string to the payload first, purely to
   confirm the injection point was reflecting correctly before attempting
   the real payload (a good sanity-check step before committing to the full
   exploit).
4. Injected an `onclick` handler attribute containing `alert(1)`, and
   confirmed via source inspection that the new attribute landed correctly
   on the tag.
5. Since `onclick` alone requires a mouse click (and the lab specifically
   requires triggering via a keyboard combination), added an `accesskey`
   attribute set to a chosen letter (e.g. `x`), which — in Chrome — combined
   with a modifier key combination (`Alt+Shift+X` on Windows/Linux Chrome)
   triggers the associated element's default action (interpreted here as
   firing the `onclick` handler).
6. Verified the correct modifier combination by checking Chrome's specific
   accesskey behavior, then confirmed the alert fired when the key
   combination was simulated.

## Proof of Concept

**Payload used to break out of the `href` attribute and add new attributes:**
```html
" accesskey="x" onclick="alert(1)
```

**Resulting tag (conceptually):**
```html
<link rel="canonical" href="" accesskey="x" onclick="alert(1)">
```

**Result:** When the simulated victim pressed the Chrome accesskey
combination (`Alt+Shift+X`) for the assigned key `x`, the browser triggered
the link element's default action, firing the injected `onclick` handler and
executing `alert(1)`.

## Impact

This lab shows that even tags not normally considered "interactive" (like a
`<link rel="canonical">`, which is metadata, not a visible or clickable
element) can become an XSS vector once attacker-controlled attributes are
added — the `accesskey` + `onclick` combination effectively turns an inert
`<link>` element into something triggerable purely by keyboard shortcut, with
no visible UI at all.

## Remediation

HTML-encode all characters with special meaning in attribute-value contexts
(especially quotes) when reflecting user input into any tag, metadata
elements included — "it's not a visible/clickable element" is not a safe
assumption once arbitrary attributes can be injected onto it.

## Key Takeaway

This lab was a good reminder to think about attribute injection risk on
*every* tag reflecting user input, not just obviously interactive ones —
metadata tags like `<link>` can still become fully interactive attack
vectors once `accesskey`/`onclick` (or similar attribute pairs) can be
attached to them.
