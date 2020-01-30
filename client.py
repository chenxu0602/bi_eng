import requests, json

url = "http://127.0.0.1:8080/orders"

params1 = {
    "origin": ["22.32", "114.17"],
    "destination": ["21.31", "114.16"]
}

params2 = {
    "origin": ["22.31", "114.18"],
    "destination": ["22.33", "114.14"]
}

res1 = requests.post(url, data=params1)
res2 = requests.post(url, data=params1)

text = res1.text
print(json.loads(text))

text = res2.text
print(json.loads(text))

res = requests.get(url)
text = res.text
print(json.loads(text))

res = requests.patch(url + '/1')
res = requests.patch(url + '/2')
res = requests.patch(url + '/7')

res = requests.get(url)
text = res.text
print(json.loads(text))
