/*

- Where am I? Silicon 2022
- Author: DS-Koolaid

apt-get install gcc
apt-get install libcurl4-openssl-dev

 gcc -Wall whereami.c -lcurl -o whereami

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

size_t write_data(void *buffer, size_t size, size_t nmemb, void *userp);


void XOR(char * data, size_t data_len, char * key, size_t key_len) {
	int j;
	j = 0;
	for (int i = 0; i < data_len; i++) {
		if (j == key_len - 1) j = 0;

		data[i] = data[i] ^ key[j];
		j++;
	}
	
}

int main(void) {

	unsigned char flag[] = { 0x78, 0x47, 0x78, 0xa, 0x13, 0x76, 0x6, 0x11, 0x5c, 0x9, 0x57, 0x55, 0x70, 0xc, 0xf, 0x72, 0x1b, 0x30, 0x48, 0x1a, 0x6d, 0x59, 0x2d, 0x34, 0x1e, 0x2f, 0x68 };
	unsigned int flag_len = sizeof(flag);
	char key[]="91HcwAhvxh";
	// http://evil.corp.local
	unsigned char resolve[] = { 0x51, 0x45, 0x3c, 0x13, 0x4d, 0x6e, 0x47, 0x13, 0xe, 0x1, 0x55, 0x1f, 0x2b, 0xc, 0x5, 0x31, 0x46, 0x1a, 0x17, 0xb, 0x58, 0x5d, 0x48 };
	CURL *curl;
	CURLcode res;
 	curl = curl_easy_init();
  	if(curl) {
  		XOR((char *) resolve, sizeof(resolve), key, sizeof(key));
    	curl_easy_setopt(curl, CURLOPT_URL, resolve);
    	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);

    	res = curl_easy_perform(curl);

    	long http_code = 0;
		curl_easy_getinfo (curl, CURLINFO_RESPONSE_CODE, &http_code);

    	curl_easy_cleanup(curl);
    	if (http_code == 200){
    		XOR((char *) flag, flag_len, key, sizeof(key));
    		printf("Sweet! Our Malware is in the right place.\nFlag: %s\n",flag);
    	}
    	else{
    		printf("How did I end up here?!\n");
    	}
    }
    return 0;
}


size_t write_data(void *buffer, size_t size, size_t nmemb, void *userp)
{
   return size * nmemb;
}
