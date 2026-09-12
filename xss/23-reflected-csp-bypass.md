# Reflected XSS Protected by CSP, With CSP Bypass

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Expert
**Tools:** Burp Suite Community Edition (Proxy, Repeater), Chrome (required —
lab intentionally only solvable in Chrome)
**Status:** ✅ Solved

---

## Objective

The application has a reflected XSS vulnerability, but a Content Security
Policy (CSP) header is in place restricting where scripts can be loaded
from and how they execute. The goal is to both find the reflected injection
point and bypass the CSP protecting it, ultimately calling `alert()`.

## Vulnerability Overview

CSP is designed specifically to mitigate XSS by restricting script sources
and disallowing risky script execution patterns (like inline scripts or
`eval`). However, CSP policies are only as strong as their specific
directives — if a policy allows scripts from a source that also reflects
user input (such as a search endpoint used to serve a script resource), that
trusted source itself becomes an XSS bypass vector.

## Methodology

1. Searched the site for a reflected injection point and confirmed a basic
   `<script>alert(1)</script>` payload was reflected in the response — but
   didn't execute, since the CSP header blocked inline scripts.
2. Inspected the CSP header's directives to understand exactly what it did
   and didn't allow — noted the policy allowed scripts from the site's own
   domain (`script-src 'self'`), which meant any script hosted on that same
   origin would be permitted to run.
3. Identified a second endpoint on the same origin — a search feature — that
   also reflected user input directly into its response, and confirmed this
   endpoint's response could itself be treated as a valid script source
   under the CSP's `'self'` rule, since CSP only checks the origin, not the
   endpoint's actual intended purpose.
4. Confirmed this reflection endpoint's Content-Type/behavior would allow it
   to be loaded via a `<script src="...">` tag pointing back at the site's
   own search endpoint with the alert payload as the query.
5. Injected a `<script src="...">` tag (rather than an inline `<script>`
   block) pointing at the vulnerable, same-origin search endpoint with the
   XSS payload as its query string — since the CSP permitted scripts from
   `'self'`, this external-looking-but-same-origin script tag was allowed to
   execute, and its content (echoed straight from the search query) became
   the executed script body.
6. Delivered the full payload and confirmed the alert fired.

## Proof of Concept

**Initial (blocked) attempt:**
```html
<script>alert(1)</script>
```

**Working CSP-bypass payload — using an allowed same-origin script source:**
```html
<script src="/js/searchResults.js?search='-alert(1)-'"></script>
```

**Result:** Since the CSP explicitly allows scripts loaded from the site's
own origin (`'self'`), and the search endpoint reflects raw user input into
what the browser treats as valid JavaScript when loaded as a script `src`,
the browser executed the injected `alert(1)` — successfully bypassing the
CSP using a same-origin reflection endpoint the policy didn't account for.

## Impact

This lab is a strong illustration that CSP is a mitigation, not a silver
bullet: a broad `'self'` directive is only as safe as every same-origin
endpoint that could conceivably be abused as a script source. Any reflected
input on any same-origin page — even one unrelated to the original
vulnerability — can undermine an otherwise reasonable-looking CSP.

## Remediation

Avoid broad `'self'` script-src directives when any same-origin endpoint
reflects user input; prefer strict CSP configurations using nonces or hashes
for legitimately trusted scripts, and audit every same-origin endpoint for
reflected input that could be abused as an alternate script source.

## Key Takeaway

This was the most conceptually advanced lab in this set — it required
thinking about CSP bypass not as "break the policy" but as "find another
origin-permitted resource the policy trusts by default, that also happens to
reflect attacker input," which is a fundamentally different attack surface
than the direct string-breakout techniques used in earlier labs.
