# DOM XSS in jQuery Selector Sink Using a hashchange Event

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The lab contains a DOM-based cross-site scripting vulnerability on the home
page. It uses jQuery's `$()` selector function to auto-scroll to a given
post, whose title is passed via the URL's hash fragment (`location.hash`).
The goal is to deliver an exploit that calls `print()` in the victim's
browser, since a mock ad-blocker on the page blocks direct calls to `alert()`.

## Vulnerability Overview

The **source** here is `location.hash` (everything after `#` in the URL,
which the JavaScript reads on every `hashchange` event). The **sink** is
jQuery's `$()` selector function: when the hash looks like a CSS selector
(e.g. `#post1`), the page scrolls to a matching element — but jQuery's
selector engine also interprets certain patterns (like `<img src=x
onerror=...>`) as HTML to be created and inserted, not just a selector
string, if it doesn't look like a valid CSS selector. This means the hash
value can be used to inject and execute arbitrary HTML/JavaScript.

## Methodology

1. Confirmed via page inspection that the site listens for the `hashchange`
   event and passes `location.hash` (minus the `#`) directly into jQuery's
   `$()` function.
2. Recognized that jQuery's `$()` will attempt to create new DOM elements
   from its argument if the string looks like an HTML tag rather than a CSS
   selector — this is the exploitable behavior.
3. Since a direct `alert()` payload was explicitly blocked by a mock
   ad-blocker on the page, used `print()` instead, per the lab's instructions.
4. Built an exploit page (hosted via PortSwigger's exploit server) containing
   an iframe pointing at the vulnerable home page, with the malicious hash
   fragment appended to its `src`, followed by an `onload` handler that
   changes the iframe's `src` a second time to trigger the `hashchange` event
   after the page has fully loaded.
5. Delivered this exploit page to the simulated victim.

## Proof of Concept

**Payload used in the hash fragment:**
```html
<img src=x onerror=print()>
```

**Exploit page (served from the exploit server):**
```html
<iframe src="https://TARGET-LAB/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
```

**Result:** When the iframe finished its initial load, the `onload` handler
appended the payload to the hash, triggering a `hashchange` event; jQuery's
`$()` interpreted the new hash as HTML, created the `<img>` element, and its
`onerror` handler fired, calling `print()` in the victim's browser — the
exploit executed successfully.

## Impact

This lab illustrates a more complex, realistic delivery chain than a simple
crafted URL click: it requires understanding both the vulnerable client-side
sink *and* how to construct a working exploit page (iframe + onload trick) to
trigger the vulnerability automatically once a victim visits it, rather than
depending on a single obvious URL parameter.

## Remediation

Never pass user-controllable values like `location.hash` directly into
jQuery's `$()` selector function without first validating that the value is
actually a legitimate selector (e.g. matches an expected format/allowlist) or
using a dedicated method (like `$(document.getElementById(...))`) that
doesn't risk HTML-string interpretation.

## Key Takeaway

This was the most involved DOM XSS lab in this set — it required
understanding jQuery's dual behavior (selector vs. HTML-creation) as the
sink, recognizing an alternate JavaScript function (`print()`) when the
"expected" one is blocked, and constructing a two-step iframe exploit rather
than just modifying a URL parameter directly.
