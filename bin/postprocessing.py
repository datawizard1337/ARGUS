# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:55:05 2018

@author: jki
"""
import configparser
import os
import time
from tkinter import messagebox
import glob
import shutil
import datetime

start_time=time.time()

def postprocessing(cwd=None):
    #read settings file
    config = configparser.RawConfigParser()   
    config.read(r".\bin\settings.txt")
    
    output_files = [cwd + "\\chunks\\" + f for f in os.listdir(cwd + "\\chunks") if f.startswith('ARGUS_chunk')]
    output = config.get('input-data', 'filepath').split(".")[0]

    len_output_files = len(output_files)
    if len_output_files == 0:
        messagebox.showinfo("Nothing found to postprocess", "Nothing found to postprocess.\nMaybe postprocessing was executed already. Check location:\n{}".format(output))
        return
    
    errors = 0
    tick = 0

    #dualspider postprocessing
    if config.get('spider-settings', 'spider') == "dual":
        print("Using dual spider postprocessing procedure. This may take a few minutes...")
        
        os.chdir(cwd + "\\chunks")
        out_filename = output + "_scraped_texts.csv"

        # get all files that start with ARGUS_chunk_
        allFiles = glob.glob('ARGUS_chunk_*') 
        with open(out_filename, 'wb') as outfile:
            for i, filenames in enumerate(allFiles):
                if filenames == out_filename:
                    continue
                with open(filenames, 'rb') as readfile:
                    if i != 0:
                        readfile.readline()  # skip header on all but first file
                    shutil.copyfileobj(readfile, outfile)
                    
                    tick += 1

                    if tick == int(len_output_files * 0.05):
                        print (r"Processed 5 % of files")
                    elif tick == int(len_output_files * 0.15):
                        print (r"Processed 15 % of files")
                    elif tick == int(len_output_files * 0.25):
                        print (r"Processed 25 % of files")
                    elif tick == int(len_output_files * 0.50):
                        print (r"Processed 50 % of files")
                    elif tick == int(len_output_files * 0.75):
                        print (r"Processed 75 % of files")
                    elif tick == int(len_output_files):
                        print (r"Processed 100 % of files")
    
    print("Merging done. Skipped {} websites because of formatting errors. Deleting leftovers...".format(errors))
    time.sleep(5)
    
    #delete chunks
    extension = 'csv'
    chunk_files = [fn for fn in glob.glob('*.{}'.format(extension)) if fn.split("_")[0] == "url"]
    
    for fn in output_files + chunk_files:
        os.unlink(fn)
    
    end_time=time.time()
    time_difference = end_time - start_time
    print("Time needed for postprocessing: ", str(datetime.timedelta(seconds=time_difference)))

    messagebox.showinfo("Postprocessing successful", "Postprocessing successful. Scraped data can be found:\n{}".format(output + "_scraped_texts.csv"))



