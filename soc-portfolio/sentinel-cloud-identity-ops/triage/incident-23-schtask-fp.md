# Incident #23 – T1053.005 Scheduled task created

**Verdict:** False Positive (not malicious)

| Field | Value |
|---|---|
| Alert time | 2026-11-03 06:43:33 UTC (12:13 IST) |
| Host | vm-win-lab |
| Evidence | Raw 4698 event: SubjectUserName = `vm-win-lab$` (machine account), Microsoft built-in task under `\Microsoft\Windows\` |

**Evidence checked:** Alert had a blank SubjectUserName, so I pivoted to the raw 4698 event. An account ending in `$` is the computer account, meaning the OS created the task, not a person.

**Context:** Built-in Microsoft task; no test or user activity on 3 Nov.

**Verdict:** False Positive – rule logic too broad (fires on Microsoft built-in tasks).

**Action:** Closed. Tuning: exclude events where SubjectUserName ends in `$` AND TaskName starts with `\Microsoft\Windows\`. Incident #24 is a duplicate of the same event.
