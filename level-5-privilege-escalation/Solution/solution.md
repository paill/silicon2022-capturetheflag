# Level 5 Priv Esc

This challenge takes the form of a docker container - you start as low priv user goomba 
where you will find a cronjob for Larry and the first flag - This allows you to 
read a file in Larrys secret directory containing his password. From there you
can pivot to Larry and locate another secret in an environment variable

## Solution

- Looking in the /tmp/ folder you can find a cron.conf that defines the cronjob and first flag

- Although Larry and Root own the file in goombas home folder goomba can use the mv command to rename the original goomba-fix.py. Then goomba can make a new goomba-fix.py and change the permissions on /home/larry/secret/.password.txt

- once logged in as larry typing out the env command will show environment variables and the final secret. the .bashrc file can be read as well.