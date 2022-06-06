#!/usr/bin/python3

import argparse
import os
import sys
import time

def check_tmp_hosts():
    custom_hosts_file_path = "/tmp/hosts"
    expected_host_resolve_string = "wannamammamia.bowsercorp.local:80:127.0.0.1"
    is_host_resolve_string_valid = False

    if not os.path.exists(custom_hosts_file_path):
        return False

    custom_hosts_file = open(custom_hosts_file_path, "r")
    for line in custom_hosts_file.readlines():
        ip_host = line.split()
        if len(ip_host) == 2:
            host_resolve_string = f"{ip_host[1]}:80:{ip_host[0]}"
            if host_resolve_string == expected_host_resolve_string:
                is_host_resolve_string_valid = True
                break
        else:
           return False

    custom_hosts_file.close()

    if is_host_resolve_string_valid:
        return True
    else:
        return False


def dns_packet_sniff(valid=False):
    if valid:
        print("""
            Ether / IP / UDP / DNS Qry \"b'wannamammamia.bowsercorp.local.'\"
            Ether / IP / UDP / DNS Ans \"127.0.0.1\"
        """)
    else:
        print("""
            Ether / IP / UDP / DNS Qry \"b'wannamammamia.bowsercorp.local.'\""
            Ether / IP / UDP / DNS Ans
            Ether / IP / ICMP / IPerror / UDPerror / DNS Ans
        """)

def http_packet_sniff(valid=False):
    if valid:
        print("""
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http S
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668 SA
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http A
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http PA / Raw
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668 A
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668 PA / Raw
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http A
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668 PA / Raw
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http A
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668 FA
            Ether / IP / TCP 127.0.0.1:57668 > 127.0.0.1:http FA
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57668
        """)
    else:
        print("""
            Ether / IP / TCP 127.0.0.1:57500 > 127.0.0.1:http S
            Ether / IP / TCP 127.0.0.1:http > 127.0.0.1:57500 RA
        """)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', type=str, required=True, help='network interface name')
    args = parser.parse_args()

    if args.interface != "lo":
        print(f"ERROR: Interface {args.interface} does not exist!")
        sys.exit(1)

    time.sleep(1)
    while True:
        if check_tmp_hosts():
            dns_packet_sniff(valid=True)
            http_packet_sniff()
        else:
            dns_packet_sniff()
        time.sleep(10)
