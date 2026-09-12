# Stored XSS into Anchor href Attribute With Double Quotes HTML-Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy), Browser
**Status:** ✅ Solved

---

## Objective

The comment form's "Website" field is stored and later used as the `href`
value of a link on the comment author's name. Double quotes are
HTML-encoded, so a naive attribute breakout won't work directly — the goal
is still to submit a Website value that calls `alert()` when the author name
is clicked.

## Vulnerability Overview

Since double quotes are encoded, an attacker can't close the existing
`href="..."` attribute and inject a new one. However, the `href` attribute
itself accepts the `javascript:` URI scheme as a valid value — no attribute
breakout is needed at all if the entire attribute value itself can simply
be replaced with executable JavaScript, since the scheme prefix doesn't
require any quotes to be manipulated.

## Methodology

1. Opened the target site's comment section and posted an initial test
   comment to observe how the Website field's value was placed into the
   page — confirmed it was used directly as the `href` attribute on the
   author name link, e.g. `<a href="WEBSITE_VALUE">AuthorName</a>`.
2. Recognized that since double quotes were HTML-encoded, breaking out of
   the attribute wasn't necessary or even useful — instead, simply setting
   the entire attribute value to a `javascript:` URI would let the browser
   execute the code when the link is clicked, without ever needing a quote
   character at all.
3. Submitted the comment with the Website field set to
   `javascript:alert(1)`, leaving other fields with placeholder values.
4. Posted the comment, then clicked on the resulting author name link to
   confirm the injected JavaScript executed.

## Proof of Concept

**Value submitted in the Website field:**
```
javascript:alert(1)
```

**Resulting HTML:**
```html
<a href="javascript:alert(1)">authorname</a>
```

**Result:** Clicking the author's name link executed `alert(1)` directly,
since the browser treats `javascript:` as a valid (if commonly abused) URI
scheme and executes its contents when the link is activated.

## Impact

Because this is stored, the payload persists and affects every visitor who
clicks the malicious comment's author name — not just the one who submitted
it. This lab also demonstrates that encoding quote characters alone doesn't
prevent every `href`-based attack, since some payloads (like `javascript:`
URIs) don't require breaking out of the attribute at all.

## Remediation

Validate that any user-supplied URL used in an `href` attribute begins with
an expected, safe scheme (e.g. `http://` or `https://` only), explicitly
rejecting `javascript:`, `data:`, and other executable URI schemes — quote
encoding alone is not sufficient protection for URL-context attributes.

## Key Takeaway

This lab was a useful reminder that not every attribute-based XSS requires
breaking out of the attribute value — sometimes the attribute itself accepts
a dangerous value directly (like a `javascript:` URI in `href`), which
sidesteps quote-encoding defenses entirely.
