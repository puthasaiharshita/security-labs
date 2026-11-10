# Incident #19 – T1053.005 Scheduled task created

**Verdict:** Benign Positive (security testing)

| Field | Value |
|---|---|
| Alert time | 2026-11-02 14:10:53 UTC (19:40 IST) |
| Host | vm-win-lab |
| Evidence | Raw 4698 event: SubjectUserName = `azureuser`, TaskName = `\spawn` |

**What fired:** T1053.005 scheduled-task rule on vm-win-lab.

**Evidence checked:** The alert output had a blank SubjectUserName, so I pivoted to the raw 4698 event in the same time window (`queries/08-triage-pivot-4698.kql`). It showed `azureuser` creating `\spawn`.

**Context:** `\spawn` matches the Atomic Red Team T1053.005 test. It was created during my authorised lab test session on 2 Nov by the lab admin account.

**Verdict:** Benign Positive – real persistence technique, authorised test.

**Action:** Closed. Rule fixes: populate SubjectUserName in the alert output, add Host and Account entity mapping (incident showed "No entities"), add a rule description.
