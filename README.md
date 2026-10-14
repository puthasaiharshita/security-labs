# Security Portfolio — Putha Sai Harshita
**Aspiring SOC Analyst** | Building hands-on blue-team labs (Active Directory, Windows Event Logging, detection fundamentals) | Red-team background from PortSwigger Web Security Academy (38 labs solved across SQL Injection and XSS)
🔗 [LinkedIn](https://www.linkedin.com/in/harshita-sai-putha-44144625b/)

## About

I'm working toward a SOC analyst role, and I believe understanding how attacks actually work makes for sharper detection — so this portfolio has two sides. My blue-team labs (Active Directory setup, Windows Event Logging, failed-logon detection) are where I'm building hands-on defensive and monitoring skills. My red-team background comes from the PortSwigger Web Security Academy, where I worked through 38 labs with Burp Suite, documenting methodology rather than just the "solved" checkbox — the same instinct for asking "how would I catch this happening?" carries directly into SOC work.

**Focus areas:** SOC Fundamentals, Detection & Monitoring, Active Directory Security
**Secondary:** Web Application Penetration Testing (VAPT), Cloud Security (AWS), Network Security (Juniper, Aviatrix)

## Skills

| Category | Tools / Areas |
|---|---|
| SOC / Detection | Windows Event Viewer, Active Directory, Event Log Analysis, Audit Policy Configuration |
| Web AppSec | Burp Suite (Proxy, Repeater, Intruder), SQLi, XSS |
| Cloud | AWS |
| Networking | Juniper Networks, Aviatrix, general networking fundamentals |
| Automation / Scripting | Python (file handling, regex, log parsing, REST APIs with requests), Git/GitHub, RPA |
| OS | Linux, Windows Server |

## Write-ups

### SOC / Detection Labs (4 completed)
- [Built My First Active Directory SOC Lab](soc-detection-labs/active-directory-soc-lab/README.md)
- [Splunk Dashboards](soc-portfolio/splunk-dashboards/README.md)
- [Python Auth Log Parser: Failed Login Detection with Regex](soc-portfolio/python-log-parser/README.md)
- [IOC Enrichment Tool: VirusTotal and AbuseIPDB Lookups](https://github.com/puthasaiharshita/ioc-enrichment-tool)

### Web Application Security (38 labs solved)
My PortSwigger Web Security Academy write-ups are in their own repo: **[web-security-labs](https://github.com/puthasaiharshita/web-security-labs)**

| Topic | Solved | Write-ups |
|---|---|---|
| SQL Injection | 15 | [sql-injection](https://github.com/puthasaiharshita/web-security-labs/tree/main/sql-injection) |
| Cross-Site Scripting (XSS) | 23 | [xss](https://github.com/puthasaiharshita/web-security-labs/tree/main/xss) |

Each write-up follows: **Objective → Vulnerability Overview → Methodology → PoC → Impact → Remediation → Key Takeaway** — mirroring the structure of a real pentest report finding, since that's ultimately the deliverable this skillset builds toward.

## Currently Learning / Next Steps

**Note on tooling constraints:** I'm unable to fully execute some Intruder-heavy and OAST-dependent labs in Burp Suite Community Edition — Community's Intruder throttles large payload sets, and out-of-band labs require Burp Collaborator, which is Pro-only. Three SQL injection labs (out-of-band interaction, out-of-band exfiltration, and filter bypass via XML encoding) are documented as methodology write-ups in `web-security-labs`, to be completed once I have Pro access.

## Structure

```
.
├── soc-detection-labs/
│   └── active-directory-soc-lab/
└── soc-portfolio/
    ├── splunk-dashboards/
    └── python-log-parser/
```

Other projects live in their own repos: [web-security-labs](https://github.com/puthasaiharshita/web-security-labs) and [ioc-enrichment-tool](https://github.com/puthasaiharshita/ioc-enrichment-tool).