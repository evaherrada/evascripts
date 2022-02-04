import requests

pids = []
with open('oshwa.txt', 'r') as f:
    for line in f:
        pids.append(int(line[:-1].split('/')[-1]))

products = []
with open('adafruit.txt', 'w') as F:
    r = requests.get('http://adafruit.com/api/products')
    print(r.status_code)
    print(r.headers['content-type'])
    print(r.encoding)
    for i in r.json():
        if i["product_manufacturer"]:
            if i["product_manufacturer"].lower() == "adafruit":
                if i["discontinue_status"].lower() != "discontinued":
                    pid = int(i["product_url"].split('/')[-1])
                    if pid > 4600 and pid not in pids:
                        product = {}
                        product["name"] = i["product_name"]
                        product["url"] = i["product_url"]
                        product["version"] = i["product_model"]
                        product["description"] = ""
                        product["documentation"] = ""
                        products.append(product)
    for i in products:
        F.write(str(i)+"\n")
