# Blind SQL Injection with Time Delays and Information Retrieval

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater, Intruder)
**Status:** ✅ Solved

---

## Objective

Building directly on the previous time-delay lab, this one requires going
further than just proving the injection exists — the goal is to fully
extract the `administrator` user's password using **only** response-time
differences as the signal, since there's still no content or error-based
oracle available.

## Vulnerability Overview

This combines conditional logic (`CASE WHEN`) with a time-delay function
instead of a content difference or a forced error: if the injected condition
is true, the query sleeps for N seconds; if false, it returns immediately.
Measuring response time at each step reveals the answer to each boolean
question, letting an attacker binary-search their way through unknown values
exactly as in the content-based blind labs, just using a stopwatch instead of
a keyword.

## Methodology

1. Confirmed basic time-based injectability first (same as the previous lab)
   using an unconditional `pg_sleep(10)` payload.
2. Confirmed the `users` table and `administrator` username exist using a
   **conditional** delay: `CASE WHEN (username='administrator') THEN
   pg_sleep(10) ELSE pg_sleep(0) END` — a delayed response confirmed the
   condition was true.
3. Determined the password **length** using the same conditional pattern with
   `LENGTH(password)>N`, sending each candidate length to Burp Intruder and
   checking the response-time column for each request — the correct length
   was 20 characters.
4. Set up a Cluster Bomb Intruder attack: one payload set for character
   *position* (1–20, sequential), and one payload set for the *character*
   value (brute-force, all letters/digits), each wrapped in a
   `CASE WHEN (SUBSTRING(password,POSITION,1)='CHAR') THEN pg_sleep(5) ELSE
   pg_sleep(0) END` payload — using 5 rather than 10 seconds per request to
   keep the overall attack duration manageable across many combinations.
5. Since Intruder shows a response-time column per request, sorted results by
   response time and identified, for each position, which single character
   produced the ~5-second delay (all others responded near-instantly).
6. Reconstructed the password character by character from the delayed
   responses and logged in as `administrator`.

## Proof of Concept

**Confirming administrator exists (time-based conditional):**
```sql
' || (SELECT CASE WHEN (username='administrator') THEN pg_sleep(10) ELSE
pg_sleep(0) END FROM users) || '
```

**Extracting password length:**
```sql
' || (SELECT CASE WHEN (LENGTH(password)>N) THEN pg_sleep(5) ELSE pg_sleep(0)
END FROM users WHERE username='administrator') || '
```

**Extracting each character:**
```sql
' || (SELECT CASE WHEN (SUBSTRING(password,POSITION,1)='CHAR') THEN pg_sleep(5)
ELSE pg_sleep(0) END FROM users WHERE username='administrator') || '
```

**Result:** Sorting Intruder's response-time column identified the correct
character at each of the 20 positions, fully reconstructing the password,
which was then used to log in successfully.

## Impact

This lab shows time-based blind SQLi isn't just a proof-of-concept
technique — it's a fully practical, if slower, method for complete data
exfiltration, including credentials, using nothing but response timing as the
oracle. Given enough automated requests, "no visible leak at all" provides no
real protection.

## Remediation

Parameterized queries remain the primary fix. As defense in depth, rate
limiting and anomaly detection on requests with unusually long response times
can help detect this attack pattern in progress, though it should never be
relied on as a substitute for fixing the injection itself.

## Key Takeaway

This lab reinforced that the *same* extraction methodology (binary search on
length, then per-character brute force via Cluster Bomb) applies almost
identically across content-based, error-based, and time-based blind SQLi —
only the "oracle" changes, not the overall attack structure.
