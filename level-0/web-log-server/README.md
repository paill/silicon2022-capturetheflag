docker run -v ${PWD}/httpd:/log -it --rm mingrammer/flog -t log -f apache_combined -o log/apache.log -p 512000 -b 20480000 -w 

sed -i '' -E 's/^[0-9]{1,3}\.[0-9]{1,3}\.([0-9]{1,3})\.([0-9]{1,3}) - .* \[/192.168.\1.\2 - - [/g' httpd/apache*.log 
sed -i '' -E 's/sexy/random/g' httpd/apache*.log 

# pick a file and replace ip with 20.237.204.80

tar czfv apache.log.tar.gz httpd/apache*.log

rm -rf httpd/apache*.log

docker build . -t silicon/challenge_zero_stage_one

## Solutions
* Flag in /tmp/.hellofriend.txt
* Flag at public IP found in /var/log/httpd/apache*.log 
    * Get all unique IPs from logs using `awk '{ print $1}' /var/log/httpd/apache*.log | sort | uniq`. All IPs will be private class C (192.168.x.x) except for one
* Flag after auth bypass
* Flag after getting finding command bypass