# PCAP Analysis Challenge Solution

The PCAP analysis challenge consists of one PCAP file with three questions:

1. What was the snmp community string that allowed access to the router?

2. What was the routers telnet password?

3. What were the contents of rex-plans.txt?

## Solution 1

For this solution you can use Wireshark to discover the snmp brute force attack and locate the correct snmp community string:

- Open badstuff.pcap in wireshark

- look for the SNMP protocol in the Protocol column

- right click -> follow -> UDP stream

- the correct string will be highlighted in blue at the bottom of the page

## Solution 2

For this question there are two ways to find the answer:

- Locate the second SNMP stream and right click -> follow -> UDP stream. This will show the full router configuration as it was downloaded

- Locate the Telnet TCP stream and right click -> follow -> TCP stream. This will show the telnet conversation with the password in plain text

## Solution 3

For this question we want to follow the Telnet stream. At the bottom we will see that a second telnet session was initiated from the router to the TC workstation and the contents of rex-plans.txt were revealed.