# Stored DOM XSS

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

The blog's comment functionality has a stored DOM-based XSS vulnerability.
The application does attempt to sanitize comments client-side using a
custom `escapeHTML()` function before rendering them — the goal is to find a
gap in that sanitization logic and submit a comment that calls `alert()`
when the comment section is later loaded and rendered by any visitor.

## Vulnerability Overview

The client-side code fetches stored comments and passes them through a
custom `escapeHTML()` function meant to neutralize dangerous characters
before inserting them into the page via `innerHTML`. However, the
`escapeHTML()` implementation here has an incomplete replace pattern: it
correctly replaces the **first** occurrence of a dangerous character (like
`<`) in a given string but fails to replace **subsequent** occurrences of
that same character within the same string — a classic single-pass
`.replace()` bug (using `String.replace()` without the global flag, or
similar faulty logic) rather than a genuinely global sanitization pass.

## Methodology

1. Reviewed the site's JavaScript (via Network/Sources tab) and found a
   `loadCommentsFromDom()`-style function fetching comments, then rendering
   them via `innerHTML` after passing them through a custom `escapeHTML()`
   function.
2. Inspected `escapeHTML()`'s implementation and found it replaced `<` with
   `&lt;` and `>` with `&gt;`, but — critically — used `.replace()` without a
   global flag (or an equivalent single-pass bug), meaning only the
   **first** `<` and the **first** `>` in the input string were actually
   escaped; any additional `<`/`>` characters later in the same string
   passed through completely untouched.
3. Realized the exploit strategy: submit a comment containing **two**
   angle-bracket-opened tags — the first one deliberately "sacrificial" (its
   `<` gets escaped and neutralized by the buggy function, harmlessly), and
   a second one placed later in the same string, whose `<` survives
   untouched because the sanitizer had already "used up" its one
   replacement on the first occurrence.
4. Constructed a payload with a throwaway opening `<` early in the comment
   (e.g. `<`), followed later by the real payload:
   `<img src=1 onerror=alert(1)>`, ensuring the real payload's `<` is the
   **second** occurrence in the string and therefore survives the flawed
   `escapeHTML()` call unescaped.
5. Submitted the comment and reloaded the page to confirm the payload
   rendered and executed as live HTML for any visitor viewing the comments.

## Proof of Concept

**Payload submitted in the Comment field:**
```html
<><img src=1 onerror=alert(1)>
```

**How it works:** the sanitizer's single-pass replace neutralizes only the
**first** `<` it encounters in the string (here, the standalone throwaway
`<`), leaving the **second** `<` — which begins the real
`<img src=1 onerror=alert(1)>` payload — completely unescaped and rendered
as live HTML.

**Result:** Simply viewing the blog post's comment section triggered the
`onerror` handler on the broken image automatically, executing `alert(1)`
for any visitor — confirming a successful bypass of the client-side
`escapeHTML()` sanitization via its single-pass replacement bug.

## Impact

Since this is stored, every visitor to the comment section executes the
payload automatically. This lab is also a strong illustration of why
hand-rolled sanitization functions are risky: a seemingly reasonable
`escapeHTML()` implementation had a subtle single-pass bug that fully
undermined its purpose, and the bug was only exploitable by understanding
the sanitizer's exact internal logic rather than guessing at generic
bypasses.

## Remediation

Never write custom HTML-escaping logic by hand — use well-tested, actively
maintained sanitization libraries (e.g. DOMPurify) instead. If custom
escaping is unavoidable, ensure replacement operations are genuinely global
(e.g. using the `g` flag with `.replace()`, or a loop that fully re-scans
the string) rather than relying on a single pass that can be defeated by
multiple occurrences of the same character.

## Key Takeaway

This lab was a strong reminder to actually read the sanitization function's
source code rather than assuming "there's an escapeHTML() function, so
`<`/`>` are safe" — the exact implementation detail (single-pass vs. global
replace) was the entire vulnerability, and this kind of subtle logic bug is
exactly what a real code review for XSS should be looking for.
