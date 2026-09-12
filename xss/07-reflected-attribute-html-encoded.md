# Reflected XSS into Attribute With Angle Brackets HTML-Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

The lab contains a reflected cross-site scripting vulnerability in the search
blog functionality, where angle brackets are HTML-encoded. The goal is to
perform a cross-site scripting attack that injects an attribute and calls the
`alert()` function.

## Vulnerability Overview

The application does encode `<` and `>` before reflecting user input, which
means a straightforward `<script>` payload gets rendered as inert text, not
executed. However, the input is reflected **inside an existing HTML attribute
value** (specifically, an `input` element's `value` attribute), and the
double-quote character is **not** encoded — so an attacker can close the
attribute early and inject a brand-new attribute (like `onmouseover`) without
ever needing an angle bracket at all.

## Methodology

1. Submitted a test value in the search box and inspected the reflected HTML,
   finding the input was placed inside `<input value="YOUR_INPUT">`.
2. Tested a plain `<script>` payload first — confirmed it appeared as
   encoded, inert text rather than executing, ruling out a normal
   tag-injection approach.
3. Noticed the double quote character in the input was **not** encoded,
   meaning a payload containing `"` could close the existing `value`
   attribute early.
4. Constructed a payload that closes the `value` attribute, then adds a new
   `onmouseover` event handler attribute containing the `alert()` call,
   ensuring the rest of the tag still parses correctly by closing it cleanly
   with `>`.
5. Confirmed exploitation by hovering the mouse over the resulting input
   field and observing the alert fire (since `onmouseover` requires user
   interaction, unlike some other event handlers).

## Proof of Concept

**Payload used in the search parameter:**
```html
" onmouseover="alert(1)
```

**Resulting HTML (conceptually):**
```html
<input value="" onmouseover="alert(1)">
```

**Result:** Hovering over the search input field on the results page
triggered the `alert(1)` popup, confirming successful attribute injection
despite angle-bracket encoding.

## Impact

This lab shows that encoding only `<` and `>` is an incomplete defense —
attribute-context injections don't require any angle brackets at all if the
surrounding quote character is left unencoded. In a real application, this
could let an attacker inject any event-handler-based payload achievable
through user interaction with the affected element (clicks, hovers, focus
events, etc.).

## Remediation

HTML-encode **all** characters with special meaning in the relevant context,
not just `<` and `>` — specifically, `"` and `'` must also be encoded when
reflecting data inside an HTML attribute value, since those characters are
what allow breaking out of the attribute in the first place.

## Key Takeaway

This lab was an important reminder that XSS defenses are context-specific:
encoding rules that are sufficient for the HTML body context (encoding `<`
and `>`) are not sufficient for the attribute-value context, where quote
characters are the actual dangerous characters to control.
