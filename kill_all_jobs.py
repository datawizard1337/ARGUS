# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 13:43:13 2018

@author: jki
"""

import subprocess
import time
import os

process = subprocess.Popen(r"curl http://localhost:6800/listjobs.json?project=ARGUS", stdout=subprocess.PIPE)
l = str(process.stdout.read()).split(",")
for c in l:
    if "id" in c and "pid" not in c:
        ID = str(c.split(":")[-1]).replace('"', '').lstrip()
        subprocess.run(r"curl http://localhost:6800/cancel.json -d project=ARGUS -d job={}".format(ID))
        print("Killed job: ", ID)
 
yn = input("Do you want to delete already scraped data? (y/n): ")

while yn != "y" and yn != "n":
    yn = input("Do you want to delete already scraped data? (y/n): ")
    if yn == "y" or yn == "n":
        break
if yn == "y":  
    print("Killed all jobs. Deleting leftovers...")
    time.sleep(2)
    
    output_files = [os.getcwd() + "\\chunks\\" + f for f in os.listdir(os.getcwd() + "\\chunks") if f.split("_")[0] == "output"]
    chunk_files = [os.getcwd() + "\\chunks\\" + f for f in os.listdir(os.getcwd() + "\\chunks") if f.split("_")[0] == "url"]
    
    for fn in output_files + chunk_files:
        os.unlink(fn)