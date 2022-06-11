# Flag 1 
We aren't given much to start with besides just a note about malware running in this sandbox.

We can perform some enumeration to see what is happening on this box.

Running `ps`, we see a `/home/shyguy/run.sh` script running in the home directory of the user `shyguy`.

![ps](./images/ps.png)

The `run.sh` script contains some bash code that unsets an environment variable DEBUG, runs a binary `whereami`, and sleeps for 10 seconds.
```bash
#!/bin/bash
while true; do
    unset DEBUG
    /home/shyguy/whereami >> /var/log/whereami.log &
    /bin/sleep 10
done
```

Looking in /var/log/whereami.log, there are a bunch of `How did I end up here?!` messages.

We can try setting the DEBUG flag and running the whereami binary ourselves to see if the output changes at all.
```
ce1b101e9083:~$ export DEBUG=anything
ce1b101e9083:~$ /home/shyguy/whereami 
/tmp/hosts file not found. Defaulting to /etc/hosts
How did I end up here?!
```

We notice that a new line about a `/tmp/hosts` file is outputted. Then the binary hangs for a few seconds before outputting the other message.

[/etc/hosts](https://tldp.org/LDP/solrhe/Securing-Optimizing-Linux-RH-Edition-v1.3/chap9sec95.html) is a Linux file that can be used to map IP addresses to DNS entries. It seems like we can create our own that the binary would use. The delay in the binary running also seems like it is trying to reach something, but what?

Looking at the commands installed on the system, Mario & Luigu conveniently left us a packetsniffer tool in `/usr/local/bin/packetsniffer`

Running this command on our loopback interface (`packetsniffer -i lo`) shows us the traffic the `whereami` binary is generating and we can see it is trying to reach the domain `wannamammamia.bowsercorp.local`

```
Ether / IP / UDP / DNS Qry "b'wannamammamia.bowsercorp.local.'""
Ether / IP / UDP / DNS Ans
Ether / IP / ICMP / IPerror / UDPerror / DNS Ans
```

Now that we know the domain it is trying to reach, we can create our own hosts file in `/tmp/hosts` and point the domain at our localhost.

`echo '127.0.0.1 wannamammamia.bowsercorp.local' > /tmp/hosts`

We run the `whereami` binary again and we see that it runs a lot quicker but still the same output.
```
ce1b101e9083:~$ /home/shyguy/whereami 
How did I end up here?!
```

Let's analyze the traffic again, and we get some different output. We see the DNS query is succeeding, and then the binary is trying to reach 127.0.0.1:http
```
ce1b101e9083:~$ packetsniffer -i lo

            Ether / IP / UDP / DNS Qry "b'wannamammamia.bowsercorp.local.'"
            Ether / IP / UDP / DNS Ans "127.0.0.1"
        

            Ether / IP / TCP 127.0.0.1:57500 > 127.0.0.1:http S
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57500 RA
```

Let's start a python web server on port 80 to see if can get the request from the malware. Waiting for 30 seconds or so, we see we get a request!
```
ce1b101e9083:~$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
127.0.0.1 - - [11/Jun/2022 03:05:58] "GET / HTTP/1.1" 200 -
```

If we look at the `/var/log/whereami.log` file, we find our first flag!
```
How did I end up here?!
Sweet! Our malware is in the right place.
SILICON{Av0id7ng_$and8ox3s_F0r_The_Win}
Payload dropped in /tmp/wannamammamia.tar
How did I end up here?!
```

`SILICON{Av0id7ng_$and8ox3s_F0r_The_Win}`

# Flag 2
Continuing from the output we got in the log file, we check the /tmp directory and find a `wannamammamia.tar` file.
```
ce1b101e9083:~$ ls -la /tmp/
total 5716
drwxrwxrwt    1 root     root          4096 Jun 11 03:08 .
drwxr-xr-x    1 root     root          4096 Jun 11 02:50 ..
-rw-r--r--    1 toad     toad            41 Jun 11 03:03 hosts
-rwxrwxrwx    1 root     root       5836800 Jun  6 02:38 wannammamia.tar
```

Un-taring the file, we get a lot of output. This is actually a Docker image!
```
ce1b101e9083:/tmp$ tar xvf wannammamia.tar 
4c6d69de2c37f7ee050175d3be00efa46ca7196bbe7e0c0c09b31d8f10b2441f/
4c6d69de2c37f7ee050175d3be00efa46ca7196bbe7e0c0c09b31d8f10b2441f/VERSION
4c6d69de2c37f7ee050175d3be00efa46ca7196bbe7e0c0c09b31d8f10b2441f/json
4c6d69de2c37f7ee050175d3be00efa46ca7196bbe7e0c0c09b31d8f10b2441f/layer.tar
5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509/
5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509/VERSION
5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509/json
5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509/layer.tar
867a74c37ff1fac12222340c69a5bf24ca5cf15d447e61312011b9f2730f70ec.json
c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44/
c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44/VERSION
c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44/json
c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44/layer.tar
ec26cc0d3f68a58e262d2ae607ad72e2b460f739d374836e910cf6c820221f10/
ec26cc0d3f68a58e262d2ae607ad72e2b460f739d374836e910cf6c820221f10/VERSION
ec26cc0d3f68a58e262d2ae607ad72e2b460f739d374836e910cf6c820221f10/json
ec26cc0d3f68a58e262d2ae607ad72e2b460f739d374836e910cf6c820221f10/layer.tar
manifest.json
repositories
```

If we un-tar the layer.tar file in each layer, we can extract files that were added to the image. In layer `c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44`, we see an interesting file `/tmp/whats_this`

```
ce1b101e9083:/tmp/c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44$ tar xvf layer.tar 
tmp/
tmp/whats_this
```

Reading this file, we find our second flag.
```
ce1b101e9083:/tmp/c8fcaa785ff4ef3e90f176ade8d7675501e1493490e3d69502778a8df5306d44$ cat tmp/whats_this 
SILICON{D0ck3R_1m4G35_4r3_JU5t_T4r_f1L35??}
```

`SILICON{D0ck3R_1m4G35_4r3_JU5t_T4r_f1L35??}`

# Flag 3
Continuing from flag 2, extracting the files from layer `5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509`, we see a git config file `tmp/wannamammamia.git/config`

```
ce1b101e9083:/tmp/5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509$ tar xvf layer.tar 
tmp/
tmp/wannamammamia/
tmp/wannamammamia/.wh..wh..opq
tmp/wannamammamia/.git/
tmp/wannamammamia/.git/config
```

Reading this file, we discover a Git repo link `https://cfb049da77b8bcdf021ccb5cdafa6b26f09bcb1a@gogs.silicon-ctf.party/shyguy/wannamammamia.git`
```
ce1b101e9083:/tmp/5516b3099009f95ad6183f6dd71cc5dd8d6e8d0ea2f8a3420e173bffd73a3509$ cat tmp/wannamammamia/.git/config 
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = https://cfb049da77b8bcdf021ccb5cdafa6b26f09bcb1a@gogs.silicon-ctf.party/shyguy/wannamammamia.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
        remote = origin
        merge = refs/heads/master
```

Since the URL contains a PAT, we can try cloning the repo down locally. Git is not installed on the terminal so we have to do this on our own system.
`git clone https://cfb049da77b8bcdf021ccb5cdafa6b26f09bcb1a@gogs.silicon-ctf.party/shyguy/wannamammamia.git`

Based on the README, this appears the wannamammamia ransomware source code repo but it wasn't quite ready to be released. There is an encrypted file `test.txt.enc` and the `wannamammammamia.py` python script.

![readme](./images/readme.png)

Reviewing the Python script, we see a public key listed but no private key! 

```python
SERVER_PUBLIC_RSA_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvCJH+5uvyf/oJGRmC+5I
YiDnjnZjU3EAW/CrCGw7g5yp+HgVJ7kD2n42AnLsFaiswADreA9L9a3ulzvT9Q0T
qz6Habb4dzl1CLD84xtO1EVx4DJIG8jSoPiS0y1BvbEKWYv8PqcEzNyhmHCNqoiu
K73E660DAmd706GYRyGSzIo/srqGPcQ84MWtC5tmwQBZCyKDR3lYp1QEIPLhnzLG
mBd42UC1WKIebG+qi2NqmoxHubyBYVEQB/pRccVTs2TGM/RRqiLgdhz9HkvSeqpT
7HUdNulCc4bqB9d3dLqs8azciJY1c3olsDPDugDuzKkig0pHcCztzR1DkpPiGism
lQIDAQAB
-----END PUBLIC KEY-----''' # Attacker's embedded public RSA key used to encrypt AES key
SERVER_PRIVATE_RSA_KEY = '''''' # SHOULD NOT BE INCLUDED - only for decryptor purposes
```

If we check the git commit history `git log`, we see there is one previous commit.

```
commit f393b5b58fbc094f0661b9aed1eb2815b9dd3343 (HEAD -> master, origin/master, origin/HEAD)
Author: pail <pail@noreply.git>
Date:   Sun Jun 5 18:38:52 2022 -0700

    Oops

commit 294d5b711c45520993bde18b02a6c625794cb240
Author: pail <pail@noreply.git>
Date:   Sun Jun 5 18:37:19 2022 -0700

    Adding poc
```

Switching to the previous commit `git checkout HEAD~1`, we can find the private key that was removed!

```
SERVER_PRIVATE_RSA_KEY = '''-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,F9D9FA5259794C8A

uujlPrJGX0QFDDNEFCl6qEwGpQLBVts91rS9v6Pxe7EV25zIf9vg5WU58Mp8cB2B
oFFKFOMPOvMWY6FBkxgJxtUSxpCie4Y4HJhtiHGb9iHuNgo8xkScVqTM5EaxwzTz
j6fck+8oDyRCR6ek8IrScFFrSm3vzonMsggqWypszopFNwcixuW2u6fkQKAeHWPK
yC0GQ6PaCeRZ4tMrbUJfXXT8lBECdTvLHemXykVHUvlG97iow74uutotFm/wyx35
DUIudFHxEj7Xes2/vSQzcDJJX+syh6CBGMPiSHJ9KYzjbxmT+ZUxSIUNkU8oXIM+
RTv7UN8n0cuSBjiKvx5i5WeQDsmTHmlfJDoNYMMje3gYywAHJFYIyvEgtTDkXlEZ
IMyvoVPl1pKXtWk79pgtDkq2vo/GmRCU0wDDAA15nqVI9otxt4huW7agPSU1XjFo
4YrDg4WCH7DmscZChffVod/56Rcvcs83OUPst5VNm7A270VCdPH9JgNWENZJtxBS
M64Ltwz0IHi+qj2o+qReUt4NLGDq6vdnIFdCmDIpQwPaRn1mjMYMQMfkUYHY68to
LdfLubA50nNnxtf5BcIefxeCvcp9JZQDjShDATDMAlpU3RhxebJb3f30ZbS8gTon
UF5FvTxUfQ3s64ela+5iYuITSD21IaBGd91gijjtgkcHO7JoKUWTJlb72zaWPs4E
lA0VqmPj2tdd2d9sRskA9hbvHvxQQkIMerTK52BL5PL7v6Uu976YSLGTzB5xNu4M
R9/okr505Fk77ZoApQYg2HFhK9LCyOe5nesBXaDSRRWUXewDByFIUqYd2fZp8dXX
b5s/YBZZsBcISnzG/lmjsttbVHOi6X9GMnUYWkd30T5dIC+Zywa4zP5re+YDb+/j
yQqdBSP1cPKwyU1jYM4gtycvNhPk1IbbJLt46I25R2VnxNyf9Fhv5jOLKIu9IHN2
R2AsWyjeVj34lIOeYc0C9negPaU47DhbTtbSGJSH2M4O1CH8TuL6Ogse6PB69N4z
aoqsCTJ7rMcFOPgHYP3KJDNV3R48X1Uh0ELUvuShSWM2kxRpn+utVPMaqN+nCjXO
v15B4CmVxbzWNpqKl6L23PaNAXJvsgD1F6cCGRGUPTAfnqMZkAv6j9xdcvW8I0gH
Oha0xOdZ4bK2i/ESUp4qEcZYf4TTlWw7IHTxtRMUGCPDGzHhCI+8Ci/0oylTgyIt
qJvPmwnSyKxYqbS2GaZz2TkFY253Bb9PjzY8rW/A48GUJpJpqR6wL/jAJFejIBtf
KJluRhX1HtAnQrG8zb4M5jEq0J5P2JX5uO6bDsEevGCJqDDiGIO9/Wf6vOD3KQ22
InslNMCsp5JByLgock0wPopKitRcR5RB1Rsu4rFGJC6b9EW6nQ79b1tMSYPiY/7v
HPIKOU3ugd86kzvnJkg0N5GlvGGnQnQsHL3uz9Msqgheg7rKIB0QM3hqlWQjQmrt
ufleoWGuxvZhnyNJAFeruFyWRVr12UTe1Q/ZYZRKOtyRki8Oo3QTd/tfqVmtwxpO
kBRbCMW6DCPiAkOSxXsDsI75oppVayb5euowaiihnqv/NAldzW/iRQ==
-----END RSA PRIVATE KEY-----''' # SHOULD NOT BE INCLUDED - only for decryptor purposes
```

However before we can try to use this private key to decrypted `test.txt.enc`, we first need to decrypt the private key.

We don't know the password, so we'll need to try to crack it using [John th Ripper](https://www.openwall.com/john/). For a wordlist, there are a couple options. Use a common one like rockyou.txt or build your own based on the theme of the CTF (mario, luigi, goomba, etc).

First, we can extract the hash the private key using `pem2john private.key > keyhash`

Then, run `john -w wordlist.txt keyhash` and you should find the password to be `bowser`

Now, we can use `openssl` to decrypt the `test.txt.enc` file with the private key.
`openssl rsautl -decrypt -inkey private.key -in test.txt.enc -out test.txt`

Reading our decrypted file, we find the third flag.

`SILICON{B0w53r_m4k35_M3_W4nn4_cRy}`