# SQL Injection Vulnerability in WHERE Clause Allowing Retrieval of Hidden Data

**Category:** SQL Injection
**Difficulty:** Apprentice
**Tools:** Burp Suite Community Edition (Proxy, Repeater), Browser
**Status:** ✅ Solved

---

## Objective

The product category filter builds a query like:
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`
The goal is to inject SQL that causes the application to display one or more
**unreleased** products, which the `released = 1` condition should normally hide.

## Vulnerability Overview

The category value from the URL/query parameter is inserted directly into the
SQL query's `WHERE` clause with no sanitization. Since the entire clause is just
a string comparison the attacker controls, it's possible to break out of the
intended `category = '...'` condition and rewrite the logic of the query itself
— including neutralizing the `AND released = 1` check that hides unreleased
products.

## Methodology

1. Submitted a single `'` character in the category parameter to confirm the
   input reaches the SQL query unescaped — this returned an internal server
   error, confirming the injection point.
2. Tested a few intermediate payloads to understand how the query was being
   built:
   - `''` → no products shown (category becomes an empty string, matches nothing)
   - `'--` → also nothing displayed, since everything after `--` was commented
     out, including the `AND released = 1` check, but the category itself no
     longer matched anything real
3. Realized the goal wasn't just to remove the `released` check, but to make
   the `WHERE` clause evaluate to true for **every row**, so all products
   (including unreleased ones) would be returned regardless of category.
4. Used `OR 1=1` to inject a condition that is always true, then commented out
   the rest of the original query with `--` so the trailing `AND released = 1`
   was never evaluated.

## Proof of Concept

**Payload used in the category parameter:**
```
' OR 1=1--
```

**Resulting query (conceptually):**
```sql
SELECT * FROM products WHERE category = '' OR 1=1--' AND released = 1
```

**Result:** Since `1=1` is always true, the `OR` condition made the entire
`WHERE` clause true for every row in the table, and the trailing `AND released = 1`
was commented out and never applied — the application displayed all products,
including unreleased ones.

## Impact

In a real application, this kind of injection could expose any data the
`WHERE` clause was meant to restrict — not just unreleased products, but
potentially private records, other users' data, or admin-only content,
depending on what the underlying query is filtering.

## Remediation

Use parameterized queries (prepared statements) so the category value is always
treated as a literal string value, never as part of the executable SQL syntax.
This prevents `'`, `--`, and `OR` from being interpreted as anything other than
plain text.

## Key Takeaway

This lab was the clearest illustration of the core SQLi mechanic: closing the
original string early (`'`), injecting a condition that's always true (`OR 1=1`),
and commenting out the rest of the query (`--`) — a pattern that shows up
repeatedly across almost every SQL injection variant.
