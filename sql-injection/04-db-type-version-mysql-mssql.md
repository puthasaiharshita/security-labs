# SQL Injection Attack, Querying the Database Type and Version on MySQL and Microsoft

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Use a UNION-based SQL injection to retrieve and display the database version
string on a database identified as either MySQL or Microsoft SQL Server (both
share very similar injection syntax, unlike Oracle).

## Vulnerability Overview

Unlike Oracle, MySQL and Microsoft SQL Server both allow `SELECT` statements
with literal values and no `FROM` clause, so the standard UNION probing
technique works without modification. The one syntax quirk in this lab: `--`
as a comment terminator needs a trailing space to be parsed correctly by these
engines, so `#` is sometimes used instead as a safer end-of-line comment
marker.

## Methodology

1. Determined column count via `ORDER BY`, which failed at 3 — confirming 2
   columns.
2. Noted that using `--` alone at the end of the payload sometimes returned an
   internal server error, so switched to using `#` as the comment terminator
   instead, which is reliably supported by MySQL.
3. Tested `UNION SELECT 'a','a'#` (no `FROM` clause needed) — this succeeded
   immediately, confirming the column data types and ruling out Oracle.
4. Used the SQL injection cheat sheet's MySQL/Microsoft version query,
   `SELECT @@version`, in place of the test literal.

## Proof of Concept

**Working payload:**
```
' UNION SELECT @@version, NULL#
```

**Result:** The page displayed the database version string
(`8.0.29` in this case), confirming both successful column-type matching and
engine fingerprinting via the `@@version` system variable, which both MySQL
and Microsoft SQL Server support.

## Impact

Same as with any successful version fingerprint — it lets an attacker target
subsequent queries precisely to the confirmed engine's syntax and evaluate
whether the specific version has any known exploitable vulnerabilities.

## Remediation

Parameterized queries prevent the injected `UNION SELECT` (and the `@@version`
lookup) from ever executing, regardless of which comment syntax or version
function the attacker tries.

## Key Takeaway

The `#` vs `--` comment syntax difference was a small but important detail —
assuming `--` always works across every database engine can cause a
false negative during testing when the actual issue is just comment-syntax
compatibility, not a lack of vulnerability.
