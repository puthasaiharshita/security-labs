# Reflected XSS into a JavaScript String With Single Quote and Backslash Escaped

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

The lab contains a reflected cross-site scripting vulnerability in the search
blog functionality, where the reflection is inside a JavaScript string. This
time, both single quotes and backslashes are escaped by the application. The
goal is to break out of the JavaScript string anyway and call `alert()`.

## Vulnerability Overview

The application appears to defend against the "close the string with a quote"
technique from an earlier lab by escaping both `'` and `\` — meaning a naive
`'-alert(1)-'` payload would have its quote automatically backslash-escaped
by the server, becoming an inert, literal string character instead of
actually terminating the JavaScript string. The bypass requires understanding
that the *order* in which characters are escaped matters, and can be abused.

## Methodology

1. Tested the standard single-quote breakout payload from a previous lab
   (`'-alert(1)-'`) and confirmed it failed — the reflected value showed the
   quote had been escaped to `\'`, meaning it was correctly treated as a
   literal character inside the string rather than terminating it.
2. Realized the escaping was likely done with a simple substitution (adding a
   backslash before every `'` and every existing `\`), which creates an
   exploitable ordering issue: if an attacker submits their **own** trailing
   backslash immediately before the quote they want to use, the server's
   escaping logic escapes the attacker's backslash (turning it into `\\`),
   and the following quote is left un-escaped and free to actually terminate
   the string.
3. Constructed a payload ending in a backslash immediately before the
   closing quote, so the server's own escaping neutralizes the attacker's
   backslash rather than the quote that follows it.
4. Verified in the reflected response that the quote after the backslash was
   no longer escaped, successfully closing the JavaScript string, followed
   by the `alert(1)` call and a fresh string reopened to keep the rest of the
   script syntactically valid.

## Proof of Concept

**Payload used in the search parameter:**
```javascript
\'-alert(1)-'
```

**How this works:** the application escapes the submitted `\` into `\\`
(a literal backslash character), which means the very next character — the
single quote the attacker intended to use as the real string terminator — is
**not** escaped, since the server already "used up" its escaping on the
attacker-supplied backslash instead.

**Resulting script (conceptually):**
```javascript
var searchTerms = '\\'-alert(1)-'';
```

**Result:** The `\\'` sequence closed the string as a literal backslash
character followed by a real, unescaped terminating quote, allowing
`alert(1)` to execute directly in the page's existing script block.

## Impact

This lab shows that naive escaping logic (blindly prepending a backslash to
every quote and every existing backslash) can be turned against itself —
attacker-controlled backslashes can "consume" the escaping mechanism meant to
protect a different character, re-opening the exact injection point the
escaping was supposed to close.

## Remediation

Avoid manually implementing custom escaping logic for JavaScript string
context. Use context-aware, well-tested encoding libraries (e.g. proper
JavaScript string literal encoders) that correctly handle sequences like a
user-supplied trailing backslash, rather than a simple find-and-replace
substitution.

## Key Takeaway

This was the lab that made the "escape the escaper" technique click for
me — realizing that submitting your own backslash right before the character
you actually want to remain unescaped can neutralize a naive escaping
routine, since the routine has no way to distinguish an attacker's backslash
from one it just added itself.
