# Security Portfolio — Putha Sai Harshita
**Aspiring SOC Analyst** | Building hands-on blue-team labs (Active Directory, Windows Event Logging, detection fundamentals) | Red-team background from PortSwigger Web Security Academy (48 labs solved across SQL Injection, XSS, and Authentication)
🔗 [LinkedIn](https://www.linkedin.com/in/harshita-sai-putha-44144625b/)

## About

I'm working toward a SOC analyst role, and I believe understanding how attacks actually work makes for sharper detection — so this portfolio has two sides. My blue-team labs (Active Directory setup, Windows Event Logging, failed-logon detection) are where I'm building hands-on defensive and monitoring skills. My red-team background comes from the PortSwigger Web Security Academy, where I worked through 48 real vulnerability classes with Burp Suite, documenting methodology rather than just the "solved" checkbox — the same instinct for asking "how would I catch this happening?" carries directly into SOC work.

**Focus areas:** SOC Fundamentals, Detection & Monitoring, Active Directory Security
**Secondary:** Web Application Penetration Testing (VAPT), Cloud Security (AWS), Network Security (Juniper, Aviatrix)

## Skills

| Category | Tools / Areas |
|---|---|
| SOC / Detection | Windows Event Viewer, Active Directory, Event Log Analysis, Audit Policy Configuration |
| Web AppSec | Burp Suite (Proxy, Repeater, Intruder), SQLi, XSS |
| Cloud | AWS |
| Networking | Juniper Networks, Aviatrix, general networking fundamentals |
| Automation | RPA |
| OS | Linux, Windows Server |

## Write-ups

### SOC / Detection Labs (1 completed)
- [Built My First Active Directory SOC Lab](soc-detection-labs/active-directory-soc-lab/README.md)

### SQL Injection (15 solved)
- [Retrieving Hidden Data via WHERE Clause Manipulation](sql-injection/01-retrieve-hidden-data.md)
- [Login Bypass via SQL Injection](sql-injection/03-login-bypass.md)
- [Querying Database Type and Version — Oracle](sql-injection/04-db-type-version-oracle.md)
- [Querying Database Type and Version — MySQL & Microsoft](sql-injection/05-db-type-version-mysql-mssql.md)
- [Listing Database Contents — Non-Oracle Databases](sql-injection/06-listing-contents-non-oracle.md)
- [Listing Database Contents — Oracle](sql-injection/07-listing-contents-oracle.md)
- [UNION Attack: Determining the Number of Columns](sql-injection/02-union-attack-columns.md)
- [UNION Attack: Finding a Column Containing Text](sql-injection/08-union-attack-text-column.md)
- [UNION Attack: Retrieving Data from Other Tables](sql-injection/09-union-attack-other-tables.md)
- [UNION Attack: Retrieving Multiple Values in a Single Column](sql-injection/10-union-attack-multiple-values.md)
- [Blind SQL Injection with Conditional Responses](sql-injection/11-blind-conditional-responses.md)
- [Blind SQL Injection with Conditional Errors](sql-injection/12-blind-conditional-errors.md)
- [Visible Error-Based SQL Injection](sql-injection/13-visible-error-based.md)
- [Blind SQL Injection with Time Delays](sql-injection/14-blind-time-delays.md)
- [Blind SQL Injection with Time Delays and Information Retrieval](sql-injection/15-blind-time-delays-info-retrieval.md)

#### Documented (Pending Burp Suite Pro)
- [Blind SQL Injection with Out-of-Band Interaction](sql-injection/16-blind-oob-interaction.md)
  — *requires Burp Collaborator (OAST), not available in Community Edition*
- [Blind SQL Injection with Out-of-Band Data Exfiltration](sql-injection/17-blind-oob-exfiltration.md)
  — *requires Burp Collaborator (OAST), not available in Community Edition*
- [SQL Injection with Filter Bypass via XML Encoding](sql-injection/18-filter-bypass-xml-encoding.md)
  — *requires extensive Intruder payload sweeps; Community Edition's rate limiting makes this impractical*

### Cross-Site Scripting (23 solved)
- [Reflected XSS into HTML Context With Nothing Encoded](xss/01-reflected-html-context.md)
- [Stored XSS into HTML Context With Nothing Encoded](xss/02-stored-html-context.md)
- [DOM XSS in document.write Sink Using Source location.search](xss/03-dom-document-write.md)
- [DOM XSS in innerHTML Sink Using Source location.search](xss/04-dom-innerhtml.md)
- [DOM XSS in jQuery Anchor href Attribute Sink Using location.search Source](xss/05-dom-jquery-href.md)
- [DOM XSS in jQuery Selector Sink Using a hashchange Event](xss/06-dom-jquery-hashchange.md)
- [Reflected XSS into Attribute With Angle Brackets HTML-Encoded](xss/07-reflected-attribute-html-encoded.md)
- [Stored XSS into Anchor href Attribute With Double Quotes HTML-Encoded](xss/08-stored-href-html-encoded.md)
- [Reflected XSS into a JavaScript String With Angle Brackets HTML Encoded](xss/09-reflected-js-string-html-encoded.md)
- [DOM XSS in document.write Sink Using Source location.search Inside a Select Element](xss/10-dom-document-write-select.md)
- [DOM XSS in AngularJS Expression With Angle Brackets and Double Quotes HTML-Encoded](xss/11-dom-angularjs-expression.md)
- [Reflected DOM XSS](xss/12-reflected-dom-xss.md)
- [Stored DOM XSS](xss/13-stored-dom-xss.md)
- [Reflected XSS into HTML Context With Most Tags and Attributes Blocked](xss/14-reflected-most-tags-blocked.md)
- [Reflected XSS into HTML Context With All Tags Blocked Except Custom Ones](xss/15-reflected-custom-tags-only.md)
- [Reflected XSS With Some SVG Markup Allowed](xss/16-reflected-svg-markup.md)
- [Reflected XSS in Canonical Link Tag](xss/17-reflected-canonical-link.md)
- [Reflected XSS into a JavaScript String With Single Quote and Backslash Escaped](xss/18-reflected-js-string-quote-backslash-escaped.md)
- [Reflected XSS into a JavaScript String With Angle Brackets and Double Quotes HTML-Encoded and Single Quotes Escaped](xss/19-reflected-js-string-mixed-encoding.md)
- [Stored XSS into onclick Event With Angle Brackets, Double Quotes HTML-Encoded, Single Quotes and Backslash Escaped](xss/20-stored-onclick-mixed-encoding.md)
- [Reflected XSS into a Template Literal With Angle Brackets, Quotes, Backslash and Backticks Unicode-Escaped](xss/21-reflected-template-literal-unicode-escaped.md)
- [Reflected XSS With Event Handlers and href Attributes Blocked](xss/22-reflected-event-handlers-href-blocked.md)
- [Reflected XSS Protected by CSP, With CSP Bypass](xss/23-reflected-csp-bypass.md)

#### Documented (Pending Burp Suite Pro / further research)
- [Exploiting XSS to Steal Cookies](xss/24-exploiting-xss-steal-cookies.md)
- [Exploiting XSS to Capture Passwords](xss/25-exploiting-xss-capture-passwords.md)
- [Exploiting XSS to Bypass CSRF Defenses](xss/26-exploiting-xss-bypass-csrf.md)
- [Reflected XSS With AngularJS Sandbox Escape Without Strings](xss/27-angularjs-sandbox-escape-no-strings.md) *(Expert)*
- [Reflected XSS With AngularJS Sandbox Escape and CSP](xss/28-angularjs-sandbox-escape-csp.md) *(Expert)*
- [Reflected XSS in a JavaScript URL With Some Characters Blocked](xss/29-reflected-js-url-chars-blocked.md) *(Expert)*
- [Reflected XSS Protected by Very Strict CSP, With Dangling Markup Attack](xss/30-strict-csp-dangling-markup.md)

### Authentication (5 solved)
- [Username Enumeration via Different Responses](authentication/01-username-enum-different-responses.md)
- [2FA Simple Bypass](authentication/02-2fa-simple-bypass.md)
- [Password Reset Broken Logic](authentication/03-password-reset-broken-logic.md)
- [Username Enumeration via Subtly Different Responses](authentication/04-username-enum-subtle-responses.md)
- [Offline Password Cracking](authentication/05-offline-password-cracking.md)

#### Documented (Pending Burp Suite Pro)
Methodology fully researched and documented; execution blocked in Community
Edition by Intruder payload/rate limitations on brute-force-heavy labs:

- [Username Enumeration via Response Timing](authentication/06-username-enum-response-timing.md)
- [Broken Brute-Force Protection, IP Block](authentication/07-broken-bruteforce-ip-block.md)
- [Username Enumeration via Account Lock](authentication/08-username-enum-account-lock.md)
- [2FA Broken Logic](authentication/09-2fa-broken-logic.md)
- [Brute-Forcing a Stay-Logged-In Cookie](authentication/10-bruteforce-stay-logged-in-cookie.md)
- [Password Reset Poisoning via Middleware](authentication/11-password-reset-poisoning-middleware.md)
- [Password Brute-Force via Password Change](authentication/12-password-bruteforce-via-change.md)
- [Broken Brute-Force Protection, Multiple Credentials per Request](authentication/13-broken-bruteforce-multi-credential.md) *(Expert)*
- [2FA Bypass Using a Brute-Force Attack](authentication/14-2fa-bypass-bruteforce.md) *(Expert)*

*(More labs added as I complete them.)*

## Currently Learning / Next Steps

**Note on tooling constraints:** I'm unable to fully execute the remaining
Intruder-heavy and OAST-dependent labs in Burp Suite Community Edition —
Community's Intruder throttles large payload sets, and out-of-band labs require
Burp Collaborator, which is Pro-only. I know how to solve these and have
prepared detailed methodology write-ups (see "Documented" sections above) for
completion once I have Pro access.

## Structure

.
├── soc-detection-labs/
│   └── active-directory-soc-lab/
├── sql-injection/
├── xss/
├── authentication/
├── assets/screenshots/
└── resources/
    └── TEMPLATE.md


Each write-up follows: **Objective → Vulnerability Overview → Methodology → PoC →
Impact → Remediation → Key Takeaway** — mirroring the structure of a real pentest
report finding, since that's ultimately the deliverable this skillset builds toward.
