# Reflected XSS into HTML Context With Most Tags and Attributes Blocked

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Intruder)
**Status:** ✅ Solved

---

## Objective

The lab contains a reflected XSS vulnerability in the search functionality,
but a web application firewall (WAF) is in place blocking most common XSS
vectors. The goal is to identify a tag/attribute combination the WAF allows
through, then use it to call `print()`.

## Vulnerability Overview

Rather than blocking XSS at the root cause (output encoding), this
application relies on a WAF pattern-matching known-bad tags and attributes.
Since the WAF works from a blocklist, any tag or event-handler attribute it
hasn't been configured to catch will pass through unfiltered — the task is
to systematically discover which ones those are.

## Methodology

1. Sent the vulnerable search request to Burp Intruder and added the
   position marker (`<>`) around the payload location in the request.
2. Used Intruder's "Sniper" attack with a payload list pulled from the SQLi/
   XSS cheat sheet's full list of HTML tags, to systematically test which
   individual tags the WAF allows vs. blocks — filtered results by HTTP
   status (blocked tags returned 400, allowed ones returned 200).
3. Repeated the same process for event-handler **attributes** (e.g.
   `onerror`, `onload`, `onmouseover`, etc.), testing each against a
   generically allowed tag to find which attribute names pass the filter.
4. Cross-referenced the two lists: found that the `body` tag was allowed, and
   the `onresize` event attribute was also allowed — a combination not
   commonly blocked by default WAF rulesets, since `onresize` isn't a typical
   "obvious" XSS vector like `onerror` or `onclick`.
5. Since `onresize` requires an actual resize event to fire, and there's no
   direct user interaction to trigger this on page load, used an `iframe`
   trick: load the vulnerable page inside an iframe, then resize the iframe
   itself via JavaScript after it loads — this fires the `onresize` handler
   automatically inside the target page.

## Proof of Concept

**Working payload (combining allowed tag + attribute):**
```html
<body onresize=print()>
```

**Exploit delivery (iframe resize trick):**
```html
<iframe src="https://TARGET-LAB/?search=<body onresize=print()>"
onload="this.style.width='100px'"></iframe>
```

**Result:** When the iframe's `onload` handler resized the iframe itself,
this triggered a `resize` event inside the loaded page, firing the injected
`onresize` handler and executing `print()` — confirming a full WAF bypass
using an allowed tag/attribute combination.

## Impact

This lab shows the fundamental limitation of blocklist-based WAF protection:
no blocklist can realistically cover every possible tag/attribute
combination, and less obvious event handlers (like `onresize`) are easy to
overlook when configuring filter rules, even though they're fully
exploitable with the right delivery mechanism.

## Remediation

WAFs should be treated as a defense-in-depth layer, never a substitute for
proper output encoding at the application level. Systematic encoding of
user-controlled output (rather than pattern-matching known-bad payloads)
closes the vulnerability regardless of which specific tag or attribute an
attacker tries.

## Key Takeaway

This was the first lab requiring genuine automated enumeration (via
Intruder) to map out a WAF's actual blocklist rather than relying on a known
payload from a cheat sheet — and it highlighted that even "sensible-seeming"
blocklists can be bypassed simply by finding an event handler the filter
author didn't think to include.
