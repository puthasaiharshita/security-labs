# Blind SQL Injection with Conditional Responses

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools:** Burp Suite Community Edition (Proxy, Repeater, Intruder), Cookie/session
extensions (Cookie-Editor, FoxyProxy)
**Status:** ✅ Solved

---

## Objective

The injection point here is a `TrackingId` **cookie**, not a visible parameter,
and the application gives no visible difference in its response based on
whether the injected SQL query returns true or false — except one subtle tell:
a "Welcome back" message that only appears under certain conditions. The goal
is to use that single bit of signal to blindly extract the administrator's
password, character by character.

## Vulnerability Overview

This is a genuine **blind** SQL injection: the query results are never
returned directly to the page, and errors aren't displayed either. The only
observable difference between a true and a false injected condition is whether
the "Welcome back" message renders. This means every piece of data has to be
inferred indirectly, one true/false question at a time, by checking for the
presence or absence of that message.

## Methodology

1. Identified the `TrackingId` cookie as the injection point by testing a `'`
   character in its value and observing an internal server error, then
   restoring a valid true-condition payload and confirming the "Welcome back"
   message reappeared — proving the cookie value reaches a SQL query.
2. Since results aren't returned to the page (only a binary "Welcome back" /
   no message signal), ruled out UNION-based extraction and confirmed a
   true/false blind approach was required.
3. Verified the `users` table exists using a boolean subquery — if a query
   like `SELECT * FROM users LIMIT 1` inside the injected condition returns a
   row, the true-branch renders "Welcome back."
4. Confirmed the `administrator` user specifically exists using a targeted
   `WHERE username='administrator'` boolean check.
5. Determined the exact **length** of the administrator's password using a
   binary-search-style boolean check with `LENGTH(password) > N`, adjusting
   `N` up or down based on whether "Welcome back" appeared, until the exact
   length (20 characters) was found.
6. Sent the request to Burp Intruder and used **Cluster Bomb** attack type
   with two payload sets: one iterating the character *position* (1–20) and
   one iterating every possible *character* (uppercase, lowercase, digits) at
   that position, using `SUBSTRING(password, position, 1) = 'character'` as
   the boolean condition.
7. Filtered Intruder's results for responses containing "Welcome back," then
   sorted by position to reconstruct the password character by character.
8. Logged in as `administrator` using the reconstructed password.

## Proof of Concept

**Confirming administrator exists:**
```sql
' AND (SELECT username FROM users WHERE username='administrator')='administrator
```

**Finding password length:**
```sql
' AND (SELECT LENGTH(password) FROM users WHERE username='administrator')>N--
```

**Extracting each character (Intruder Cluster Bomb payload):**
```sql
' AND (SELECT SUBSTRING(password,POSITION,1) FROM users
WHERE username='administrator')='CHARACTER
```

**Result:** Filtering Intruder's grid for "Welcome back" responses across all
20 positions reconstructed the full password, which was then used to log in
successfully as `administrator`.

## Impact

Blind SQLi is often underestimated because there's no visible data leak on
the page — but as this lab shows, even a single reliable true/false signal
(here, a welcome message) is enough to exfiltrate arbitrarily sensitive data,
including full credentials, given enough automated requests.

## Remediation

Parameterized queries remain the fix. Additionally, avoid conditionally
rendering *any* UI element (messages, styling, redirect behavior) based on
raw query results tied to user-controlled input, since any observable
difference — however subtle — can become a blind-injection oracle.

## Key Takeaway

This lab reframed SQL injection for me as fundamentally a signal-extraction
problem once direct output is blocked: as long as there's *any* observable
difference between true and false, full data exfiltration is just a matter of
enough well-structured boolean queries and automation via Intruder.
