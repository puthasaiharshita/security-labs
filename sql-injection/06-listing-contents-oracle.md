# SQL Injection Attack, Listing the Database Contents on Oracle

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Same challenge as the non-Oracle version of this lab — no table or column
names are given — but this time on an **Oracle** database, which doesn't have
`information_schema` and requires Oracle-specific metadata views instead.

## Vulnerability Overview

Oracle does not expose the standard `information_schema` used by most other
engines. Instead, it provides its own metadata views — `all_tables` for table
names and `all_tab_columns` for column names — and (as in earlier Oracle labs)
every `SELECT` still requires a `FROM` clause, satisfied here with `DUAL` for
literal-only queries.

## Methodology

1. Determined the query returns **2 columns** via `ORDER BY` (failed at 3).
2. Tested `UNION SELECT 'a','a' FROM DUAL--`, which succeeded, confirming both
   column types and that the database was Oracle.
3. Queried the Oracle-specific table-listing view to find candidate table
   names containing user data:
   ```
   ' UNION SELECT table_name, NULL FROM all_tables--
   ```
4. Identified a table matching the expected pattern (e.g. `USERS_XXXXXX`).
5. Queried `all_tab_columns`, filtered to that table name, to list its
   columns:
   ```
   ' UNION SELECT column_name, NULL FROM all_tab_columns
   WHERE table_name='USERS_XXXXXX'--
   ```
6. Identified columns matching `USERNAME` and `PASSWORD` in the results.
7. Ran the final extraction query directly against the discovered table and
   columns:
   ```
   ' UNION SELECT username, password FROM users_xxxxxx--
   ```
8. Located the `administrator` row, retrieved the password, and logged in.

## Proof of Concept

**Table enumeration:**
```
' UNION SELECT table_name, NULL FROM all_tables--
```

**Column enumeration:**
```
' UNION SELECT column_name, NULL FROM all_tab_columns
WHERE table_name='USERS_XXXXXX'--
```

**Result:** Successfully reconstructed the full path from an unknown schema
to working administrator credentials, using only Oracle's built-in metadata
views.

## Impact

Identical impact to the non-Oracle version — full database structure
disclosure and credential extraction — but demonstrates that engine-specific
metadata differences (`all_tables`/`all_tab_columns` vs.
`information_schema`) don't meaningfully raise the bar for an attacker who
knows to check the cheat sheet for the right equivalent.

## Remediation

Parameterized queries prevent this attack entirely, regardless of which
metadata views the specific database engine happens to expose.

## Key Takeaway

Doing the non-Oracle and Oracle versions of this lab back-to-back made the
underlying pattern obvious: every major engine has *some* mechanism for
listing its own schema, so "the attacker doesn't know our table names" is
never a real security boundary on its own.
