# SQL Injection Vulnerability Allowing Login Bypass

**Category:** SQL Injection
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Log in to the application as the `administrator` user without knowing their
password, by exploiting a SQL injection flaw in the login form.

## Vulnerability Overview

The login form takes a username and password and uses them directly inside a
backend SQL query to check credentials, without sanitizing or parameterizing the
input. Because the raw input is concatenated straight into the query string, an
attacker can inject SQL syntax that changes the logic of the query itself — for
example, turning a strict "username AND password" check into a condition that is
always true, or commenting out the password check entirely.

## Methodology

1. Intercepted the login POST request in Burp Suite Proxy to see exactly how the
   `username` and `password` parameters were being sent.
2. Sent the request to Repeater to safely experiment with payloads without
   repeatedly submitting the form through the browser.
3. Tested the `username` field with a SQL comment sequence to strip out the rest
   of the query (including the password check).
4. Adjusted the payload until the backend returned a successful authentication
   response instead of an error, confirming the injection worked.

## Proof of Concept

**Payload used in the `username` field:**
```
administrator'--
```

**Password field:** left as any arbitrary value (irrelevant, since the injected
comment removes the password check from the query).

**Result:** The application responded with a successful login as `administrator`,
confirming the backend query was effectively reduced to just checking that a user
named `administrator` exists — the password clause was commented out and never
evaluated.

## Impact

In a real application, this would let an attacker log in as any known user
(including admins) without a password — a direct authentication bypass. Combined
with username enumeration (a separate vulnerability class I also practiced), an
attacker wouldn't even need to know a valid username in advance.

## Remediation

Use parameterized queries / prepared statements so user input is always treated as
data, never executable SQL syntax. Never build queries via raw string
concatenation, regardless of how "trusted" the input source seems.

## Key Takeaway

This lab made it concrete that SQL injection isn't just about "leaking data" — it
can break the authentication logic of an application entirely, since the query
itself IS the security control.

