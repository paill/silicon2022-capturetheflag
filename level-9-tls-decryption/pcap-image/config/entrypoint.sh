# Main shell script that is run at the time that the Docker image is run

# Go to default.conf directory
cd /etc/nginx/http.d;

# ENV VARS
# A list of environment variables that are passed to the container and their defaults

# Modify nginx.conf file to use TLS 1.2
sed -i "s/ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;/ssl_protocols TLSv1.2;/" /etc/nginx/nginx.conf

# CRT - double check that the file exists
export CRT="${CRT:=nginx-selfsigned.crt}";
if [ -f "/etc/ssl/certs/$CRT" ]
then
    # set crt file in the default.conf file
    sed -i "/ssl_certificate \//c\\\tssl_certificate \/etc\/ssl\/certs\/$CRT;" default.conf;
fi

# KEY - double check that the file exists
export KEY="${KEY:=nginx-selfsigned.key}";
if [ -f "/etc/ssl/private/$KEY" ]
then
    # set key file in the default.conf file
    sed -i "/ssl_certificate_key \//c\\\tssl_certificate_key \/etc\/ssl\/private\/$KEY;" default.conf;
fi

# Needed to make sure nginx is running after the commands are run
nginx -g 'daemon off;'; nginx -s reload;
