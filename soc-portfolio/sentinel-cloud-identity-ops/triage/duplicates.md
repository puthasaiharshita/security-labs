# Duplicate incidents

The T1053.005 rule ran every 5 minutes with a 10-minute lookback, so one event was often caught by two runs and created two incidents. Each duplicate was closed with the same classification as its original and a one-line reference.

| Duplicate | Original | Event | Classification |
|---|---|---|---|
| #20 | #19 | 2026-11-02 14:10:53 UTC, `azureuser`, `\spawn` | Benign Positive – security testing |
| #24 | #23 | 2026-11-03 06:43:33 UTC, `vm-win-lab$`, Microsoft task | False Positive – not malicious |
| #54 | #49 | 2026-11-06 06:46:41 UTC, `vm-win-lab$`, Defender task | False Positive – not malicious |

Fix: alert grouping (all entities match, 1 hour) now merges repeat alerts into one incident, which already worked for the NSG rule (#61: 2 alerts → 1 incident).
