# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:55:05 2018

@author: jki
"""
import configparser
import os
import time

config = configparser.RawConfigParser()   
config.read("settings.txt")

merged_file = open(config.get('input-data', 'filepath').split(".")[0] +   "_scraped.csv", "w", encoding="utf-8")
output_files = [os.getcwd() + "\\chunks\\" + f for f in os.listdir(os.getcwd() + "\\chunks") if f.split("_")[0] == "output"]

print("Merging output files to ", config.get('input-data', 'filepath').split(".")[0] + "_scraped.csv", " ...")
time.sleep(2)

c=0
for fn in output_files:   
    f = open(fn, encoding="utf-8")
    if c == 0:
        merged_file.write(f.readline())
        c+=1
    else:
        f.readline()
    while 1:
        line = f.readline()
        if not line:
            break
        merged_file.write(line)
    f.close()
    
merged_file.close()    

print("Merging done. Deleting leftovers...")
time.sleep(2)

#chunk_files = [os.getcwd() + "\\chunks\\" + f for f in os.listdir(os.getcwd() + "\\chunks") if f.split("_")[0] == "url"]

#for fn in output_files + chunk_files:
#    os.unlink(fn)
    


