import requests

key = "NOT_COMMITTING_THIS_AGAIN"

url = "https://certificationapi.oshwa.org/api/projects?limit=1000"
url1 = "https://certificationapi.oshwa.org/api/projects?limit=1000&offset=1000"

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {key}'
}

products = []
with open('oshwa.txt', 'w') as F:
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json()['limit'])
    for i in response.json()['items']:
        if i["responsibleParty"] == "Adafruit Industries, LLC":
            #product = {}
            #product["name"] = i["projectName"]
            #product["url"] = i["projectWebsite"]
            #product["version"] = i["projectVersion"]
            products.append(i["projectWebsite"].replace("www.", ""))
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    print(response1.json()['offset'])
    for i in response1.json()['items']:
        if i["responsibleParty"] == "Adafruit Industries, LLC":
            #product = {}
            #product["name"] = i["projectName"]
            #product["url"] = i["projectWebsite"]
            #product["version"] = i["projectVersion"]
            products.append(i["projectWebsite"].replace("www.", ""))
    for i in products:
        F.write(str(i)+"\n")
