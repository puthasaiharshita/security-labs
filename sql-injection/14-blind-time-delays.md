# Blind SQL Injection with Time Delays

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater)
**Status:** ✅ Solved

---

## Objective

In this variant, the application gives absolutely no observable difference in
its response content whether the injected query's condition is true or
false, and it also doesn't produce a distinguishable error — the query is
executed **synchronously**, so the only usable signal is how long the
response takes to come back. The goal is simply to prove the injection point
is exploitable by causing a deliberate 10-second delay.

## Vulnerability Overview

When neither content differences nor errors are observable, but the
vulnerable query executes synchronously (the app waits for the query before
responding), an attacker can use database-specific sleep/delay functions to
turn response time itself into a binary signal — a condition that's "true"
takes N seconds longer to respond than one that's "false."

## Methodology

1. Confirmed the `TrackingId` cookie as the injection point via a basic `'`
   test, but found no visible content difference or error message regardless
   of the payload — ruling out both content-based and error-based blind
   techniques from the earlier labs.
2. Referenced the SQL injection cheat sheet's time-delay syntax, which
   differs significantly by engine:
   - Oracle: `dbms_pipe.receive_message(('a'),10)`
   - Microsoft: `WAITFOR DELAY '0:0:10'`
   - PostgreSQL: `SELECT pg_sleep(10)`
   - MySQL: `SELECT SLEEP(10)`
3. Sent the request to Burp Repeater and tried the PostgreSQL syntax first
   (based on earlier engine identification from prior labs in the same
   series), appending it directly to the tracking cookie value.
4. Observed the response time in Repeater — a plain, non-delayed request
   returned almost instantly, while the payload-injected request took
   noticeably (~10 seconds) longer to respond, confirming successful
   time-based blind injection.

## Proof of Concept

**Payload used in the `TrackingId` cookie:**
```sql
' || (SELECT pg_sleep(10))--
```

**Result:** The response was delayed by approximately 10 seconds compared to
a baseline request with no payload, confirming the parameter is vulnerable to
time-based blind SQL injection.

## Impact

Time-based blind SQLi is significant because it works even when an
application leaks absolutely nothing else — no content difference, no
errors — making it the technique of last resort but also one of the hardest
to defend against through output sanitization alone, since the "leak" is
purely timing, not content.

## Remediation

Parameterized queries prevent this entirely, since the injected `pg_sleep()`
call (or engine equivalent) would never be treated as executable SQL. As
additional hardening, enforcing strict statement timeouts at the database
level limits how much delay an attacker can meaningfully induce per request,
though this doesn't fix the underlying vulnerability.

## Key Takeaway

This lab was a good reminder to always check for a time-based signal as a
fallback once content-based and error-based blind techniques come up empty —
"no observable difference at all" doesn't mean "not exploitable," it just
means the vulnerability requires a different oracle.
