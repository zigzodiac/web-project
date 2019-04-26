import requests
import json

url = "http://localhost:8080/api/files/copy"
data = {'Name': 'Lance', 
'Files': [{'Local': r'C:\test1.iso', 'Ftp': r'E:\Utils\CentOS-6.9-x86_64-bin-DVD1.iso'}, 
        {'Local': r'C:\test2.exe', 'Ftp': r'E:\Utils\bitnami-redmine-3.4.2-3-windows-installer.exe'}]}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

print r