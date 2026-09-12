# Stored XSS into HTML Context With Nothing Encoded

**Category:** Cross-Site Scripting (XSS)
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater), Browser
**Status:** ✅ Solved

---

## Objective

The lab contains a stored cross-site scripting vulnerability in the blog
comment functionality. The goal is to submit a comment that calls the
`alert()` function when the blog post is viewed — by anyone, not just the
person who posted it.

## Vulnerability Overview

Unlike reflected XSS (where the payload only affects the person who submits
the request), stored XSS means the malicious input is saved server-side —
here, as a blog comment — and then rendered, unescaped, to **every visitor**
who views that blog post afterward. This makes stored XSS significantly more
dangerous, since a single malicious comment can compromise every subsequent
reader.

## Methodology

1. Navigated to a blog post and opened its comment section ("Leave a
   comment" form: Comment, Name, Email, Website fields).
2. Made sure the browser traffic was routed through Burp Suite (proxy
   enabled) so the comment submission could be intercepted and inspected.
3. Submitted an initial test comment with plain values to see exactly how the
   application structured the POST request and which fields were reflected
   back on the page.
4. Forwarded the intercepted POST request to Burp Repeater, then replaced the
   comment field's value with a `<script>alert()</script>` payload.
5. Reloaded the blog post page in the browser (not just Repeater) to confirm
   the stored comment now renders the injected script for any visitor viewing
   the page, not just in the original request/response cycle.

## Proof of Concept

**Payload submitted in the comment field:**
```html
<script>alert(document.cookie)</script>
```

**Result:** After posting, simply viewing the blog post's comment section
(as any visitor would) triggered the alert automatically — the payload was
stored server-side and rendered unescaped into the page's HTML on every
subsequent load.

## Impact

Stored XSS in a comment section means every visitor who reads that blog
post — not just the attacker — executes the malicious script. This is far
more severe than reflected XSS since it requires no social engineering (no
malicious link needs to be sent); the payload persists and fires
automatically for anyone browsing the content.

## Remediation

HTML-encode all user-submitted content before storing it or, more robustly,
before rendering it back to the page (encode on output, not just on input,
since stored data may be reused in multiple contexts). Comment systems in
particular should never render user input as raw HTML.

## Key Takeaway

This lab made the reflected-vs-stored distinction concrete: the exact same
missing-encoding root cause becomes dramatically more dangerous once the
payload is persisted and served to an unlimited number of future visitors
rather than just the single request that submitted it.
