# Reflected XSS With Event Handlers and href Attributes Blocked

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Intruder)
**Status:** ✅ Solved

---

## Objective

This lab has a whitelist-based filter: only certain tags are allowed, but
**all** event attributes and `href` attributes are blocked outright. The
goal is to inject a vector that, when clicked, calls `alert()` — and the
vector must be labeled with the word "Click me" to simulate inducing a real
user to click it.

## Vulnerability Overview

Since both event handlers (which normally trigger JavaScript) and `href`
(which would normally carry a `javascript:` payload) are blocked, a direct
clickable-link approach fails outright. However, SVG's `<animate>` element
supports an `attributeName`/`values` mechanism that can **animate** an
attribute's value over time — including animating an anchor's `href`
attribute into a `javascript:` URI, entirely through SVG markup, without
ever directly setting a blocked `href` or event attribute in the injected
payload itself.

## Methodology

1. Sent the request to Burp Intruder and tested the full HTML tag list from
   the cheat sheet, filtering for allowed (200-status) tags — found `svg`,
   `animate`, and `a` (anchor) were all allowed, while direct `href` and any
   `on*` event attribute were blocked outright regardless of tag.
2. Recognized that since a literal `href` attribute was blocked, but the SVG
   `<animate>` element's `attributeName="href"` parameter is just a string
   value (not the actual restricted attribute name being parsed by the
   filter), this offered a way to set the anchor's `href` indirectly.
3. Built a payload nesting an `<a>` (anchor) element inside an `<svg>`, with
   an `<animate>` child element targeting the anchor's `href` attribute via
   `attributeName=href`, and setting its animated `values` to a
   `javascript:alert(1)` URI.
4. Labeled the visible anchor text "Click Me" as required by the lab, since
   the vector needs a human to actually click it (this isn't an
   auto-firing exploit).
5. Verified in the browser that once the SVG animation applied the
   `javascript:` value to the anchor's `href`, clicking the resulting "Click
   Me" link executed the alert.

## Proof of Concept

**Working payload:**
```html
<svg><a><animate attributeName=href values="javascript:alert(1)" /><text
x=20 y=20>Click Me</text></a>
```

**Result:** The SVG `<animate>` element applied the `javascript:alert(1)`
value to the anchor's `href` attribute at runtime, bypassing the filter
(which only inspected the literal attributes written in the payload, not
values applied dynamically via SVG animation). Clicking the resulting "Click
Me" text executed the alert.

## Impact

This lab demonstrates a genuinely creative filter bypass class: rather than
smuggling a blocked attribute past the filter directly, SVG's animation
system can be used to **apply** a dangerous attribute value at runtime, after
the filter has already approved the (seemingly harmless) static markup. Any
filter that only inspects literal attribute/value pairs in the submitted
payload — without accounting for what SVG animation can dynamically set — is
bypassable this way.

## Remediation

Blocklisting specific attributes (`href`, `on*`) is not sufficient when SVG
animation elements can indirectly set those same attributes at runtime.
Proper sanitization libraries (like DOMPurify) are specifically built to
account for this class of SVG-based bypass and should be used instead of
custom attribute blocklists.

## Key Takeaway

This was the most conceptually interesting filter bypass in this set — it
required realizing that "blocked attribute" only means the filter checks the
literal payload text, not what the browser's own rendering engine (via SVG
animation) can dynamically apply afterward. It's a good example of why
building custom XSS filters is so error-prone compared to using
well-vetted sanitization libraries.
