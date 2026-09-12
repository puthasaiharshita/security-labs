# Reflected XSS into a JavaScript String With Angle Brackets and Double Quotes HTML-Encoded and Single Quotes Escaped

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

This lab layers multiple defenses at once: angle brackets and double quotes
are HTML-encoded, and single quotes are backslash-escaped (this time
correctly, unlike the ordering flaw in the previous lab). The goal is still
to break out of the reflected JavaScript string and call `alert()`.

## Vulnerability Overview

Since the single-quote escaping in this lab is implemented correctly (no
reusable ordering bypass like the previous lab), the string can't be
terminated with a literal quote character at all. Instead, this lab requires
using a character the escaping logic doesn't account for: an actual
**backslash character in the input itself**, submitted directly (not as part
of an escape sequence), to interfere with how the browser's JavaScript
parser interprets the characters that follow.

## Methodology

1. Confirmed angle brackets and double quotes were HTML-encoded (ruling out
   both a fresh `<script>` tag and attribute-based breakout), and confirmed
   single quotes were properly escaped this time — the previous lab's
   backslash-ordering trick did not work here.
2. Recognized the goal wasn't to terminate the string with an unescaped
   quote, but to use the **backslash's own meaning inside JavaScript
   string literals**: a backslash directly preceding another backslash in a
   JS string produces a single literal backslash character (`\\` → `\`) —
   and critically, if the attacker submits a single backslash right before
   the quote the server escapes, the server turns it into `\\'`.
   JavaScript's parser then reads that sequence as: an escaped backslash
   (`\\`) followed by an **unescaped** quote (`'`) — since the server's own
   `\` was consumed pairing with the attacker's `\`, leaving the actual
   string-terminating quote free.
3. Verified this differs subtly from the previous lab's approach: here, the
   application correctly escapes quotes generally, but this particular
   double-backslash trick still works because the browser's JS parser
   resolves `\\` as one literal backslash *before* considering what follows
   it — meaning the quote right after is parsed as a real terminator by the
   browser, even though server-side it was technically "escaped" in
   isolation.
4. Confirmed the payload closed the string, executed `alert(1)`, and
   reopened a dummy string to keep the remaining script syntactically valid.

## Proof of Concept

**Payload used in the search parameter:**
```javascript
\'-alert(1)-'
```

**Result:** The browser's JavaScript parser resolved the escaped backslash
sequence as a single literal backslash, exposing the following quote as an
actual, unescaped string terminator from the parser's perspective — allowing
`alert(1)` to execute despite the server's quote-escaping logic technically
having run.

## Impact

This lab reinforced that string-escaping bugs aren't just about "is the quote
escaped or not" — subtle interactions between backslash sequences and how
the browser's parser resolves them can still create an exploitable gap, even
when the escaping logic looks correct at first glance.

## Remediation

Rely on standard, well-tested JavaScript string-encoding libraries rather
than manual escaping logic, since correctly handling every backslash/quote
interaction by hand is genuinely difficult to get right — as this lab
demonstrates even "correct-looking" custom escaping can still be bypassed.

## Key Takeaway

This lab and the previous one, taken together, taught me to always test
backslash-based payloads specifically against JavaScript string escaping,
since backslash's dual role (escape character *and* literal character) makes
it a uniquely tricky case that's easy to get subtly wrong in custom
sanitization code.
