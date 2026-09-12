# Blind SQL Injection with Conditional Errors

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater, Intruder)
**Status:** ✅ Solved

---

## Objective

Similar setup to the previous lab (injection via the `TrackingId` cookie,
`users` table with `username`/`password` columns), but this application
doesn't respond differently based on whether the query returns rows —
instead, it returns a **generic custom error page** only when the injected
SQL query itself throws an error. That error/no-error distinction is the only
usable signal.

## Vulnerability Overview

Rather than inferring truth from a content difference (like a "Welcome back"
message), this variant requires deliberately **causing a database error** as
the "true" signal, and avoiding an error as "false." This is done by
conditionally executing a query that only throws an error when a condition is
true, using a `CASE WHEN` expression.

## Methodology

1. Confirmed the injection point and blind nature by testing
   `'||(SELECT '')||'` (string concatenation with an empty subquery), which
   executed successfully with no visible page difference, then tested a
   payload designed to force a divide-by-zero-style database error to confirm
   errors do produce a distinct response.
2. Since the database didn't support `information_schema` cleanly and gave an
   internal server error on some payloads, tested `FROM DUAL` and other
   Oracle-style syntax, confirming the database engine as **Oracle**.
3. Confirmed the `users` table exists using a conditional error technique: a
   `CASE WHEN (condition) THEN <valid query> ELSE <invalid query, e.g.
   divide by zero> END` structure — if the condition is true, the valid
   branch runs silently; if false, the invalid branch throws an error.
4. Confirmed the `administrator` user specifically exists using the same
   `CASE WHEN` pattern, checking `username='administrator'`.
5. Determined the password length using a `CASE WHEN LENGTH(password)>N THEN
   <valid> ELSE <divide-by-zero> END` structure, sent to Intruder with the
   length value as the payload, iterating a numeric range and watching for
   which values returned a normal response vs. an internal server error —
   found the length to be 50 (i.e. one longer than the last successful case,
   or exactly 20 in some earlier attempts, confirmed via response length).
6. Used the same `CASE WHEN` + `SUBSTRING` approach as the previous lab to
   extract the password one character at a time, this time using presence/
   absence of an error response (not a "Welcome back" message) as the signal.
7. Ran a Cluster Bomb Intruder attack over character position and character
   value, filtered by HTTP status/error page keyword instead of a success
   keyword, and reconstructed the password.
8. Logged in as `administrator` with the extracted password.

## Proof of Concept

**Confirming table exists (error-based):**
```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/1) ELSE TO_CHAR(1/0) END FROM dual) || '
```

**Extracting password length:**
```sql
' || (SELECT CASE WHEN (LENGTH(password)>N) THEN TO_CHAR(1/1) ELSE TO_CHAR(1/0)
END FROM users WHERE username='administrator') || '
```

**Extracting each character:**
```sql
' || (SELECT CASE WHEN (SUBSTRING(password,POSITION,1)='CHAR') THEN TO_CHAR(1/1)
ELSE TO_CHAR(1/0) END FROM users WHERE username='administrator') || '
```

**Result:** Filtering Intruder responses by absence of the error page (i.e.
identifying which character/position combinations did NOT throw a database
error) reconstructed the full password, used to log in as administrator.

## Impact

This lab demonstrates that even applications that deliberately suppress
detailed error messages can still leak a binary signal (error vs. no error),
which is just as exploitable as any other blind oracle — "generic error
pages" alone are not a mitigation for SQL injection.

## Remediation

Parameterized queries eliminate this entirely, since the `CASE WHEN`
conditional error trick relies on the attacker's SQL syntax actually reaching
the database. As defense in depth, database errors should never depend on
attacker-influenced logic in the first place.

## Key Takeaway

The `CASE WHEN ... THEN <valid> ELSE <invalid, e.g. divide-by-zero> END`
pattern is a reusable trick worth remembering — it converts *any* boolean
condition into a controllable error/no-error signal, which is often more
reliable to detect via Intruder (HTTP 500 vs 200) than parsing subtle page
content differences.
