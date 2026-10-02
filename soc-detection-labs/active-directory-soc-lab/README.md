## Built My First Active Directory SOC Lab

### What I built

I wanted to stop just reading about how enterprise networks handle logins and actually build one myself, so I set up a small AD lab from scratch on my laptop using VirtualBox. Two VMs: a Windows Server 2022 box acting as the Domain Controller (DC01), and a Windows 11 machine joined to it as a client (Client01). Both sit on their own isolated network so nothing touches my actual home network. Windows gave the client a default name, DESKTOP-0U2KVQR, which I refer to as Client01 in this write-up.

On the DC I installed Active Directory Domain Services, promoted it, and created a domain called `corp.local`. Then I built out three OUs (Sales, IT and HR) and in each one added a test user and a matching security group.

![OU structure](screenshots/New-OU-creation.png)
<p align="center"><em>Figure 1: The Sales, IT and HR OUs in corp.local</em></p>

![Sales user and group](screenshots/User_Group_creation-1.png)
<p align="center"><em>Figure 2: Test user and security group in the Sales OU</em></p>

![IT user and group](screenshots/User_Group_creation-2.png)
<p align="center"><em>Figure 3: Test user and security group in the IT OU</em></p>

![HR user and group](screenshots/User_Group_creation-3.png)
<p align="center"><em>Figure 4: Test user and security group in the HR OU</em></p>

![Group membership](screenshots/Add_member_to_group.png)
<p align="center"><em>Figure 5: Adding a user to their security group</em></p>

After that I joined the Windows 11 client to the domain and logged in as one of the domain users. Small thing, but it felt like a real milestone after all the setup. Then, to actually see the logging side of things, I deliberately typed the wrong password a few times on the client and went looking for the failed-logon event in Event Viewer, Event ID 4625.

![Domain join confirmed](screenshots/domain-joining-successfull.png)
<p align="center"><em>Figure 6: Client01 successfully joined to corp.local</em></p>

![Logged in as domain user](screenshots/Domain-joined-salesuser-into-client.png)
<p align="center"><em>Figure 7: Logged in to Client01 as a domain user</em></p>

### What AD actually does

Basically, AD is the one place that decides who's allowed to do what across the whole network. Instead of every machine keeping its own list of users and passwords, everything's defined once at the domain level, and every machine that joins trusts that central source. The Domain Controller holds all of it, and every login, no matter where it happens, gets checked against it.

### What I actually learned

Way more went wrong than I expected, honestly. Getting static IPs set correctly on both machines, making sure DNS pointed to the DC, keeping the internal network settings matched between the two VMs, even something as small as typing the username in the wrong format sometimes gave me errors. Any one of these being off broke things in ways that weren't obvious at first. I also picked the wrong Windows Server install mode early on (Server Core instead of Desktop Experience) and had to redo the whole install because of it.

The thing that genuinely surprised me: I assumed all the failed-login logging would show up on the Domain Controller since that's where authentication happens. It doesn't. The client logs its own local failed logins, and the DC logs a totally different set of events for whatever it's handling. I didn't expect logging to be spread out like that.

### What Event 4625 means

4625 just means "this login attempt failed." Wrong password, locked account, disabled account, all of it triggers this event. It shows up on whichever machine actually handled the logon attempt (for me, that was the client, not the DC), and the details include the account name, why it failed, and where the attempt came from.

![Event 4625 details](screenshots/4625_error.png)
<p align="center"><em>Figure 8: Event 4625 on Client01 after a wrong password</em></p>

### Why this actually matters for SOC work

One 4625 on its own usually means nothing - someone just fat-fingered their password. But a SOC analyst isn't watching one event at a time, they're watching for patterns: a bunch of 4625s in a short window, the same account failing over and over, or one account failing across a pile of different machines. That kind of pattern is usually the first sign something's wrong - brute force, someone testing stolen credentials, whatever. Building this made it click for me why knowing *where* these events actually land matters so much (and why related events on the DC matter too, like 4771 for Kerberos failures and 4776 for NTLM credential checks) - you can't spot an attack across a network if you don't know which machine is logging what.

### What's next

Now that I know where these events land, my next step is to forward the logs into Splunk and build a detection for repeated failed logons across this lab. I'll link that investigation here once it's done.
