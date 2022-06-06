# Level - 03 - Recon

## Flag 1

This flag is found using common recon techniques and tools. Commands such as ps, netstat, and python have been disabled for the player, so they must scan for open services running on the system. Once they discover that nmap is available, they can run this command to find a list of high ports listening.

```
nmap localhost -p1-65535
```

```
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-04 22:33 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00015s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 65497 closed tcp ports (conn-refused)
PORT      STATE SERVICE
65400/tcp open  unknown
65401/tcp open  unknown
65402/tcp open  unknown
65403/tcp open  unknown
65404/tcp open  unknown
65405/tcp open  unknown
65406/tcp open  unknown
65407/tcp open  unknown
65408/tcp open  unknown
65409/tcp open  unknown
65410/tcp open  unknown
65411/tcp open  unknown
65412/tcp open  unknown
65413/tcp open  unknown
65414/tcp open  unknown
65415/tcp open  unknown
65416/tcp open  unknown
65417/tcp open  unknown
65418/tcp open  unknown
65419/tcp open  unknown
65420/tcp open  unknown
65421/tcp open  unknown
65422/tcp open  unknown
65423/tcp open  unknown
65424/tcp open  unknown
65425/tcp open  unknown
65426/tcp open  unknown
65427/tcp open  unknown
65428/tcp open  unknown
65429/tcp open  unknown
65430/tcp open  unknown
65431/tcp open  unknown
65432/tcp open  unknown
65433/tcp open  unknown
65434/tcp open  unknown
65435/tcp open  unknown
65436/tcp open  unknown
65437/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 3.38 seconds
```

It won't be apparent what's behind these services, so the player might just want to connect to one of them and see if something responds.

```
nc localhost 65400
```

```
mwah HA ha HA ha ha HA HA
```

If the player runs through each of the running services they should notice that they all respond with some sort of evil Bowser laugh. The key to solving this level is identifying the pattern, which is a series of lowercase and uppercase words, and always 8 of them.

```
mwah = 0
ha = 0
HA = 1
```

Using this as a guide, they can convert these to binary.

```
01010011
01001001
01001100
01001001
01000011
01001111
01001110
01111011
01011001
01101111
01110101
00110001
01001100
01001110
01000101
01010110
01000101
01010010
01010011
01100101
01000101
01110100
01101000
01000101
01010000
01010010
01001001
01001110
01000011
01100101
01010011
01010011
01100001
01000111
01100001
01101001
01101110
01111101
```

Now the last part in solving the level is to convert these from binary to their ascii representation, which is the flag.

```
SILICON{You1LNEVERSeEthEPRINCeSSaGain}
```
