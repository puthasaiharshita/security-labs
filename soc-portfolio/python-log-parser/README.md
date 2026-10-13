# Python Log Parser

This is my first real Python project. I'm learning to become a SOC analyst, and I wanted to understand what a log file actually looks like before I touch tools like Splunk or Sentinel. So I wrote a small script that reads an SSH `auth.log` file and tells me what's going on in it.

## What it does

It reads the log line by line and pulls out:

- how many failed and successful logins there were
- which IP addresses failed the most (the likely attackers)
- which usernames were targeted the most

The sample log is made up. The IPs come from ranges reserved for documentation, so nothing in here is real.

## How to run it

Make sure Python 3 is installed, put `auth.log` in the same folder, then run:

```
python log_parser.py
```

You should see a summary like this:

```
=== AUTH LOG SUMMARY ===
Total failed logins:     5
Total successful logins: 2
Unique IPs seen:         5

Top attacking IPs (failed logins):
  203.0.113.5        3
  192.168.1.10       1
  198.51.100.7       1

Most targeted usernames:
  root               3
  admin              1
  test               1
```

## What I learned

- Reading files in Python and looping through them
- Using regex to pull IPs and usernames out of messy text. I found out that the "invalid user" lines break a simple pattern, so I had to handle them separately
- Counting things quickly with `collections.Counter`

## What's next

I want to let the script accept any log file as an argument, and later flag IPs with a lot of failed logins automatically.
