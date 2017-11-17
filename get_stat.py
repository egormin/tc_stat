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

prj = projects()
builds = builds()
table = BeautifulTable()
table.column_headers = ["Name", "Count"]
table.append_row(["Projects", prj])
table.append_row(["Build configurations", builds])
print(table)

headder = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Report</title>
</head>
<body bgcolor="#d2691e">
<table border="1">
"""

footer = """
</table>
</body>
</html>"""

content1 = "<tr><td>Projects counter: </td><td>{}</td></tr>".format(prj)
content2 = "<tr><td>Projects counter: </td><td>{}</td></tr>".format(builds)
content3 = table

f = open('report/index.html', 'w')
f.write(headder + content1 + content2 + content3 + footer)
f.close()


