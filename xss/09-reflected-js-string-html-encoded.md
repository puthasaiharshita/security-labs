# Reflected XSS into a JavaScript String With Angle Brackets HTML Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

The lab contains a reflected cross-site scripting vulnerability in the search
query tracking functionality, where angle brackets are HTML-encoded. The
reflection occurs **inside a JavaScript string**. The goal is to break out of
that string and call `alert()`.

## Vulnerability Overview

Since angle brackets are HTML-encoded, injecting a new `<script>` tag won't
work — but the input is reflected inside an existing JavaScript variable
assignment (`var searchTerms = 'YOUR_INPUT';`), inside a script block that's
already executing. If the surrounding single quotes aren't escaped, an
attacker can close the string early, inject entirely new JavaScript
statements, and then reopen a dummy string afterward so the rest of the
original script still parses without a syntax error.

## Methodology

1. Submitted a test search term and viewed the page source, finding it
   reflected inside `var searchTerms = 'YOUR_INPUT';` within an existing
   `<script>` block.
2. Confirmed angle brackets were encoded (ruling out a fresh `<script>` tag
   injection) but noted the single quotes around the reflected value were
   **not** escaped.
3. Constructed a payload that: closes the original string with a single
   quote, adds a semicolon to terminate that statement cleanly, injects a
   new `alert(1)` statement, and then reopens an empty string literal on both
   sides so the trailing portion of the original line (if any) still parses
   without breaking the script.
4. Verified the alert fired directly on page load, since this executes inside
   an already-running script block (no user interaction required, unlike
   attribute-based injections needing a click or hover).

## Proof of Concept

**Payload used in the search parameter:**
```javascript
'-alert(1)-'
```

**Resulting script (conceptually):**
```javascript
var searchTerms = ''-alert(1)-'';
```

**Result:** The browser executed `alert(1)` immediately as part of the
existing script block on page load, confirming the JavaScript string context
was exploitable despite angle-bracket encoding.

## Impact

This demonstrates that HTML encoding alone is not sufficient once user input
is reflected into a JavaScript context — a JS string is a fundamentally
different parsing context than HTML, with its own dangerous characters
(quotes, backslashes) that need separate, context-aware escaping.

## Remediation

When reflecting data inside a JavaScript string literal, use proper
JavaScript string escaping (escaping quotes, backslashes, and other
JS-significant characters) — HTML encoding of `<`/`>` has no bearing on
JavaScript string syntax and doesn't prevent this class of injection at all.

## Key Takeaway

This lab reinforced that "the input is reflected somewhere in the page" isn't
enough information on its own — the *specific parsing context* (HTML body vs.
HTML attribute vs. JavaScript string vs. JSON, etc.) determines which
characters are actually dangerous and need escaping, and each context needs
its own defense.
