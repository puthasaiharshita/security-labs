# Incident #61 – NSG security rule created, changed or deleted

**Verdict:** Benign Positive (security testing)

| Field | Value |
|---|---|
| Event time | 2026-11-08 ~05:29 UTC |
| Resource | NSG `nsg-misconfig-test`, rule `allow-rdp-any-TEST`, resource group `rg-soc-lab` |
| Evidence | AzureActivity `SECURITYRULES/DELETE`, status Succeeded, Caller = lab admin account |

**Evidence checked:** The incident held 2 alerts, both Action = Deleted. They were the same event, caught by two overlapping rule runs (every 15 min, 30 min lookback). Alert grouping merged them into 1 incident.

**Context:** Planned test. The rule (Any → 3389 TCP Allow) was created at 04:10 UTC on an NSG not attached to any NIC or subnet, then deleted to test the detection. The NSG was removed afterwards.

**Verdict:** Benign Positive – authorised test; detection worked end to end.

**Action:** Closed. Note: the Activity log does not include rule contents, so the analyst must review the rule itself.
