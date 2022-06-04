# Level 4 - Foothold

## Description  
All the recon paid off! It looks like you found an S3 server of Bowser Corp's that's exposed to the internet. Log on to this server and see if it can be used to gain a foothold on their network!


## Premise  
Bowser Corp appears to have an open S3 server (discovered during recon). It looks it is publicly readable. There is a `.wpress` file, an `.s3` file, an encrypted `.pdf`, and a message from their web development company. The `.wpress` file is an archive of a new site being developed for a product Bowser Corp is planning to release. Likely what they stole from MBP!


Players use the  `.wpress` backup to get a copy of the sites data. The website's database contains credentials for a system account that will provide a foothold into Bowser Corp's network.  

![landing](https://user-images.githubusercontent.com/98978857/171498802-e550e829-7765-49d2-8777-a2dcc536599e.png)
Websites landing page when restored via the backup file.



## Files  
* [s3_bucket](./s3_bucket) contains the files for the challenge, and are intended to be uploaded to the CTF's FTP server.
* [bowsercorp](./bowsercorp) contains the WordPress child theme (and backdoor). These files are not to be uploaded, and are here just for reference. 


## Solutions  
[Solutions](./solutions)
