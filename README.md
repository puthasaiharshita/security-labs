# Security Portfolio — Putha Sai Harshita
**Aspiring SOC Analyst** | Building hands-on blue-team labs (Active Directory, Windows Event Logging, detection fundamentals, Splunk and Microsoft Sentinel)
🔗 [LinkedIn](https://www.linkedin.com/in/harshita-sai-putha)

## About

I'm working toward a SOC analyst role. My labs are where I build hands-on defensive and monitoring skills: setting up an Active Directory environment, collecting Windows event logs, and writing detections in Splunk and Microsoft Sentinel for attacks I simulate myself. I document what broke as well as what worked, because that's where most of the learning happens.

**Focus areas:** SOC Fundamentals, Detection & Monitoring, Active Directory Security
**Also:** Azure monitoring (Arc, Sentinel), Python automation

## Skills

| Category | Tools / Areas |
|---|---|
| SOC / Detection | Splunk (SPL), Microsoft Sentinel (KQL), Windows Event Viewer, Active Directory, Event Log Analysis, Audit Policy Configuration, MITRE ATT&CK mapping, ATT&CK Navigator, Sysmon, Atomic Red Team, Detection Engineering |
| Cloud | Azure Arc, Azure Monitor Agent, Microsoft Sentinel, Data Collection Rules, Azure VMs, Network Security Groups
| Networking | Static IPs, DNS and isolated lab networks (VirtualBox) |
| Automation / Scripting | Python (file handling, regex, log parsing, REST APIs with requests), Git/GitHub |
| OS | Windows Server 2022 and 2025, Windows 11 |

## Write-ups

### SOC / Detection Labs (7 completed)
- [Built My First Active Directory SOC Lab](soc-detection-labs/active-directory-soc-lab/README.md)
- [Detecting Repeated Failed Logons with Splunk (T1110.001)](soc-portfolio/splunk-bruteforce-detection/README.md)
- [Python Auth Log Parser: Failed Login Detection with Regex](soc-portfolio/python-log-parser/README.md)
- [IOC Enrichment Tool: VirusTotal and AbuseIPDB Lookups](https://github.com/puthasaiharshita/ioc-enrichment-tool)
- [Hunting Encoded PowerShell with Microsoft Sentinel (KQL, T1059.001)](soc-portfolio/kql-encoded-powershell/README.md)
- [Getting Windows Logs into Microsoft Sentinel and Finding Failed Logons (KQL)](soc-portfolio/sentinel-windows-security-lab/README.md)
- [Simulating Attacker Techniques, Detecting Them in Microsoft Sentinel and Fixing the Gaps (KQL)](soc-portfolio/sentinel-attack-simulation/README.md)

## Currently Learning / Next Steps

- Converting my Sentinel rules to Sigma with automated validation in GitHub Actions (detection-as-code)
- Building more SOC detection write-ups (next: phishing analysis and incident response playbooks)

## Structure

```
.
├── soc-detection-labs/
│   └── active-directory-soc-lab/
└── soc-portfolio/
    ├── splunk-bruteforce-detection/
    ├── kql-encoded-powershell/
    ├── sentinel-windows-security-lab/
    ├── sentinel-attack-simulation/
    └── python-log-parser/
```

Other projects live in their own repo: [ioc-enrichment-tool](https://github.com/puthasaiharshita/ioc-enrichment-tool).
