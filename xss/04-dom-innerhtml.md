# DOM XSS in innerHTML Sink Using Source location.search

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The lab contains a DOM-based cross-site scripting vulnerability in the search
blog functionality. It uses an `innerHTML` assignment, which changes the HTML
contents of a `div` element, using data from `location.search`. The goal is
to perform a cross-site scripting attack that calls the `alert()` function.

## Vulnerability Overview

Here, the **source** is `location.search` (the URL query string) and the
**sink** is an `innerHTML` assignment on a `div` element. `innerHTML` parses
whatever string is assigned to it as HTML and inserts it into the DOM — so
any tags in the URL-derived value get rendered as real elements, not escaped
text.

## Methodology

1. Confirmed via page inspection that the search term was being inserted into
   a `div` using `element.innerHTML = ...` sourced from `location.search`,
   rather than a safe method like `textContent`.
2. Noted an important constraint specific to `innerHTML`: unlike
   `document.write()`, a plain `<script>` tag assigned via `innerHTML` does
   **not** execute — browsers deliberately suppress script execution for
   `<script>` elements inserted this way, as a partial XSS mitigation.
3. Used an `<img>` tag with a broken `src` and an `onerror` event handler
   instead — since event handler attributes on elements inserted via
   `innerHTML` **do** execute normally, this bypasses the `<script>`
   restriction entirely.
4. Constructed the URL with the `<img>` payload in the search parameter.

## Proof of Concept

**Payload used in the URL search parameter:**
```html
<img src=x onerror=alert(1)>
```

**Result:** The browser attempted to load the broken image source, failed,
and fired the `onerror` handler — executing the injected JavaScript and
popping the alert, confirming the DOM-based XSS via the `innerHTML` sink.

## Impact

Same category of impact as other DOM XSS — full script execution in the
victim's browser context via a crafted URL — but this lab specifically
demonstrates that "the sink doesn't execute `<script>` tags" is not a real
mitigation, since event-handler-based payloads bypass that restriction
entirely.

## Remediation

Avoid `innerHTML` for untrusted data; use `textContent` when only plain text
needs to be displayed, or run any necessary HTML through a dedicated
sanitization library (e.g. DOMPurify) before insertion. Relying on browsers'
partial script-blocking behavior in `innerHTML` is not sufficient protection
on its own.

## Key Takeaway

This lab reinforced that different DOM sinks have different execution rules
(`document.write()` executes `<script>` tags directly; `innerHTML` does not,
but still executes inline event handlers) — understanding these sink-specific
quirks is essential for correctly identifying whether a "blocked" payload
type actually closes off the vulnerability or just requires a different
payload shape.
