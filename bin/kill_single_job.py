# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:11:04 2018

@author: jki
"""

import subprocess

jobid = input("Enter job id: ")
def kill_job(jobid=None):
    subprocess.run(r"curl http://localhost:6800/cancel.json -d project=ARGUS -d job={}".format(jobid))