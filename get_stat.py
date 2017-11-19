#!/usr/bin/env python

import requests
import sys
sys.path.append("modules")

from beautifultable import BeautifulTable

tc_url = "myUrl"
auth = "myUser", "myPassword"
headers = {'Accept': 'application/json'}

from anytree import Node, RenderTree

arch_count = 0
def projects():
    global arch_count
    url = tc_url + "/app/rest/projects"
    r = requests.get(url, headers=headers, auth=auth, timeout=10).json()

    for i in range(0, len(r['project'])):
        if r['project'][i].get('archived'):
            arch_count += 1
    return len(r['project'])


def builds():
    url = tc_url + "/app/rest/buildTypes"
    r = requests.get(url, headers=headers, auth=auth, timeout=10).json()
    return len(r['buildType'])

prj = projects()
builds = builds()
table = BeautifulTable()
table.column_headers = ["Name", "Count"]
table.append_row(["Projects", prj-arch_count])
table.append_row(["Build configurations", builds])
table.append_row(["Archived projects", arch_count])
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

                    # for pre, fill, node in RenderTree(first_l):
                    #     print("%s%s" % (pre, node.name))

        for pre, fill, node in RenderTree(first_l):
            print("%s%s" % (pre, node.name))
    return ""

#print(tree().encode('utf8', 'replace'))
print(tree())

content = "Projects number: {}<br>".format(prj - arch_count)
content += "Build configurations number: {}<br>".format(builds)
content += "Build configurations number: {}".format(arch_count)

f = open('report/index.html', 'w')
f.write(content)
f.close()
