# SQL Injection with Filter Bypass via XML Encoding

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools required:** Burp Suite Professional recommended (Intruder's larger
payload/encoding options make iterating bypass attempts far more practical)
**Status:** 📝 Studied via walkthrough — not yet personally executed

*Note: I have not solved this lab myself. These are notes I took while
studying a walkthrough for later revision. I'm documenting the methodology
here to show I understand the technique, not to claim completion.*

---

## Objective

The application has an input filter (a WAF or custom validation layer)
blocking common SQL injection keywords like `SELECT` and `UNION` when
submitted directly. The request itself is structured as XML data. The goal is
to bypass the keyword filter using XML-specific encoding tricks so the
injected SQL still reaches the database intact.

## Vulnerability Overview

Many naive input filters check the raw request body for blocked keywords
*before* any decoding happens. Since the request body here is XML, and XML
supports encoding characters as numeric character references (e.g. `&#83;`
for the letter `S`), an attacker can encode the blocked keywords so the
filter's plain-text pattern match never triggers — but the XML parser on the
server still decodes the entities back into the real keywords before passing
them to the SQL layer.

## Methodology (as studied)

1. Identify that the request body is XML-formatted and that a direct `'
   UNION SELECT NULL--`-style payload gets blocked by the filter (likely
   pattern-matching on `UNION` or `SELECT`).
2. Convert the blocked keywords into their XML numeric character reference
   equivalents, character by character (e.g. `U` → `&#85;`, `N` → `&#78;`,
   etc.), so that "UNION SELECT" is spelled out entirely in encoded entities
   rather than plain text.
3. Submit the XML-encoded payload as the request body via Burp Repeater.
4. The application's XML parser decodes the entities back into literal text
   *before* the value is used in the SQL query — meaning the filter (which
   only inspected the raw, still-encoded body) never sees the blocked
   keywords, but the database still receives valid, executable SQL.
5. From there, the attack proceeds exactly like a standard UNION-based
   extraction: determine column count, find the string-compatible column,
   then extract username/password data from the `users` table.
6. Log in as `administrator` using the extracted credentials.

## Proof of Concept (conceptual)

**Blocked (plain-text) payload:**
```
' UNION SELECT username, password FROM users--
```

**XML-entity-encoded equivalent (illustrative, partial):**
```
&#39;&#32;&#85;&#78;&#73;&#79;&#78;&#32;&#83;&#69;&#76;&#69;&#67;&#84;...
```
*(Each character of the blocked keywords replaced with its numeric XML
entity; the filter's plain-text match fails, but the XML parser resolves it
to the real SQL before execution.)*

## Why I Haven't Executed This Yet

This specific bypass benefits significantly from Burp Suite Pro's more
flexible Intruder payload processing (e.g. built-in "XML encode" payload
processing rules) to generate the full encoded payload reliably; doing it
entirely by hand is possible but error-prone and slow, which is why I've
prioritized understanding the mechanism over rushing a manual attempt in
Community Edition.

## Planned Remediation (if I were the developer)

Input validation and filtering should always happen **after** any decoding
step (XML parsing, URL decoding, etc.), not before — filters need to inspect
the fully resolved value the application will actually use, not the raw
wire-format representation of it. Ultimately, though, filter-based defenses
are inherently bypassable; parameterized queries remain the only reliable
fix regardless of encoding tricks.

## Key Takeaway

This was a good reminder that keyword-blocklist filters are a losing game —
any encoding layer the application decodes *after* the filter runs (XML
entities, URL encoding, Unicode normalization, etc.) is a potential bypass
vector, which is exactly why allowlisting and parameterization are considered
the only real defenses against injection, not pattern matching.
