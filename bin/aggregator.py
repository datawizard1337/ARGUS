# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:01:19 2018

@author: JKI
"""

import pandas as pd

def aggregate_webpages(filepath=None):
    try:
        filename = filepath.split("\\")[0]
        data = pd.read_csv(filename, encoding="utf-8", sep="\t", error_bad_lines=False, chunksize=25000)
        outputfile = open(filename.split(".")[0] + "_aggregated.csv", "w", encoding='utf-8')
        outputfile.write("ID" + "\t" + "dl_rank" + "\t" + "dl_slot" + "\t" + "error" + "\t" + "redirect" + "\t" + "start_page" + "\t" + "title" + "\t" + "keywords" + "\t" + "description" + "\t" + "text" + "\t" + "timestamp\n")
        
        c=0
        # iterate chunks
        for chunk in data:
            # chunk data
            IDs = chunk["ID"].values.tolist()
            errors = chunk["error"].values.tolist()
            redirects = chunk["redirect"].values.tolist()
            start_pages = chunk["start_page"].values.tolist()
            timestamps = chunk["timestamp"].values.tolist()
            texts = chunk["text"].values.tolist()
            dl_slots = chunk["dl_slot"].values.tolist()
            dl_ranks = chunk["dl_rank"].values.tolist()
            titles = chunk["title"].values.tolist()
            keywordss = chunk["keywords"].values.tolist()
            descriptions = chunk["description"].values.tolist()
            output = ""
            
            # iterate webpage texts
            for i, text in enumerate(texts):
                if str(text) == "nan":
                    text = ""
                
                # if first webpage, initialize aggregator
                if c==0:
                    dl_slot = dl_slots[i]
                    website_text = text
                    dl_rank = dl_ranks[i]
                    ID = IDs[i]
                    error = errors[i]
                    start_page = start_pages[i]
                    timestamp = timestamps[i]
                    redirect = redirects[i]
                    title = titles[i]
                    keywords = keywordss[i]
                    description = descriptions[i]
                    c+=1
                
                # if not same webpage, write and empty aggregator
                if dl_slots[i] != dl_slot:
                    output = output + "\t".join([str(x) for x in [ID, dl_rank, dl_slot, error, redirect, start_page, title, keywords, description, website_text, timestamp]]) + "\n"
                    dl_slot = dl_slots[i]
                    website_text = text
                    dl_rank = dl_ranks[i]
                    ID = IDs[i]
                    error = errors[i]
                    start_page = start_pages[i]
                    timestamp = timestamps[i]
                    redirect = redirects[i]
                    title = titles[i]
                    keywords = keywordss[i]
                    description = descriptions[i]
                
                # if same website, aggregate texts
                website_text = website_text + text
                dl_rank = dl_ranks[i]
            outputfile.write(output)
            
        outputfile.close()
        return filename.split(".")[0] + "_aggregated.csv"
    except:
        print("Error! Please select a file containing webpage-level text spider output.")