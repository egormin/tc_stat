#!/usr/bin/env python

import requests
import sys
sys.path.append("modules")

from beautifultable import BeautifulTable

tc_url = "myUrl"
auth = "myUser", "myPassword"
headers = {'Accept': 'application/json'}

from anytree import Node, RenderTree

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


first_lev = []
sec_lev = []
def tree():
    url = tc_url + "/app/rest/projects"
    r = requests.get(url, headers=headers, auth=auth, timeout=10)
    res = r.json()

    for i in range(1, len(res['project'])):
        if res['project'][i]['parentProjectId'] == "_Root":
            first_lev.append(res['project'][i]['id'])

            # array L2
    for i in range(0, len(first_lev)):
        for x in range(0, len(res['project'])):
            if res['project'][x]['id'] == first_lev[i]:
                first_l = Node(res['project'][x]['name'])

        sec_lev = []
        for x in range(1, len(res['project'])):
            if res['project'][x]['parentProjectId'] == first_lev[i]:
                sec_lev.append(res['project'][x]['id'])

        for j in range(0, len(sec_lev)):
            for x in range(0, len(res['project'])):
                if res['project'][x]['id'] == sec_lev[j]:
                    second_l = Node(res['project'][x]['name'], parent=first_l)

            for m in range(1, len(res['project'])):
                if res['project'][m]['parentProjectId'] == sec_lev[j]:
                    third_l = Node(res['project'][m]['name'], parent=second_l)


        for pre, fill, node in RenderTree(first_l):
            print("%s%s" % (pre.encode('utf8', 'replace'), node.name.encode('utf8', 'replace')))
    return ""

print(tree())



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
f.write(headder + content1 + content2 + str(content3) + footer)
f.close()


