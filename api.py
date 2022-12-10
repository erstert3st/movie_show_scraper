import requests
print("hi")
response = requests.post("http://10.0.0.13:8110/api/login?username=user&password=user")
print(response)
