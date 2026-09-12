# Reflected XSS into HTML Context With All Tags Blocked Except Custom Ones

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser
**Status:** ✅ Solved

---

## Objective

This lab blocks all standard HTML tags, allowing only custom (non-standard,
made-up) tag names through the filter. The goal is to perform a cross-site
scripting attack that automatically calls `print(document.cookie)` — meaning
the exploit must fire without any manual user interaction.

## Vulnerability Overview

The filter here allowlists only tags it doesn't recognize as "real" HTML
elements — since browsers still render unknown/custom tags as generic inline
elements, this leaves a gap: a made-up tag name combined with a valid event
handler attribute can still execute JavaScript, even though no real HTML
element like `<img>` or `<body>` is being used.

## Methodology

1. Confirmed via testing that standard tags (`<script>`, `<img>`, `<svg>`,
   etc.) were all blocked by the filter, but a completely made-up tag name
   was allowed through untouched.
2. Since a custom tag has no default behavior of its own, needed an event
   attribute that fires **automatically** without requiring any user
   interaction (unlike `onclick` or `onmouseover`) — used the `onfocus`
   event combined with the `autofocus` HTML attribute, which causes the
   browser to focus the element as soon as the page loads, immediately
   triggering `onfocus` with zero interaction needed.
3. Also added a `tabindex` attribute, which makes the custom element
   focusable at all (since custom tags aren't focusable by default without
   it).
4. Constructed the full payload with a custom tag name, `onfocus` handler,
   `tabindex="1"`, and `autofocus` (or, per the exact approach, used the
   `#` URL fragment to bring focus to the element via the browser's fragment
   targeting behavior).
5. Since the lab requires the exploit to fire automatically (not from a
   manually visited URL), used the exploit server to auto-redirect a
   simulated victim to the crafted URL with a trailing `#x` fragment matching
   the injected element's `id`, so the browser automatically focuses that
   element on load.

## Proof of Concept

**Payload used in the search parameter:**
```html
<xss id=x onfocus=alert(document.cookie) tabindex=1>#x
```

**Delivery via exploit server (auto-redirect to trigger without interaction):**
```html
<script>
  window.location = "https://TARGET-LAB/?search=%3Cxss+id%3Dx+onfocus%3Dprint(document.cookie)+tabindex%3D1%3E#x";
</script>
```

**Result:** On load, the browser auto-focused the custom `<xss>` element
(due to the URL fragment matching its `id` and the `tabindex` making it
focusable), immediately firing the `onfocus` handler and executing
`print(document.cookie)` — with zero manual interaction from the victim.

## Impact

This demonstrates that "only allow custom tags" is not a meaningful security
boundary — any tag, real or invented, becomes dangerous the moment it carries
an event-handler attribute the browser will fire, and browsers' fragment/
focus behavior can be abused to trigger such handlers automatically.

## Remediation

Filtering should never be based on an allowlist of "unrecognized" tag names;
instead, output encoding should neutralize `<` and `>` entirely regardless of
what follows them, and any HTML that genuinely needs to render should go
through a strict, attribute-aware sanitization library (like DOMPurify) with
an allowlist of both tags **and** attributes, not tags alone.

## Key Takeaway

This lab was a good demonstration that browsers treat any unknown tag as a
generic, attribute-bearing element — meaning tag-name filtering alone
provides no protection at all if event-handler attributes are still
permitted, and that URL fragments can be weaponized to trigger `autofocus`-
style automatic execution without any click or hover.
