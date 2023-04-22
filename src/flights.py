import requests

url = "https://skyscanner50.p.rapidapi.com/api/v1/searchFlightEverywhereDetails"

querystring = {"origin":"LOND","CountryId":"US","anytime":"true","oneWay":"true","currency":"EUR","countryCode":"US","market":"en-US"}

headers = {
"X-RapidAPI-Key": "22408fc45bmsh753eabf966f3a11p1b7fc4jsne32992c3e5ee",
"X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)