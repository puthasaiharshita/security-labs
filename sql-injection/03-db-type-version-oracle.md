# SQL Injection Attack, Querying the Database Type and Version on Oracle

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Use a UNION-based SQL injection to retrieve and display the database's version
string, on a database later identified as **Oracle**.

## Vulnerability Overview

Fingerprinting the database engine and version is usually the first real
information-gathering step after confirming column count — different engines
expose their version through different system tables/functions, and Oracle in
particular has a syntax quirk (a mandatory `FROM` clause) that has to be
worked around.

## Methodology

1. Determined the query returns 2 columns via `ORDER BY` (failed at 3).
2. Attempted the standard data-type probing query
   `UNION SELECT 'a','a'--` — this failed with an internal server error, which
   was the first clue the database wasn't MySQL or Microsoft SQL Server
   (neither of which requires a `FROM` clause for a literal `SELECT`).
3. Recalled that **Oracle requires every `SELECT` to include a `FROM` clause**,
   even when selecting a literal value with no real table involved. Oracle
   provides a built-in dummy table called `DUAL` specifically for this case.
4. Re-tested with `UNION SELECT 'a','a' FROM DUAL--`, which succeeded —
   confirming both the column types and that the database was Oracle.
5. Used the SQL injection cheat sheet's Oracle-specific version query,
   `SELECT banner FROM v$version`, in place of the literal test values.

## Proof of Concept

**Confirming Oracle via DUAL:**
```
' UNION SELECT 'a','a' FROM DUAL--
```

**Final working payload:**
```
' UNION SELECT banner, NULL FROM v$version--
```

**Result:** The page displayed the Oracle database version banner string,
confirming both the injection point and successful engine fingerprinting.

## Impact

Knowing the exact database engine and version lets an attacker tailor every
subsequent query to that engine's specific syntax (system tables, string
functions, concatenation operators), and can also reveal whether the database
is running a version with known, unpatched vulnerabilities.

## Remediation

Parameterized queries prevent this fingerprinting step entirely, since no
injected `UNION SELECT` — Oracle-syntax or otherwise — would ever reach the
database as executable SQL.

## Key Takeaway

The `FROM DUAL` requirement was the key signal here — a `UNION SELECT` with
literal values failing only on this database, while working elsewhere, is
itself a strong fingerprint for Oracle before ever running an explicit version
query.
