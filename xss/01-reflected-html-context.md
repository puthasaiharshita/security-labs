# Reflected XSS into HTML Context With Nothing Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

The lab contains a simple reflected cross-site scripting vulnerability in the
search functionality. The goal is to perform a cross-site scripting attack
that calls the `alert()` function.

## Vulnerability Overview

The search term submitted by the user is reflected directly back into the
page's HTML response with no encoding or sanitization applied. Since the
browser parses whatever is in the response body as real HTML, any script tag
submitted in the search box is executed exactly as if it were part of the
original page.

## Methodology

1. Accessed the lab and intercepted the search request with Burp Suite's
   proxy, then sent the request to Repeater to test payloads without
   repeatedly submitting the search form through the browser.
2. In Repeater, checked exactly how and where the search term ("test") was
   reflected in the raw HTML response, to confirm the reflection point was in
   the page body and not inside an attribute or script block.
3. Replaced the search term with a `<script>` payload and resent the request.
4. Right-clicked the response in Repeater and used "Copy URL" to get the full
   URL with the payload already embedded in the query string.
5. Pasted the copied URL into the browser to trigger the payload in a real
   page load.

## Proof of Concept

**Payload used in the search parameter:**
```html
<script>alert(39)</script>
```

**Request:**
```
GET /?search=<script>alert(39)</script> HTTP/2
```

**Result:** The browser executed the injected script on page load, popping a
JavaScript alert box with the value `39`, confirming the search parameter is
vulnerable to reflected XSS with no output encoding at all.

## Impact

In a real application, an attacker could craft a malicious search URL like
this and send it to a victim (via email, chat, etc.). As soon as the victim
opens it, the script executes in their browser under the site's own origin —
meaning it could steal session cookies, perform actions as the victim, or
redirect them to a phishing page.

## Remediation

HTML-encode all user-controlled output before writing it into the page
(encode `<`, `>`, `&`, `"`, `'`) so that a submitted `<script>` tag is
rendered as inert, visible text rather than being parsed as executable HTML.

## Key Takeaway

Using Burp Repeater to test payloads first (rather than repeatedly submitting
the search form in the browser) made it much faster to confirm the injection
point and refine the exact payload before ever loading it in a real page —
and copying the URL directly from Repeater's response view was the quickest
way to reproduce the exploit in the browser afterward.
