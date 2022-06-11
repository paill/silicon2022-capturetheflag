# Flag 1
Find the right index to search in Splunk

Hint1: Try searching for available indexes
    
    | eventcount summarize=false index=*

Hint2: Switch the time picker to "All Time" 
 
Solution: 
    
    index="nothingtoseehere" earliest=0

`SILICON{ImLik3l00k!ngAr0nd4Stuff}`

# Flag 2         
Find the password used to get into the admin site for the server

Hint 1:  Find all the events related to the defaced website. Use thie following SPL in your search:
    
    index="mariobrosplumbing" mariobrosplumbing.com


Hint 2: There are four sourcetypes. Let's take a closer look at the http:stream events and idnetify all the src_ip. Add the follow to the Hint 1 search: 
    
    sourcetype="stream:http" |stats count by src_ip

Hint 3: We also have data in a sourcetype called suricata. That is likely from an Suricata IDS. Let's see if we have any alerts from those IP addresses. Add the follow to the Hint 1 search:  
    
    sourcetype="suricata" |stats count by alert.signature, src_ip

Hint 4: There's an IP that is definitely trying to do bad things. It also looks like that IP is using a web scanning tool. Let's head back to the http:stream events and take a closer look for login attempts not made by the scanner. Remember the despt_ip for later:
    
    index="mariobrosplumbing" sourcetype="stream:http" http_method="POST" src_content="*user*" src_content="*pass*" src_ip=<INSERT_BAD_IP_HERE> NOT <INSERT_WED_SCANNER_NAME_HERE>

Solution:
    
    index="mariobrosplumbing" sourcetype="stream:http" http_method="POST" src_content="*user*" src_content="*pass*" src_ip="40.80.148.42" NOT Acunetix
The flag is in the password in HEX `53494C49434F4E7B4D4072696F31247D`
`SILICON{M@rio1$}`
		
# Flag 3
Find the file uploaded and run to gain a foothold

Hint 1: Let's keep looking in the stream:http sourcetype, look at the POST events, and filter out the Web scanner found in the previous task
        
    index="mariobrosplumbing" sourcetype="stream:http" http_method=POST

Hint 2: Let's narrow further by filter on our web servers IP, the dest_ip from the previous task
    
    index="mariobrosplumbing" sourcetype="stream:http" http_method=POST NOT <INSERT_WED_SCANNER_NAME_HERE> dest_ip=<INSERT_WEB_SERVER_IP_HERE>

Hint 3: The web server is Windows running IIS, so let's look for the .exe file uploaded.
    
    index="mariobrosplumbing" sourcetype="stream:http" http_method=POST NOT <INSERT_WED_SCANNER_NAME_HERE> dest_ip=<INSERT_WEB_SERVER_IP_HERE> ".exe"

Solution:
        
    index="mariobrosplumbing" sourcetype="stream:http" http_method=POST NOT Acunetix dest_ip="192.168.250.70" ".exe"

The flag is in the filename in HEX `53494C49434F4E7B42406446696C337D`
`SILICON{B@dFil3}`

# Flag 4	
Find the file used to deface the customer site and C&C server
    
Hint 1: We know a malicious file was uploaded to our web server from the previous task. Let's see if it ran
    
    index="mariobrosplumbing" sourcetype="xmlwineventlog" "<INSERT_BAD_FILE_NAME_HERE>.exe" 
    | stats count by DestinationIp
    
Hint 2: Because we know the malicious file was executed, let's see what our webserver was doing with the command and control (C&C)server
        
    index="mariobrosplumbing" sourcetype="stream:http"  src_ip=<INSERT_WEB_SERVER_IP_HERE>
    
Solution:
        
    index="mariobrosplumbing" sourcetype="stream:http" src_ip="192.168.250.70"
        
The flag is in jpeg filename in base64 `U0lMSUNPTntFdklsX0Iwd3Mzcn0K`
`SILICON{EvIl_B0ws3r}`