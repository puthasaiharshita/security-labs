# SQL Injection UNION Attack, Retrieving Data from Other Tables

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Combine the techniques from the previous labs to pull data out of a
**completely different table** than the one the original query targets.
Specifically: extract usernames and passwords from a `users` table and use
them to log in as the `administrator`.

## Vulnerability Overview

A UNION-based SQL injection isn't limited to the table the original query
references — as long as the column count and types line up, `UNION SELECT`
can pull from any table the database user has access to. This is what turns a
"harmless" filter injection into a full data-extraction vector across the
entire database.

## Methodology

1. Determined the number of columns returned by the original query using
   `ORDER BY` — found it to be **2** columns.
2. Confirmed both columns accept string data by testing
   `UNION SELECT 'a','a'--`, which succeeded without error.
3. Since the lab specified the target table (`users`) and columns
   (`username`, `password`), constructed a UNION query pulling directly from
   that table instead of `products`.
4. Sent the payload and read the returned username/password pairs directly
   off the product listing page (they appeared as if they were product
   names/descriptions, in the position of the string-compatible columns).
5. Took the row showing `administrator` as the username, copied the
   accompanying password, and logged in through the normal login form.

## Proof of Concept

**Working payload:**
```
' UNION SELECT username, password FROM users--
```

**Result:** The page displayed every username/password pair from the `users`
table inline with the normal product listing. The row for `administrator`
revealed the password `8cg031dos8dej20clyr0` (lab-generated, single-use
value), which was then used to log in successfully as the administrator.

## Impact

This is the point where a UNION SQLi stops being a "display bug" and becomes a
full credential-harvesting vulnerability. In a real system, this means an
attacker with a single injectable parameter could dump every user's
credentials — including admin accounts — directly from the front-end response,
no separate database access required.

## Remediation

Parameterized queries remain the primary fix. Defense in depth should also
include the principle of least privilege on the database account the web app
uses (it should not have read access to tables — like `users` with plaintext
or reversible passwords — it doesn't need for its own queries), and passwords
should always be hashed with a strong, salted algorithm so even direct table
access doesn't yield usable credentials.

## Key Takeaway

This lab made the "UNION attack" concept fully concrete: the injection point
doesn't have to be anywhere near the sensitive data — as long as column count
and type line up, any table in the database is fair game.
