# DOM XSS in document.write Sink Using Source location.search Inside a Select Element

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The stock-checker widget uses `document.write()` to build a `<select>`
dropdown of store locations, with the currently selected option driven by a
`storeId` URL parameter (sourced from `location.search`). The goal is to
break out of the existing `<select>`/`<option>` markup and call `alert()`.

## Vulnerability Overview

This is another `document.write()` DOM XSS sink, but the injection point is
**inside an existing HTML element structure** (a `<select>` with several
`<option>` children) rather than a blank/plain context. To exploit it, the
injected value needs to properly close the surrounding `<select>` element
before introducing new, executable markup — otherwise the payload just
becomes another (inert) `<option>`.

## Methodology

1. Viewed the page's source/DevTools and found the vulnerable JavaScript:
   the value of `storeId` from `location.search` was inserted directly into
   a `document.write()` call building a `<select>` element's `selected`
   option.
2. Confirmed the value was reflected inside the HTML structure as an
   attribute-like value within the `<select>`/`<option>` block, not in a
   free HTML context — meaning a raw `<img onerror=...>` payload alone
   wouldn't render correctly without first closing the surrounding
   `<select>` and `<option>` tags.
3. Constructed a payload that first closes the `</option>` and `</select>`
   tags properly, then introduces a fresh, valid HTML element with an event
   handler — using `<img src=1 onerror=alert(1)>` — followed by relevant
   markup to keep the rest of the page visually intact (not strictly
   necessary for exploitation, but good practice to avoid obviously breaking
   the page layout).
4. Submitted the crafted URL with the payload in the `storeId` parameter and
   confirmed the alert fired on page load.

## Proof of Concept

**Payload used in the `storeId` parameter:**
```html
"></select><img src=1 onerror=alert(1)>
```

**Example URL:**
```
https://TARGET-LAB/product/stock?productId=1&storeId="></select><img src=1 onerror=alert(1)>
```

**Result:** The payload closed the existing `<select>` element cleanly, then
introduced a new `<img>` element with a broken `src`, whose `onerror` event
fired immediately, executing `alert(1)` and confirming the DOM-based XSS via
`document.write()` inside a structured HTML context.

## Impact

This lab shows that DOM XSS defenses have to account not just for whether a
sink writes raw HTML, but for the **structural context** the injection lands
in — a payload that would work in a blank context can fail (or render inert)
if it doesn't first properly close out surrounding tags like `<select>`/
`<option>`.

## Remediation

Avoid using `document.write()` to build dynamic, structured HTML like
dropdowns from URL-derived values at all. If dynamic option lists are
required, build them using safe DOM methods (e.g. `document.createElement`
and `textContent`) rather than raw string concatenation and HTML writing.

## Key Takeaway

This lab reinforced that exploiting DOM XSS inside structured markup (tables,
selects, lists) usually requires an extra step most "context-free" DOM XSS
payloads skip: properly closing the surrounding tags before introducing new,
executable elements — otherwise the payload just becomes inert, malformed
markup instead of a working exploit.
