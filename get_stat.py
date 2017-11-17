#!/usr/bin/env python

import requests
import json

tc_url = "myUrl"
print(tc_url)
auth = "myUser", "myPassword"
print(auth)

headers = {'Accept': 'application/json'}

url = tc_url + "/app/rest/buildTypes"
r = requests.get(url, headers=headers, auth=auth, timeout=10)
res = r.json()
print(res)


