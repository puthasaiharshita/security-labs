# Reflected XSS into a Template Literal With Angle Brackets, Single, Double Quotes, Backslash and Backticks Unicode-Escaped

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

The reflection here occurs inside a JavaScript **template literal**
(a string surrounded by backticks, e.g. `` `hello` ``) rather than a
traditional single- or double-quoted string. Angle brackets, both quote
types, backslashes, and even the backtick characters themselves are all
Unicode-escaped. The goal is still to break out and call `alert()`.

## Vulnerability Overview

Template literals support a feature regular strings don't: **expression
interpolation** using `${...}`. Anything inside `${}` is evaluated as live
JavaScript and its result is inserted into the string — this happens
regardless of whether the surrounding backticks, quotes, or angle brackets
are escaped, since `${}` itself isn't a quote character and therefore isn't
part of what the encoding scheme was protecting against.

## Methodology

1. Confirmed the reflection point was inside a template literal (backtick
   string) by viewing the page source, rather than a regular single/double
   quoted string as in earlier labs.
2. Noted that angle brackets, single quotes, double quotes, backslashes, and
   even backticks were all being Unicode-escaped by the application —
   meaning none of the previous "break out with a quote" or "backslash
   trick" approaches from earlier labs would work here, since there's no
   unescaped character available to terminate the string.
3. Recognized that template literals don't require breaking out of the
   string at all to execute code — the `${}` syntax lets you embed and
   execute a JavaScript expression directly **inside** the existing string,
   without ever needing an unescaped backtick, quote, or angle bracket.
4. Constructed a payload using `${alert(1)}`, relying entirely on the
   template literal's built-in expression syntax rather than any
   string-breakout technique.
5. Submitted the payload in the search bar and confirmed the alert fired.

## Proof of Concept

**Payload used in the search parameter:**
```javascript
${alert(1)}
```

**Resulting template literal (conceptually):**
```javascript
var message = `hello ${alert(1)}`;
```

**Result:** The browser evaluated the `${alert(1)}` expression as live
JavaScript embedded inside the template literal, executing `alert(1)`
regardless of the fact that every quote/bracket character was properly
escaped — because no escaping of those characters was actually needed for
this technique.

## Impact

This lab demonstrates that character-based escaping schemes (however
thorough) are incomplete if they don't account for language features beyond
string termination — template literal interpolation is a completely
separate code-execution path that doesn't rely on breaking out of the
string at all.

## Remediation

Never place user-controlled input inside a JavaScript template literal
without either strict output encoding specifically designed to neutralize
`${` sequences, or (better) avoiding template literals for untrusted data
entirely in favor of safe DOM APIs like `textContent`.

## Key Takeaway

This was a genuinely different mental model from every previous XSS lab in
this set: instead of finding an unescaped character to break out of a
string, the vulnerability here is a built-in language feature (template
literal interpolation) that executes code without ever needing to "escape"
anything at all.
