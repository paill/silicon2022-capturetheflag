# Level 5 Priv Esc

This challenge takes the form of a docker container - you start as low priv user goomba 
where you will find a cronjob for Larry and the first flag - This allows you to 
read a file in Larrys secret directory containing his password. From there you
can pivot to Larry and locate another secret in an environment variable

## Solutions
### Flag 1

- Looking in the /tmp/ folder you can find a cron.conf that defines the cronjob and first flag

```
#### SILICON{Cr0N-J0B-f7W}
PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/bin
SHELL=/bin/bash

* * * * *  /home/goomba/goomba-fix.py
```

### Flag 2

According to the cron.conf file, the file is set to run [every minute](https://crontab.guru/#*_*_*_*_*). We can confirm this by watching the processes that execute using `ps aux`.

We can do this manually or use the `watch` command or us a bash script like below
```bash
#!/bin/bash
while true
do
  date >> watch.log
  ps aux | grep goomba >> watch.log
  sleep 5
done
```

If you wait a couple minutes, CTRL-C and check the watch.log file, you'll that every 60 secs or so, the goomba script runs as larry. So if we can modify the goomba-fix.py script, we could escalate privileges to larry.

Checking file permissions in the `/home/goomba`, `goomba-fix.py` is owned by larry/root so we can't modify it directly.

However, goomba has write permissions to this directory - notice the drwxr-xr-x for the `.` entry. This means goomba can use the mv command to rename the original goomba-fix.py. Then goomba can make a new goomba-fix.py. Then we change the permissions on /home/larry/secret/.password.txt

Example goomba-fix.py:
```python
#!/usr/bin/python3
import subprocess

subprocess.run(["chmod", "666", "/home/larry/secret/.password.txt"])
```

To make sure that your script works, you need to do two steps

1. Set your script as executable using `chmod +x goomba-fix.py`
2. Add `#!/usr/share/python3` to the top of your script. You can find the path to python3 by running `which python3`. The #! is known as a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) and is how linux knows what to use when executing your script - by default it will try to use bash. So without this, your script likely won't work as the cron.conf file shows the script is being executed directly - /home/goomba/goomba-fix.py, instead of something like python3 /home/goomba/goomba-fix.py

This would run with the cron job and make it so that the file containing Larry's password is readable by the goomba user. Then you can switch users with su

```bash
su larry
```
### Flag 3

- once logged in as larry typing out the env command will show environment variables and the final secret. the .bashrc file can be read as well.