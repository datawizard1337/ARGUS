# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:55:05 2018

@author: jki
"""
import configparser
import os
import time


def postprocessing(cwd=None):
    #read settings file
    config = configparser.RawConfigParser()   
    config.read(r".\bin\settings.txt")
    
    #get files
    if config.get('spider-settings', 'spider') == "text":
        merged_file = open(config.get('input-data', 'filepath').split(".")[0] +   "_scraped_texts.csv", "w", encoding="utf-8")
        output = config.get('input-data', 'filepath').split(".")[0] + "_scraped_texts.csv"
    elif config.get('spider-settings', 'spider') == "link":
        merged_file = open(config.get('input-data', 'filepath').split(".")[0] +   "_scraped_links.csv", "w", encoding="utf-8")
        output = config.get('input-data', 'filepath').split(".")[0] + "_scraped_links.csv"
    output_files = [cwd + "\\chunks\\" + f for f in os.listdir(cwd + "\\chunks") if f.split("_")[0] == "output"]

    len_output_files = len(output_files)
    if len_output_files == 0:
        print("Nothing found to postprocess.\nMaybe postprocessing was executed already. Check location:\n{}".format(output))
        return
    if len_output_files >= 10:
        report_ticks = {"5%%": int(len_output_files * 0.05), "15%%": int(len_output_files * 0.15), "25%%": int(len_output_files * 0.25), "50%%": int(len_output_files * 0.50), "75%%": int(len_output_files * 0.75)}

    print("Merging output files to ", output , " ...")
    time.sleep(2)
    
    errors = 0
    tick = 0 
    
    #textspider postprocessing
    if config.get('spider-settings', 'spider') == "text":
        print("Using text spider postprocessing procedure. This may take a few minutes...")
    #merge chunks
        c=0
        for fn in output_files:
            tick += 1
            if len_output_files >= 10:
                if tick in list(report_ticks.values()):
                    print("Processed {} of files".format(report_ticks[tick]))
            f = open(fn, encoding="utf-8")
            #if first file write the column names
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
            
    #linkspider postprocessing
    elif config.get('spider-settings', 'spider') == "link":
        print("Using link spider postprocessing procedure. This may take a few minutes...")
        #generate list of all internal (given in user url list) domains
        all_internal_links = []
        for fn in output_files:
            f = open(fn, encoding="utf-8")
            f.readline()
            while 1:
                try:
                    line = f.readline()
                    if not line:
                        break
                    if line == "\n":
                        continue
                    line = line.split("\t")
                    dl_slot = line[2]
                    if dl_slot not in all_internal_links:
                        all_internal_links.append(dl_slot)
                except:
                    errors += 1
                    continue
            f.close()
        #write outputfile
        c=0
        for fn in output_files:
            tick += 1
            if len_output_files >= 10:
                if tick in list(report_ticks.values()):
                    print("Processed {} of files".format(report_ticks[tick]))
            f = open(fn, encoding="utf-8")
            #if first chunk write the column names
            if c == 0:
                line = f.readline().split("\t")
                first_line = line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + "links_internal" + "\t" + "links_external" + "\t" + line[5] + "\t"  + line[6] + "\t" + line[7]
                merged_file.write(first_line)
                c+=1
            #for other chunks, skip first line
            else:
                f.readline()
           
            #iterate lines and extract links, divide into internal and external links, write to output file
            while 1:
                try:
                    line = f.readline()
                    if not line:
                        break
                    if line == "\n":
                        continue
                    line = line.split("\t")
                    links = line[4].split(",")
                    #lists to collect links which are either from initial/internal population or from external websites
                    #first item is self --> easier to import into analysis software later on
                    links_internal = [line[2]]
                    links_external = [line[2]]
                    for link in links:
                        if link == "":
                            continue
                        #if the link is from the internal population...
                        if link in all_internal_links:
                            #...and has not been saved yet, add to internal links
                            if link not in links_internal:
                                links_internal.append(link)
                        #...if not from internal population add to external population
                        else:
                            links_external.append(link)
                            
                    #create output string
                    if len(links_internal) == 1:
                        links_internal = ""
                    else:
                        links_internal = ",".join(links_internal)   
                    if len(links_external) == 1:
                        links_external = ""
                    else:
                        links_external = ",".join(links_external)
        
                    #write to output file                    
                    output_line = line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + links_internal + "\t" + links_external + "\t" + line[5] + "\t"  + line[6] + "\t" + line[7]
                    merged_file.write(output_line)
                except:
                    errors += 1
                    continue
            f.close()        
    merged_file.close()    
    
    print("Merging done. Skipped {} websites because of formatting errors. Deleting leftovers...".format(errors))
    time.sleep(5)
    
    #delete chunks
    chunk_files = [os.getcwd() + "\\chunks\\" + f for f in os.listdir(os.getcwd() + "\\chunks") if f.split("_")[0] == "url"]
    
    for fn in output_files + chunk_files:
        os.unlink(fn)
    print("Postprocessing successful. Scraped data can be found:\n{}".format(output))