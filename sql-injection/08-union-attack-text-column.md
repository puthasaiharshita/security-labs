# SQL Injection UNION Attack, Finding a Column Containing Text

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

Building on the previous lab, once the column count is known (3, in this case),
determine **which** of those columns accepts string/text data — since that's
the column any extracted text data (like usernames or passwords) will need to
be placed into. Prove it by making a supplied random string appear on the page.

## Vulnerability Overview

Even after the column count matches, a `UNION SELECT` will still fail if a
column's data type is incompatible with the value placed in it (e.g. putting a
string into a column the database expects to be numeric or a date). Each
column's type has to be probed individually.

## Methodology

1. Started from the confirmed column count (3) from the previous lab.
2. Replaced one `NULL` at a time with a test string, keeping the others as
   `NULL`, to isolate which column tolerates string data without erroring:
   - `' UNION SELECT 'a',NULL,NULL--` → tested column 1
   - `' UNION SELECT NULL,'a',NULL--` → tested column 2
   - `' UNION SELECT NULL,NULL,'a'--` → tested column 3
3. Whichever attempt did **not** throw an error confirmed that column accepts
   string values — column 2 was the working position.
4. Replaced the test value `'a'` with the actual random string value the lab
   required to be displayed, confirming full control over that column's output.

## Proof of Concept

**Working payload:**
```
' UNION SELECT NULL,'MJUh7k',NULL--
```

**Result:** The supplied random string (`MJUh7k`) appeared directly on the
page in place of a normal product name, confirming column 2 is a string-typed
column and that its output is rendered directly to the page.

## Impact

Identifying the string-compatible column is what makes real data extraction
possible — once you know which column renders as visible text, you can place
any query result (usernames, passwords, table names, etc.) into that exact
position and read it straight from the page response.

## Remediation

Standard SQLi remediation applies: parameterized queries prevent the
`UNION SELECT` clause from being injected at all, regardless of column count
or data type probing.

## Key Takeaway

This lab reinforced a methodical, one-variable-at-a-time approach to blind
probing — changing one column at a time rather than guessing multiple
positions at once made it fast to isolate exactly which column to target for
data extraction in later labs.
