import requests
import json

url = "http://localhost:5051/v1/account/password"

payload = json.dumps({
  "login": "<string>",
  "token": "<uuid>",
  "oldPassword": "<string>",
  "newPassword": "<string>"
})
headers = {
  'X-Dm-Auth-Token': '<string>',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
