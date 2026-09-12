# Reflected DOM XSS

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser DevTools
**Status:** ✅ Solved

---

## Objective

This lab demonstrates a reflected **DOM** vulnerability, where user input
from the request is echoed back into the response and then processed
client-side by JavaScript that ultimately reaches a dangerous sink —
specifically, the sink here is `eval()`, a function that executes whatever
string is passed to it as live JavaScript code. The goal is to construct an
injection that calls `alert()`.

## Vulnerability Overview

An external JavaScript file makes an AJAX request to a search-results
endpoint, and once results come back, wraps them in a JSON structure and
passes that structure through `eval()` — rather than using a safe JSON
parser like `JSON.parse()`. Since `eval()` executes any valid JavaScript
handed to it, and the search term itself is embedded directly into a string
being built for that `eval()` call, an attacker who can control the search
term can break out of the intended JSON string and inject arbitrary
executable JavaScript instead.

## Methodology

1. Reviewed the site's external JavaScript file (`searchResults.js`) and
   found an AJAX request handler that took search results and passed them
   through `eval()`, constructing a JSON-like string manually via
   concatenation: `eval('searchResultsObj = {"searchTerm":"' +
   searchTerm + '", "results":[]}')`.
2. Since the raw `searchTerm` value is concatenated directly into a string
   destined for `eval()`, tested submitting a search term containing a
   double quote to see if the surrounding string could be broken.
3. Confirmed via the browser's Network tab that the raw search term was
   reflected unescaped in the response, meaning any quotes or backslashes in
   the input reached the `eval()` call exactly as submitted.
4. Since a plain `alert(1)` payload alone would break the JSON syntax the
   application expected afterward (the trailing `, "results":[]}` needed to
   still parse), first tried a naive double-quote break, then adjusted:
   used a payload ending in a properly placed backslash and comment
   sequence to both execute the alert and cleanly discard/comment out the
   remaining JSON structure so `eval()` didn't throw a syntax error
   afterward.
5. Refined the payload to `\"-alert(1)}//`, verified it against the actual
   application logic (noting the app also escaped literal double quotes it
   received, turning a submitted `"` into `\"` — but a submitted backslash
   was **not** further escaped, letting the same "attacker-supplied
   backslash absorbs the escaping" trick from earlier JS-string labs apply
   here too).
6. Submitted the refined payload and confirmed the alert executed.

## Proof of Concept

**Payload used in the search parameter:**
```
\"-alert(1)}//
```

**Why this works:** the application automatically escapes any double quote
in the input (`"` → `\"`), but does **not** further escape an
attacker-submitted backslash. By submitting our own leading backslash before
the quote, the resulting sequence resolves (from the JavaScript parser's
perspective) as an escaped backslash followed by an unescaped, real
string-terminating quote — the same underlying trick used against
JavaScript-string contexts elsewhere in this series, just landing inside an
`eval()` sink instead of a plain inline script block. The trailing `}//`
closes the object literal and comments out anything the application
appended afterward, keeping the overall `eval()` call syntactically valid.

**Result:** `eval()` executed the injected `alert(1)` as part of evaluating
what the application believed was safe, self-constructed JSON — confirming
the reflected DOM XSS via the unsafe `eval()` sink.

## Impact

`eval()` is one of the most dangerous JavaScript sinks precisely because it
treats its argument as fully executable code, not data — any string
concatenation involving user input that reaches `eval()` is a direct code
execution vulnerability, arguably more severe and less forgiving than
HTML-injection-based XSS, since there's no HTML parsing step to add any
friction at all.

## Remediation

Never use `eval()` (or `new Function()`) to parse data that should be JSON —
use `JSON.parse()` instead, which only ever produces data structures and
never executes arbitrary code, regardless of what a malicious string
contains.

## Key Takeaway

This lab tied together two ideas from earlier in the series: the
"attacker-supplied backslash defeats naive escaping" trick, and the general
principle that any sink treating a string as executable code (`eval`,
`Function`, `setTimeout` with a string argument, etc.) is exponentially more
dangerous than a sink that merely renders HTML.
