# SQL Injection UNION Attack, Retrieving Multiple Values in a Single Column

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Extract both a username and a password from the `users` table, but this time
the original query only returns **one** string-compatible column — meaning
both values have to be squeezed into a single column position and displayed
on the same page, then used to log in as `administrator`.

## Vulnerability Overview

This lab is a variation on the standard UNION data-extraction attack: instead
of having two separate string columns available (one for username, one for
password), only one column can render text. The solution is to concatenate
both values together into a single string using the database's own string
concatenation syntax — but that syntax differs by database engine, so the
underlying database type has to be identified first.

## Methodology

1. Determined the query returns **2 columns total**, but only **one** of them
   is a usable string/text column (confirmed via the `ORDER BY` and
   `UNION SELECT NULL,'a'` probing technique from earlier labs).
2. Since both username and password needed to fit in that one string column,
   researched the SQL injection cheat sheet's **database version** queries to
   identify which engine was in use — found this database returned a version
   string identifying it as **PostgreSQL**.
3. Looked up PostgreSQL's specific string concatenation operator (`||`) from
   the cheat sheet, since concatenation syntax varies by engine (e.g. MySQL
   uses `CONCAT()`, Microsoft/PostgreSQL use `||` or `+`).
4. Built a UNION query concatenating `username`, a separator character (space,
   for readability), and `password` into the single available string column.

## Proof of Concept

**Database version query used:**
```
' UNION SELECT NULL, @@version--
```
*(used earlier to identify the engine — for PostgreSQL, `version()` was the
correct call: `UNION SELECT NULL, version()--`)*

**Final working payload:**
```
' UNION SELECT NULL, username || ' * ' || password FROM users--
```

**Result:** The page displayed every username and password pair concatenated
together in the single available text column (e.g.
`administrator ~ 8cg031dos8dej20clyr0`), which was then used to log in as
administrator.

## Impact

Same fundamental impact as any UNION-based credential extraction — full
username/password disclosure — but this lab demonstrates that even a
constrained injection point (only one usable output column) doesn't prevent
full data exfiltration; it just requires an extra concatenation step.

## Remediation

Parameterized queries eliminate this entire attack class regardless of how
many string columns are available, since the injected SQL syntax (including
`||` concatenation) would never be interpreted as executable code.

## Key Takeaway

This lab showed that a limited number of "usable" output columns is not a
real defense — concatenation just becomes another tool in the attacker's
UNION-attack toolkit. It also reinforced the value of the SQLi cheat sheet for
quickly identifying engine-specific syntax (version queries, concatenation
operators) rather than guessing.
