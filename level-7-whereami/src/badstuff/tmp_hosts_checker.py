#!/usr/bin/python3

import sys
import os

custom_hosts_file_path = "/tmp/hosts"
expected_host_resolve_string = "wannamammamia.bowsercorp.local:80:127.0.0.1"
is_host_resolve_string_valid = False

if not os.path.exists(custom_hosts_file_path):
    sys.exit(1)

custom_hosts_file = open(custom_hosts_file_path, "r")
for line in custom_hosts_file.readlines():
    ip_host = line.split()
    if len(ip_host) == 2:
        host_resolve_string = f"{ip_host[1]}:80:{ip_host[0]}"
        if host_resolve_string == expected_host_resolve_string:
            is_host_resolve_string_valid = True
            break
    else:
        sys.exit(2)

custom_hosts_file.close()

if is_host_resolve_string_valid:
    sys.exit(0)
else:
    sys.exit(3)