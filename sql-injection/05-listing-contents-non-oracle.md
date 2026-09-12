# SQL Injection Attack, Listing the Database Contents on Non-Oracle Databases

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Unlike previous labs where the target table and column names were given, this
lab provides no hints. The goal is to independently discover the name of the
table holding usernames/passwords, discover its column names, extract the
data, and log in as `administrator` — entirely through injected queries.

## Vulnerability Overview

Most non-Oracle relational databases (MySQL, PostgreSQL, Microsoft SQL Server)
expose a standard `information_schema` metadata schema that lists every table
and column in the database. If an application is vulnerable to SQL injection,
an attacker can query this metadata schema directly to map out the entire
database structure before extracting any real data.

## Methodology

1. Determined the query returns **2 columns** via `ORDER BY` (failed at 3).
2. Confirmed both columns accept string data with
   `UNION SELECT 'a','a'--` (no `FROM DUAL` needed, ruling out Oracle).
3. Queried the database version using `UNION SELECT @@version, NULL--` and
   identified the engine as **PostgreSQL** from the returned version string.
4. Used the SQL injection cheat sheet's non-Oracle "list all tables" query
   against `information_schema.tables`, filtering for table names likely to
   contain credentials (`LIKE '%user%'`):
   ```
   ' UNION SELECT table_name, NULL FROM information_schema.tables--
   ```
5. Found a table matching the expected naming pattern (e.g. `users_xxxxxx`,
   the lab appends a random suffix to avoid guessable names).
6. Queried `information_schema.columns` filtered by that exact table name to
   list its column names:
   ```
   ' UNION SELECT column_name, NULL FROM information_schema.columns
   WHERE table_name='users_xxxxxx'--
   ```
7. Identified columns matching `username` and `password` in the results.
8. Ran a final query selecting those two columns directly from the discovered
   table:
   ```
   ' UNION SELECT username, password FROM users_xxxxxx--
   ```
9. Located the row for `administrator`, copied the password, and logged in.

## Proof of Concept

**Final data-extraction payload:**
```
' UNION SELECT username, password FROM users_xxxxxx--
```

**Result:** Successfully retrieved and used the administrator's credentials to
log in, having discovered the entire path — table name, column names, and
values — purely through injected metadata queries.

## Impact

This lab demonstrates that a lack of publicly documented schema is not a
meaningful defense: `information_schema` (or engine-equivalent metadata views)
lets an attacker reconstruct the entire database layout from scratch, turning
a single injectable parameter into full database reconnaissance and
extraction capability.

## Remediation

Parameterized queries remain the fix. As defense in depth, restricting the
web application's database account from having read access to
`information_schema` (where the engine allows it) adds a layer of friction,
though it should never be relied on as the primary control.

## Key Takeaway

This was the first lab requiring a full attack chain end-to-end — fingerprint
engine, enumerate tables, enumerate columns, then extract data — rather than
being handed the table/column names directly. It's a much closer simulation
of what a real-world blind assessment looks like.
