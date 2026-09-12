# DOM XSS in AngularJS Expression With Angle Brackets and Double Quotes HTML-Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy), Browser
**Status:** ✅ Solved

---

## Objective

The search function reflects user input into a page that uses AngularJS
(via the `ng-app` directive), with angle brackets and double quotes
HTML-encoded. The goal is to execute JavaScript by exploiting AngularJS's
own expression evaluation, without needing any raw `<script>` tags or
unencoded angle brackets at all.

## Vulnerability Overview

AngularJS scans the DOM for the `ng-app` attribute and, when present,
evaluates any content wrapped in double curly braces (`{{ }}`) as a live
AngularJS expression. This means that even if HTML tag injection is fully
blocked by encoding, injecting a value the AngularJS engine itself will parse
and execute is a completely separate, HTML-independent attack surface.

## Methodology

1. Confirmed via page source that the application was using AngularJS
   (`ng-app` attribute present on a container element), and that the search
   term was reflected somewhere within the scope AngularJS actively scans.
2. Confirmed angle brackets and double quotes were HTML-encoded, ruling out
   a direct tag-injection approach.
3. Recalled that AngularJS expressions inside `{{ }}` are evaluated as
   JavaScript-like expressions by the framework itself, independent of
   normal HTML parsing — meaning `{{ }}` syntax alone doesn't require any
   angle brackets or quotes to reach the AngularJS expression evaluator.
4. Since directly calling arbitrary functions isn't allowed by AngularJS's
   expression sandbox in older/newer versions differently, used the known
   `constructor` property chain to reach the JavaScript `Function`
   constructor indirectly: `$on.constructor('alert(1)')()` — where `$on` is
   an AngularJS-related object/function already present in scope, its
   `.constructor` resolves to the JavaScript `Function` constructor, calling
   it with a string creates a new function containing that code, and the
   trailing `()` immediately invokes it.
5. Submitted this expression as the search term and confirmed the alert
   fired.

## Proof of Concept

**Payload used in the search parameter:**
```javascript
{{$on.constructor('alert(1)')()}}
```

**How it works, step by step:**
1. `$on` — an AngularJS-related object/function already reachable in the
   evaluated scope, used as a starting point.
2. `.constructor` — resolves to the underlying JavaScript `Function`
   constructor associated with `$on`.
3. `('alert(1)')` — calling the `Function` constructor with this string
   creates a new function whose body is `alert(1)`.
4. `()` — the trailing parentheses immediately invoke that newly created
   function, executing the `alert(1)` code.

**Result:** AngularJS evaluated the `{{ }}` expression as intended by the
framework, and the expression itself constructed and executed arbitrary
JavaScript — popping the alert despite full HTML encoding of angle brackets
and quotes.

## Impact

This lab demonstrates that frontend frameworks which auto-evaluate embedded
expressions (like AngularJS's `{{ }}` syntax) introduce an entirely separate
code-execution surface from raw HTML injection — an application can encode
every HTML-dangerous character perfectly and still be fully exploitable if
user input reaches a location the framework itself actively parses and
evaluates.

## Remediation

Never reflect unsanitized user input into any DOM region an active frontend
framework directive (like `ng-app`) scans and evaluates. Where possible,
upgrade to AngularJS versions with stricter expression sandboxing (though
sandbox bypasses have historically been found repeatedly), or better, avoid
interpolating raw user input into framework-evaluated regions entirely.

## Key Takeaway

This lab expanded my understanding of DOM XSS again — beyond "sources and
sinks" in vanilla JavaScript, front-end frameworks add their own expression
evaluation layers that can be attacked entirely independently of standard
HTML/JS injection techniques, and the AngularJS `constructor` chain trick is
a good example of "living off the framework" to reach arbitrary code
execution.
