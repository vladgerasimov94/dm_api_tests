import requests

url = "http://localhost:5051/v1/account/login/all"

payload = {}
headers = {
  'X-Dm-Auth-Token': '<string>',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Accept': 'text/plain'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
