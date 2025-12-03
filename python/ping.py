import requests

url = "https://oracleapex.com/ords/astroneer_wksp/rest/dummy"

payload = {"data":["test"],"response": {    
  "format": "json"   
 }}
headers={'content-type': 'application/json'}
response = requests.post(url, headers=headers, data=payload)

print(response.text)