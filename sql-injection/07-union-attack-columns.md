# SQL Injection UNION Attack, Determining the Number of Columns Returned by the Query

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Before any UNION-based SQL injection attack can work, the injected `UNION SELECT`
must return exactly the same number of columns as the original query. The goal
of this lab is simply to determine that number using the product category
filter as the injection point.

## Vulnerability Overview

A `UNION SELECT` only succeeds if it returns the same column count (and
compatible data types) as the original query. Since the application doesn't
reveal the original query's structure, the column count has to be inferred
through the database's own error behavior — either via `ORDER BY` or via
trial-and-error `UNION SELECT NULL` attempts.

## Methodology

**Approach 1 — ORDER BY:**
1. Injected `' ORDER BY 1--` and increased the number each time.
2. `ORDER BY 1`, `ORDER BY 2` returned normal pages (columns 1 and 2 exist).
3. `ORDER BY 3` triggered an internal server error, meaning the query only
   returns 2 columns — ordering by a non-existent 3rd column fails.

**Approach 2 — UNION SELECT NULL (used to confirm):**
1. Injected `' UNION SELECT NULL--` — this only works if the original query
   returns exactly 1 column; here it produced an "incorrect number of columns"
   error, meaning the query returns more than 1.
2. Injected `' UNION SELECT NULL,NULL--` — this succeeded and returned an
   additional row full of `NULL` values, confirming the query returns exactly
   2 columns.
3. Verified in Burp Repeater by resending the request with the working payload
   and checking the response for the extra all-NULL row.

**Why `NULL` specifically:** `NULL` is valid for (and implicitly compatible
with) any data type, so it sidesteps data-type mismatch errors and isolates
the test to just the column *count*.

## Proof of Concept

**Working payload:**
```
' UNION SELECT NULL,NULL--
```

**Result:** HTTP 200 response with an extra row of `NULL` values appended to
the product listing, confirming the original query returns 2 columns.

## Impact

This step alone has no direct impact, but it's the mandatory first step for
every UNION-based data extraction attack — without the correct column count,
none of the later UNION attacks (pulling usernames, passwords, or other table
data) will execute.

## Remediation

Same as any SQL injection: use parameterized queries so user input can never
be interpreted as SQL syntax, which prevents `ORDER BY` and `UNION SELECT`
injection entirely.

## Key Takeaway

`ORDER BY` is often the faster way to fingerprint column count (binary-search
style, fewer requests), while incrementing `UNION SELECT NULL` is a good
sanity check to confirm the number found is actually correct before moving on
to real data extraction.
