# Visible Error-Based SQL Injection

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Unlike the fully blind labs, this application **does** return detailed
database error messages directly on the page. The goal is to exploit this by
deliberately triggering type-conversion errors that leak actual data values
(the administrator's password) inside the error message itself, then use
that password to log in.

## Vulnerability Overview

Some databases, when a type conversion fails (e.g. trying to cast a string
value into an integer), include the offending value directly in the resulting
error message. If an attacker can force a subquery's result into a type
conversion function, the database will "helpfully" print that subquery's
result as part of the error — turning error messages into a full data
exfiltration channel, no blind/boolean guessing required.

## Methodology

1. Intercepted a request (via a product page) and sent it to Repeater to
   check for injectability in the `TrackingId` cookie.
2. Added a payload designed to break the query using unbalanced quotes,
   confirming the app returned a **generic** internal server error (no detail)
   for a malformed query — so the raw injection point alone wasn't leaking data.
3. Tested a payload combining the injection with an explicit type-cast
   attempt: forcing a string result into an integer conversion function
   (`CAST` in some engines, or an implicit conversion trigger depending on the
   database).
4. On a correctly malformed cast attempt, the application returned a **more
   detailed** error message than the generic one — specifically an
   "invalid input syntax for type integer" style error that embedded the
   actual string value it failed to convert.
5. Since the goal was to leak the administrator's password, replaced the
   forced-fail value with a subquery selecting the password itself, so the
   database would attempt to cast the *password value* to an integer, fail,
   and print the password directly in the error message.
6. Read the leaked password straight out of the verbose error response and
   logged in as `administrator`.

## Proof of Concept

**Payload forcing the password into a failed type cast:**
```sql
' AND 1=CAST((SELECT password FROM users WHERE username='administrator')
AS int)--
```

**Result:** The application returned a detailed database error resembling:
`ERROR: invalid input syntax for type integer: "<the actual password value>"`
— the password was extracted directly from the error text itself, with no
need for any blind/boolean iteration.

## Impact

Verbose database error messages turn error-based SQL injection into one of
the fastest and most severe SQLi variants — a single well-crafted request can
exfiltrate an arbitrary value with no automation or Intruder required, unlike
the many-request blind techniques used in the previous labs.

## Remediation

Two layers matter here: (1) parameterized queries prevent the injection
entirely, and (2) regardless of query safety, applications should **never**
return raw database error messages to end users — catch exceptions server-side
and return a generic error page, logging full details only internally.

## Key Takeaway

Comparing this lab directly against the two blind labs made the value of
error suppression obvious: the exact same underlying vulnerability class
(SQL injection) went from "requires hundreds of Intruder requests to extract
one password" to "one request, instant full disclosure" purely because of how
verbose the error handling was.
