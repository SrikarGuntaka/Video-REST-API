import requests

BASE = "http://127.0.0.1:5000/"

put_resp = requests.put(
    BASE + "video/1",
    json={"name": "Test Video", "views": 10, "likes": 1},
)
print({"put_status": put_resp.status_code, "put_body": put_resp.json()})

patch_resp = requests.patch(BASE + "video/1", json={"views": 99})
print({"patch_status": patch_resp.status_code, "patch_body": patch_resp.json()})

get_resp = requests.get(BASE + "video/1")
print({"get_status": get_resp.status_code, "get_body": get_resp.json()})