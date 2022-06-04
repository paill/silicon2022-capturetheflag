# Solutions
## Silicon 2022 CTF
### Level 4 - Foothold. 
These are a work in progress, screenshots will be added over the next 24 hours as I resolve this from start to finish. 

### Flag 1 - Plain Sight
Very easy. The flag is located in the `.s3` of the S3 bucket server.. The only challenge is downloading files from an S3 bucket.

### Flags 2-4, maybe 5 and definitly 6. 
By Googling the file extension and/or reading `README.txt` in S3 bucket, users will realize that the
.wpress file is a backup file created with 
[All-in-One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/).

Players have two options, 
1. Quick hacker way. Use a command line tool such as [Wpress-Extractor](https://github.com/fifthsegment/Wpress-Extractor) to extract the archive. 

<img width="1143" alt="Screen Shot 2022-06-01 at 2 06 26 PM" src="https://user-images.githubusercontent.com/98978857/171501920-85f6a93c-99e0-458c-9d4f-52755e149e49.png">


2. Long GUI way. Spinning up a local instance of WordPress, then restoring the archive via the [All-in-One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/) plugin. Players will discover it's over the size limit for the free version. This is a fun challenge to solve. They can try and hack the open source plugin, or google [alternative solutions](https://github.com/d0n601/All-In-One-WP-Migration-With-Import) :).  

<img width="1200" alt="Screen Shot 2022-06-01 at 2 24 25 PM" src="https://user-images.githubusercontent.com/98978857/171504887-b49dc359-c44f-4680-afa6-21c07d64cdc2.png">
Fail.  

Using an open source plugin they can restore the site. Accessing the admin console will still be a challenge though. 

<img width="1200" alt="Screen Shot 2022-06-01 at 2 34 19 PM" src="https://user-images.githubusercontent.com/98978857/171505783-d2a31217-62f4-4c87-aabf-77b9961574e7.png">

To get access to the admin console they either need to crack the `gumba3` user's password, or insert a new administrator into the dabase via [
this method](https://stackoverflow.com/questions/50865311/wordpress-cannot-login-after-migrating-with-all-in-one-wp-migration) <-- as we know they control their own local database.

#### Cracking Gumba3 User Creds. 
After extracting the data from the `.wpress` file, 
* Find user hashes `cat database.sql | grep _users`.
* <img width="868" alt="Screen Shot 2022-06-01 at 2 57 36 PM" src="https://user-images.githubusercontent.com/98978857/171508762-d68e9458-8327-4350-8339-065c88b85a6c.png">

* Copy the hashes into their own file, one hash per line, pay attention to gumba3's -> `$P$BmcHRRkoaQcWmOpUDhjgiXN8X3p8Pt0`.
* Crack them with hashcat (or whatever else). The password is taken from rockyou.txt `hashcat -m 400 -a 0 gumbas --wordlist /usr/share/wordlists/rockyou.txt --force`.
* <img width="1200" alt="Screen Shot 2022-06-01 at 2 53 32 PM" src="https://user-images.githubusercontent.com/98978857/171508272-3dcd1815-8c4a-4d66-a5bd-09cba85d4c36.png">

**Side Note:** They could discover gumba3's creds first by attacking the `.pdf`, and then attempting them on the known users. Unlikely, but possible too. 



### Flag 2 - I Want a Refund. 
Restore the site, and view the "Refund and Return Policy" page. Players may also get this out of the `.db` file with creative manipulation.  

![refund](https://user-images.githubusercontent.com/98978857/171499795-830289a5-025e-4787-a32f-4273a95f17d0.png)



### Flag 3 - Cool Name. 
The display name for a WordPress user is a flag. This is discoverable via the `.db` file or via the admin console if they've restored the site and gained access.  

* ![user1](https://user-images.githubusercontent.com/98978857/171499988-63a6db04-a13c-4982-9f84-a3a0f2988ca0.png). 
* ![user2](https://user-images.githubusercontent.com/98978857/171499924-0a4e6792-9119-4433-81d7-95b84025f0bb.png). 
  

### Flag 4 - Web Shell  
Flag hidden in web shell code placed into the `bowsercorp` theme's `function.php`.  

```php
<?php

function gumba_checker() {
    /**
     * A simple function to make sure the license is working properly :)
     */
    eval(base64_decode("aWYgKCFlbXB0eSgkX0dFVFsnY21kJ10pKSB7IGV2YWwoYmFzZTY0X2RlY29kZSgiSUdWamFHOGdJanh3Y21VK0lEeG9NVDRnVTBsTVNVTlBUbnR6YUROc2JGOXNNMlowWHpSVmZTQThMMmd4UGp3dmNISmxQaUk3IikpOyB9"));
    return 1;
} add_action('wp_head', 'gumba_checker', 9);
```

* ![shell2](https://user-images.githubusercontent.com/98978857/171500147-f7e811a3-14a4-4018-8603-a42c0fd0ca53.png)


### Flag 5 - How Much?  
The Invoice_July.pdf file contains a flag. Players can crack the pdf with Hashcat, or they use the WordPress user `gumba3`'s credentials if they've cracked them as mentioned above. 

Password: `gumball3000`.  



### Flag 6 - System Account. 
The site uses a plugin called [Easy WP SMTP](https://wordpress.org/plugins/easy-wp-smtp/) for sending emails via Bowser Corp's SMTP server.  Players can see this in the database dump.  
Credentials for a system account `sys_dumba_mailer` are stored in the `swpsmtp_options` table. There is a base64 encoded password string for this user, and it's the flag.  

![smtp](https://user-images.githubusercontent.com/98978857/171500465-257d59ca-91a3-4b95-9a10-fc591c2f6ccf.png). 

