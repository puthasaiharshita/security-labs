import re
from collections import Counter

LOG_FILE = "auth.log"

ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
failed_pattern = re.compile(r'Failed password for (?:invalid user )?(\S+) from (\S+)')
accepted_pattern = re.compile(r'Accepted \w+ for (\S+) from (\S+)')

all_ips = Counter()
failed_users = Counter()
failed_ips = Counter()
successful_users = Counter()

with open(LOG_FILE) as f:
    for line in f:
        ip_match = ip_pattern.search(line)
        if ip_match:
            all_ips[ip_match.group()] += 1

        failed = failed_pattern.search(line)
        if failed:
            user, ip = failed.groups()
            failed_users[user] += 1
            failed_ips[ip] += 1

        accepted = accepted_pattern.search(line)
        if accepted:
            successful_users[accepted.group(1)] += 1
print("=== AUTH LOG SUMMARY ===")
print(f"Total failed logins:     {sum(failed_users.values())}")
print(f"Total successful logins: {sum(successful_users.values())}")
print(f"Unique IPs seen:         {len(all_ips)}")

print("\nTop attacking IPs (failed logins):")
for ip, n in failed_ips.most_common(5):
    print(f"  {ip:<18} {n}")

print("\nMost targeted usernames:")
for user, n in failed_users.most_common(5):
    print(f"  {user:<18} {n}")
