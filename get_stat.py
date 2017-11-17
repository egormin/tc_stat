#!/usr/bin/env python

import requests
import sys
sys.path.append("modules")

from beautifultable import BeautifulTable

tc_url = "myUrl"
auth = "myUser", "myPassword"
headers = {'Accept': 'application/json'}


def projects():
    url = tc_url + "/app/rest/projects"
    r = requests.get(url, headers=headers, auth=auth, timeout=10).json()
    return len(r['project'])


def builds():
    url = tc_url + "/app/rest/buildTypes"
    r = requests.get(url, headers=headers, auth=auth, timeout=10).json()
    return len(r['buildType'])

table = BeautifulTable()
table.column_headers = ["Name", "Count"]
table.append_row(["Projects", projects()])
table.append_row(["Build configurations", builds()])
print(table)

