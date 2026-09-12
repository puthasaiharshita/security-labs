# DOM XSS in jQuery Anchor href Attribute Sink Using location.search Source

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The lab contains a DOM-based cross-site scripting vulnerability in the submit
feedback page. It uses the jQuery library's `$` selector function to find an
anchor element and changes its `href` attribute using data from
`location.search`. The goal is to make that link execute `alert(document.cookie)`
when clicked.

## Vulnerability Overview

The **source** is `location.search` (specifically, a `returnUrl` query
parameter used to build a "back" link) and the **sink** is the anchor
element's `href` attribute, set via jQuery. Since `href` accepts the
`javascript:` URI scheme, and the value is taken from the URL with no
validation, an attacker can make the link's destination itself be executable
JavaScript instead of a real URL.

## Methodology

1. Used the browser's "Inspect" tool on the "back" link on the feedback
   confirmation page and found its `href` attribute was built directly from
   the `returnUrl` query parameter with no validation of what that value
   actually was.
2. Recognized that `href` attributes accept the `javascript:` pseudo-protocol,
   which executes arbitrary JavaScript when the link is clicked, instead of
   navigating to a URL.
3. Modified the `returnUrl` parameter in the address bar to a `javascript:`
   payload instead of a real path.
4. Loaded the crafted URL, then manually clicked the "back" link to confirm
   the JavaScript executed (this requires user interaction — clicking the
   link — unlike some other DOM XSS variants that fire automatically on page
   load).

## Proof of Concept

**Payload used in the `returnUrl` parameter:**
```
javascript:alert(document.cookie)
```

**Example URL:**
```
https://.../feedback?returnUrl=javascript:alert(document.cookie)
```

**Result:** Clicking the "back" link triggered the injected JavaScript
instead of navigating anywhere, popping an alert containing the page's
cookies — confirming the `href` sink was vulnerable to `javascript:` URI
injection.

## Impact

Because this requires a user click rather than firing automatically, it's
slightly less severe than some DOM XSS variants — but it's still fully
exploitable via social engineering (an attacker sending a link and prompting
the victim to click "back" or a similarly labeled link), and the payload
executes with full access to cookies and page context once clicked.

## Remediation

Never build `href` (or `src`) attribute values directly from untrusted input
without validating that the resulting value is a legitimate, safe URL —
explicitly reject `javascript:`, `data:`, and other executable URI schemes,
or use an allowlist of permitted URL patterns (e.g. only relative paths
starting with `/`).

## Key Takeaway

This lab showed that DOM XSS isn't limited to obvious HTML-writing sinks like
`innerHTML` or `document.write()` — attribute assignments like `href` can be
just as dangerous when they accept executable URI schemes, and jQuery's
convenience selectors don't add any automatic protection against this.
