# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 13:43:13 2018

@author: jki
"""

import subprocess

liste = subprocess.call(r"curl http://localhost:6800/listjobs.json?project=prototyp")
print(liste)

process = subprocess.Popen(r"curl http://localhost:6800/listjobs.json?project=prototyp", stdout=subprocess.PIPE)
l = str(process.stdout.read()).split(",")
for c in l:
    if "id" in c and "pid" not in c:
        ID = str(c.split(":")[-1]).replace('"', '').lstrip()
        print(r"curl http://localhost:6800/cancel.json -d project=prototyp -d job={}".format(ID))
        subprocess.run(r"curl http://localhost:6800/cancel.json -d project=prototyp -d job={}".format(ID))
        print("Killed process: ", ID)