# DOM XSS in document.write Sink Using Source location.search

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The lab contains a DOM-based cross-site scripting vulnerability in the search
query tracking functionality. The page uses `document.write()` to write data
taken from `location.search` (the URL's query string) directly into the DOM.
The goal is to perform a cross-site scripting attack that calls the `alert()`
function.

## Vulnerability Overview

This is a **DOM-based** vulnerability rather than a server-side one — the
data never round-trips through the server as HTML. Instead, client-side
JavaScript reads a value straight from the URL (`location.search`, the
**source**) and writes it into the page using `document.write()` (the
**sink**). Because `document.write()` interprets its argument as raw HTML,
any HTML/JavaScript in the URL is parsed and executed directly by the
browser.

## Methodology

1. Identified that the search functionality echoes the search term back onto
   the page, and confirmed (via viewing page source / DevTools) that this was
   happening through a `document.write()` call reading from `location.search`,
   not a server-rendered response.
2. Recognized this meant the browser itself would interpret whatever HTML was
   present in the injected value, so the goal was to make the URL-controlled
   input become executable HTML.
3. Since `document.write()` writes its argument as raw HTML (not raw
   JavaScript), a plain `<script>` tag wasn't the most reliable route here —
   instead, used an HTML element with a built-in event handler that fires
   automatically once the element loads: `<svg onload=alert(1)>`.
4. The `<svg>` tag is a valid HTML element the browser will render, and its
   `onload` event fires as soon as the element finishes loading — no user
   interaction required, and no separate `<script>` execution context needed.

## Proof of Concept

**Payload used in the URL search parameter:**
```html
"><svg onload=alert(1)>
```

**Example request:**
```
GET /?search="><svg onload=alert(1)> HTTP/2
```

**Result:** As soon as the `<svg>` element loaded in the page, its `onload`
handler fired immediately, executing the injected JavaScript and popping the
alert — confirming the DOM-based XSS via `document.write()`.

## Impact

DOM-based XSS is easy to miss in a code review focused only on server-side
output encoding, since the vulnerable data flow exists entirely in client-side
JavaScript. An attacker exploiting this could craft a malicious URL and send
it to a victim; anything executed here runs in the victim's browser under the
site's own origin, with full access to cookies and page content.

## Remediation

Avoid `document.write()` entirely when handling untrusted data — use safer
DOM APIs like `textContent` for plain text, or ensure any HTML insertion goes
through a proper sanitization library. More generally, never feed
`location.search`, `location.hash`, or similar URL-derived values directly
into HTML-writing sinks without encoding.

## Key Takeaway

This was the first lab that shifted my focus from "does the server escape
output" to "does *any* client-side JavaScript take untrusted input (a
source) and write it somewhere dangerous (a sink)" — DOM XSS requires
tracing data flow through JavaScript itself, not just the server response.
