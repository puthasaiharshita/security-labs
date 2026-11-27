# Security Portfolio: Putha Sai Harshita
Information Security Analyst | Hands-on blue-team labs in Active Directory, Windows event logging, Sigma, Splunk and Microsoft Sentinel
[LinkedIn](https://www.linkedin.com/in/harshita-sai-putha)

## About

I'm looking for an entry-level Information Security Analyst role. I build these skills in a home lab: I set up an Active Directory domain, collect Windows event logs, simulate attacks against my own machines, write detections for them in Splunk and Microsoft Sentinel, and triage the incidents those detections raise. Along the way I've also worked with Azure monitoring (Arc, Azure Monitor Agent, Sentinel) and written small Python tools. Each write-up covers what broke as well as what worked, and what the results can't prove. I build these skills in a home lab: I set up an Active Directory domain, collect Windows event logs, simulate attacks against my own machines, write detections for them in Splunk and Microsoft Sentinel, and triage the incidents those detections raise. Along the way I've also worked with Azure monitoring (Arc, Azure Monitor Agent, Sentinel) and written small Python tools. Each write-up covers what broke as well as what worked, and what the results can't prove.

## Skills

| Category | Tools / Areas |
|---|---|
| SOC / Detection | Splunk (SPL), Microsoft Sentinel (KQL), Sigma, Windows Event Viewer, Active Directory, Event Log Analysis, Audit Policy Configuration, MITRE ATT&CK mapping, ATT&CK Navigator, Sysmon, Atomic Red Team, Detection Engineering, Alert Triage and Rule Tuning |
| Cloud | Azure Arc, Azure Monitor Agent, Microsoft Sentinel, Data Collection Rules, Azure Activity, Entra ID audit logs, Azure VMs, Network Security Groups |
| Networking | Static IPs, DNS and isolated lab networks (VirtualBox) |
| Automation / Scripting | Python (file handling, regex, log parsing, REST APIs with requests), Git/GitHub, GitHub Actions |
| OS | Windows Server 2022 and 2025, Windows 11 |

## Write-ups

### Featured
- [Simulating Attacker Techniques, Detecting Them in Microsoft Sentinel and Fixing the Gaps (KQL)](soc-portfolio/sentinel-attack-simulation/README.md)
- [Detection-as-Code with Sigma (Sentinel + Splunk)](soc-portfolio/sigma-detection-as-code/README.md)
- [Triaging Sentinel Incidents and Tuning a Noisy Rule (Azure Activity and Entra ID)](soc-portfolio/sentinel-cloud-identity-ops/README.md)
- [Detecting Repeated Failed Logons with Splunk (T1110.001)](soc-portfolio/splunk-bruteforce-detection/README.md)

### Earlier labs
- [Built My First Active Directory SOC Lab](soc-detection-labs/active-directory-soc-lab/README.md)
- [Hunting Encoded PowerShell with Microsoft Sentinel (KQL, T1059.001)](soc-portfolio/kql-encoded-powershell/README.md)
- [Getting Windows Logs into Microsoft Sentinel and Finding Failed Logons (KQL)](soc-portfolio/sentinel-windows-security-lab/README.md)

### Python tools
### Python tools
- [IOC Enrichment Tool: VirusTotal and AbuseIPDB Lookups](https://github.com/puthasaiharshita/ioc-enrichment-tool) (separate repo)
- [Auth Log Parser: Finding Brute-Force Sources in Linux SSH Logs](soc-portfolio/python-log-parser/README.md)

## What I'm working on next

## What I'm working on next

- Phishing triage: parsing reported emails, enriching indicators and comparing rule-based and AI verdicts against my own labels
- Vulnerability management: scanning my lab, prioritising findings with CVSS, EPSS and CISA KEV, and tracking fixes
- Incident response: a full investigation with a timeline, incident report and new detections
- Small-company security review: access review, cloud posture and ISO 27001 / NIST CSF evidence

## Structure

```
.
├── .github/workflows/        (Sigma CI)
├── soc-detection-labs/
│   └── active-directory-soc-lab/
└── soc-portfolio/
    ├── sentinel-attack-simulation/
    ├── sigma-detection-as-code/
    ├── sentinel-cloud-identity-ops/
    ├── splunk-bruteforce-detection/
    ├── kql-encoded-powershell/
    ├── sentinel-windows-security-lab/
    └── python-log-parser/
```
