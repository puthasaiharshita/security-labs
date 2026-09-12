# Stored XSS into onclick Event With Angle Brackets, Double Quotes HTML-Encoded, Single Quotes and Backslash Escaped

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser
**Status:** ✅ Solved

---

## Objective

The lab contains a stored cross-site scripting vulnerability in the comment
functionality. The submitted "Website" value is later used inside an
`onclick` JavaScript handler on the comment author's name. Angle brackets,
double quotes, single quotes, and backslashes are all filtered or escaped —
the goal is still to call `alert()` when the author name is clicked.

## Vulnerability Overview

The website URL is inserted into an `onclick` attribute that calls a
JavaScript function with the URL as a quoted string argument. Since single
quotes are escaped as the literal characters `\'` (or blocked outright as raw
input), a direct string-breakout using `'` doesn't work. However, the
application encodes single quotes using the **HTML entity** `&apos;` instead
of blocking them — and critically, the browser **HTML-decodes** attribute
values (like `onclick="..."`) *before* handing the resulting string to the
JavaScript parser. This means `&apos;` becomes a real `'` character from the
JavaScript engine's point of view, even though it was never a literal quote
in the raw HTML source the filter inspected.

## Methodology

1. Submitted a comment with a plain URL in the Website field and inspected
   the reflected HTML, finding it placed inside an `onclick` handler that
   called a JavaScript function with the URL as a single-quoted string
   argument.
2. Tested a direct single-quote breakout payload in the Website field and
   confirmed it was blocked/escaped by the application, ruling out a literal
   `'` character in the submitted value.
3. Recognized that since the *rendered output* only needs to contain a
   literal single quote from the **browser's HTML-parsing perspective**
   (before JS execution), the HTML entity `&apos;` could be submitted
   instead — the filter, which likely checks for the literal `'` character,
   would not flag `&apos;` as a match, but the browser decodes HTML entities
   in attribute values before the JavaScript engine ever sees the string.
4. Constructed the Website field value using `&apos;` to close the intended
   JavaScript string inside the `onclick` handler, followed by `-alert(1)-`,
   and another `&apos;` to reopen a dummy string, keeping the rest of the
   `onclick` handler's syntax valid.
5. Posted the comment, then clicked on the author's name on the resulting
   page to trigger the `onclick` handler and confirm the alert fired.

## Proof of Concept

**Value submitted in the Website field:**
```
http://foo?&apos;-alert(1)-&apos;
```

**Resulting HTML (conceptually):**
```html
<a href="..." onclick="viewProfile('http://foo?'-alert(1)-'')">AuthorName</a>
```

**How this bypasses the filter:** the raw submitted value contains no literal
`'` character (only the harmless entity `&apos;`), so any filter checking for
literal single quotes in the input passes it through — but the browser
resolves `&apos;` into an actual `'` when parsing the `onclick` attribute's
HTML, handing the JavaScript engine a string that *does* contain real quote
characters.

**Result:** Clicking the author's name on the comment executed
`alert(1)`, confirming the stored XSS payload successfully broke out of the
`onclick` string context via HTML entity decoding.

## Impact

Since this is a **stored** vulnerability, every visitor who clicks the
malicious comment's author name — not just the original attacker — triggers
the payload, making this significantly more dangerous than a reflected
equivalent. It also demonstrates that filtering literal characters is
insufficient when the browser will decode equivalent HTML entities before
the value reaches its actual execution context.

## Remediation

Escaping/filtering logic must account for **all** representations of a
dangerous character — including HTML entities, URL encoding, and Unicode
escapes — not just the literal character itself, since browsers routinely
decode these forms before further processing (like handing an attribute
value to the JavaScript engine). Ideally, avoid placing user-controlled data
inside inline event-handler attributes entirely; use safer patterns like
`addEventListener` with properly escaped or validated data.

## Key Takeaway

This was the clearest demonstration in the whole series that "the filter
blocks the literal character" is not the same as "the browser will never see
that character" — HTML entity decoding happens as a normal part of attribute
parsing, well before JavaScript ever runs, creating a gap that a
character-literal filter can't close on its own.
