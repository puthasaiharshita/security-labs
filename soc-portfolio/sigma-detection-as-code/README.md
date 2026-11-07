# Project 4: Detection-as-Code with Sigma (Sentinel + Splunk)

![Sigma detection CI](https://github.com/puthasaiharshita/security-labs/actions/workflows/sigma-ci.yml/badge.svg)

I rewrote my Project 3 Sentinel detections as vendor-neutral Sigma rules and converted them to KQL for Microsoft Sentinel and SPL for Splunk. I tested every KQL query against real attack logs from my lab. A GitHub Actions workflow validates and converts every rule on each push.

The rewrite exposed blind spots, duplicate alerts and false positives in my original rules. The numbers for each are in the test results section.

## Architecture

```
rules/*.yml (Sigma)
   |  sigma check (CI fails on any error or issue)
   v
pipelines/ --> map Sigma log sources to my Sentinel parsers
   |
   +--> converted/kql/  --> Sentinel (tested)
   |       uses parsers/SecurityEventParsed + parsers/SysmonParsed
   +--> converted/spl/  --> Splunk (converted, not tested)
```

In my workspace, Sysmon lands in the generic `Event` table. Some `SecurityEvent` fields are also empty, such as TaskName and SubjectUserSid for event 4698, and the data sits inside the `EventData` XML instead. The Sigma converter refused to build queries on columns that don't exist, which was correct. I wrote two KQL parser functions that extract the fields and pointed the pipelines at them.

## Rules and ATT&CK mapping

| # | Rule | ATT&CK | Data source | Level |
|---|---|---|---|---|
| 1 | Security log cleared | T1685.005 (formerly T1070.001), Defense Impairment | SecurityEvent 1102 | high |
| 2 | Local account created | T1136.001, Persistence | SecurityEvent 4720 | medium |
| 3 | Scheduled task created | T1053.005, Persistence / Execution | SecurityEvent 4698 | medium |
| 4 | Registry Run/RunOnce key set | T1547.001, Persistence | Sysmon 13 | medium |
| 5 | Local account discovery | T1087.001, Discovery | Sysmon 1 | low |
| 6 | Batch script via cmd.exe | T1059.003, Execution | Sysmon 1 | low |

`sigma check` flagged my original tags (`attack.defense-evasion`, `attack.t1070.001`) because ATT&CK v19 revoked them. The rules use the current IDs.

## Test results (14 days of lab data, 1 Windows VM)

| Rule | Before tuning | After tuning | What changed |
|---|---|---|---|
| 1 Log cleared | 2 | 2 | Matches my Day 3 fixed rule |
| 2 Account created | 2 | 2 | Same as Project 3 |
| 3 Scheduled task | 18 | 12 | Removed 6 false positives: Windows Defender Scheduled Scan created by SYSTEM (`S-1-5-18`) |
| 4 Run key | 9 | 3 | Removed 4 EventID 12 clean-up events and 2 Windows `ctfmon.exe /n` RunOnce writes by `userinit.exe` |
| 5 Account discovery | 44 | 24 | Removed 20 duplicate `net1.exe` events spawned by `net.exe` |
| 6 Batch script | 15 | 2 | Removed 13 Windows service scripts in System32 run by `svchost.exe` |

Each filter matches both the program or parent process and the specific value. An attacker who copies a benign name from a different account or process still triggers the rule.

## Problems I found in my Project 3 rules

- The account discovery rule missed 8 real commands. It searched the event text for "net user", but Windows logs commands launched from PowerShell as `"C:\Windows\system32\net.exe" user`. The Sigma rule matches the program and its arguments as separate fields and catches all 8. It also covers `net1.exe` and the PowerShell cmdlet `Get-LocalUser`.
- The Run key rule missed RunOnce. KQL `has` matches whole terms, so `has "CurrentVersion\\Run"` didn't match `RunOnce`. The Sigma rule uses `contains`.
- The batch script rule only matched the Atomic test's file name (`T1059.003_script.bat`). The Sigma rule fires on cmd.exe running any .bat or .cmd file and excludes only Windows service scripts.
- The scheduled task rule fired on days when I ran no test. Windows Defender was re-creating its scan task. I confirmed this from the creator SID before filtering it.

## Lessons

- Free-text search breaks on quoting and path formats, so I match on fields.
- I look at the data before tuning. My first idea for the batch script rule was to watch Temp and Downloads, and that would have missed my own test, which ran from `C:\AtomicRedTeam\`.
- A converted query can run without errors and still never match, if the field it uses is empty in the SIEM. I test every query against real events.
- I pin tool versions. On the day I installed it, `sigma-cli` 4.0.0 with pySigma 2.x broke the KQL backend, so `requirements.txt` pins the versions I tested. CI pins its runner (`ubuntu-24.04`) for the same reason.

## Run it yourself

```powershell
py -3.12 -m venv sigma-env
.\sigma-env\Scripts\Activate.ps1
pip install -r requirements.txt
sigma check rules\
sigma convert -t kusto -p pipelines\sentinel_securityevent.yml -p pipelines\sentinel_sysmon.yml -p azure_monitor rules\<rule>.yml
sigma convert -t splunk -p sysmon -p splunk_windows rules\<rule>.yml
```

Before using the KQL in Sentinel, save `parsers/SecurityEventParsed.kql` and `parsers/SysmonParsed.kql` as workspace functions with those exact names.

## Limitations

- The results come from lab data: 14 days, 1 VM and Atomic Red Team tests. A real environment will need more tuning.
- I converted the SPL queries but did not test them, because my Splunk lab does not hold these attack logs.
- No test events matched the PowerShell branch of rule 5, so that branch is untested.
- The rules depend on the two parser functions existing in the workspace.
- XML-encoded characters stay encoded in parsed fields. For example, `&` appears as `&amp;`.
- Rule 6 would miss a script placed in System32 and run by a service. Rule 3 covers the scheduled task setup that usually comes first.

## Next steps

- Write T1110.001 password guessing as a Sigma correlation rule (a count of 4625 events over 10 minutes).
- Deploy the KQL as Sentinel analytics rules from CI.

## Evidence

`screenshots/` holds the Sentinel test results for rules 1 to 6 (screenshots 01 to 06) and the passing CI run (07).
