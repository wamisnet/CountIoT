import requests
import netifaces
import uptime
import json
import os
Ver = "0.0.3"
Data = {}
Data["version"] = Ver
user = ""
try:
    with open(userPath) as f:
        user = f.read()
except:
    print("Cannot open User File")
interfaces = netifaces.interfaces()
addrslist = []
for interface in interfaces:
    addrs = netifaces.ifaddresses(interface)
    addrslist.append(addrs[netifaces.AF_LINK][0]["addr"])
Data["macAddress"] = addrslist
Data["uptime"] = uptime.uptime()
headers = {'user': user}
response = requests.post('http://cloud.nefry.studio:1880/nefrysetting/countit/polling', data=Data,headers=headers)
print(response.status_code)
print(response.text) 
result = response.json()
print(result) 
if response.status_code == 200:
    if result["update"] == True:
        os.system("bat/gitpull.sh")
    if result["reboot"] == True:
        os.system("bat/reboot.sh")