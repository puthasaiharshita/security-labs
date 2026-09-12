# Reflected XSS With Some SVG Markup Allowed

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Intruder)
**Status:** ✅ Solved

---

## Objective

This lab blocks most common XSS tags and event attributes but does allow
some SVG markup through. The goal is to perform a cross-site scripting
attack that calls the `alert()` function.

## Vulnerability Overview

SVG (Scalable Vector Graphics) is XML-based markup that supports its own set
of elements and animation-related attributes — some of which (like
`<animatetransform>`) can execute JavaScript via event handlers, just like
standard HTML elements. Filters that focus on blocking common HTML-based XSS
vectors often overlook SVG-specific animation elements and their event
attributes entirely.

## Methodology

1. Sent the vulnerable request to Burp Intruder and tested a broad list of
   HTML tags against the filter to identify which ones were allowed — found
   that standard tags (`script`, `img`, `body`, etc.) were blocked, but
   `<svg>` itself passed through.
2. Since `<svg>` alone doesn't execute JavaScript, tested which **event
   attributes** the filter allowed by adding a generic payload marker after
   `%20` (URL-encoded space) inside the SVG tag and iterating attribute names
   via Intruder, filtering for allowed (200-status) responses.
3. Found `onbegin` was allowed as an event attribute — this event fires when
   an SVG animation element begins.
4. Combined `<svg>` with the `<animatetransform>` child element (an SVG
   element used to animate transformations, which supports the `onbegin`
   event) to build a working payload that executes automatically as soon as
   the SVG element starts rendering.

## Proof of Concept

**Working payload:**
```html
<svg><animatetransform onbegin=alert(1)>
```

**Result:** As soon as the browser began rendering the SVG's animation
element, the `onbegin` event fired automatically, executing `alert(1)` and
confirming a successful bypass using an SVG-specific animation vector rather
than a standard HTML tag/event combination.

## Impact

This lab shows that XSS filters focused only on standard HTML tags and
common event handlers (`onerror`, `onclick`, `onload`) can be bypassed
entirely by moving into SVG's separate markup vocabulary, which has its own
set of animation-triggered event attributes that are easy to overlook when
building a blocklist.

## Remediation

As with other filter-bypass labs, the real fix is proper context-aware output
encoding rather than tag/attribute blocklisting. If SVG upload or embedding
is a genuine business requirement, it should go through a dedicated,
well-maintained SVG sanitizer that strips all script-capable elements and
event attributes, not a generic HTML filter.

## Key Takeaway

This lab expanded my mental model of "XSS vectors" beyond standard HTML —
SVG is a full markup language with its own animation-based event system, and
any filter that doesn't specifically account for SVG's unique elements
(`animate`, `animatetransform`, `set`, etc.) and their `onbegin`/`onend`
events leaves a real gap.
