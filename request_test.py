import requests 

payload = 'http://vulnweb.com/'

data = 'Host: testphp.vulnweb.com'

response = requests.post(payload, headers=data)
print(response.status_code)