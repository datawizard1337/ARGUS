# -*- coding: utf-8 -*-

import pandas as pd
import glob
import os
import configparser
import time
from bin import start_crawl

script_dir = os.path.dirname(__file__)  ###
script_dir_edit = str(script_dir)[:-4] 

def skipped_urls():

    #############################################
    # get all URLs that have not yet been scraped
    #############################################

    # read settings file
    config = configparser.RawConfigParser()   
    config.read(script_dir + r"\settings.txt")

    # read original URL list
    urllist = pd.read_csv(config.get('input-data', 'filepath'), sep="\t", encoding="utf-8", error_bad_lines=False)
    url_column = str(config.get('input-data', 'url'))
    initial_urls = urllist[url_column].values.tolist()

    # get all chunks
    #chunks = glob.glob(os.path.abspath(os.path.join(script_dir_edit + "\chunks", "*.csv")))

    scraped_urls = []

    # get every scraped url (including URLS with error) and add them to list 
    #only_ARGUS_chunk = (chunk for chunk in chunks if chunk.startswith('ARGUS_chunk'))

    argus_chunks = [script_dir_edit + "\\chunks\\" + f for f in os.listdir(script_dir_edit + "\\chunks") if f.startswith('ARGUS_chunk')]

    for chunk in argus_chunks:
        for url in pd.read_csv(chunk, sep="\t", encoding="utf-8")["dl_slot"].values.tolist():
            scraped_urls.append("www." + str(url))

    print("Number of non-scraped URLs: ", len(list(set(initial_urls) - set(scraped_urls))))

    # write skipped URLs to new list for further scraping
    new_urllist = config.get('input-data', 'filepath').split(".")[0] + "_skipped_urls.txt"
    urllist[urllist[url_column].isin(list(set(initial_urls) - set(scraped_urls)))].to_csv(new_urllist, sep="\t", encoding="utf-8", index=False)

    #############################
    # start new scraping process
    #############################

    # overwrite previous settings file
    settings_txt = open(script_dir + r"\settings.txt", "r", encoding="utf-8")
    filepath = config.get('input-data', 'filepath')
    new_file = ""
    for line in settings_txt:
        stripped_line = line.strip()
        new_line = stripped_line.replace(filepath, new_urllist)
        new_file += new_line + "\n"
    settings_txt.close()

    write_new_file = open(script_dir + r"\settings.txt", "w", encoding="utf-8")
    write_new_file.write(new_file)
    write_new_file.truncate()
    write_new_file.close()

    # start crawl
    print("Starting server in separate windows...")
    time.sleep(2)
    os.startfile(script_dir + r"\start_server.bat")
    time.sleep(2)
    scraping_type = "skipped"
    start_crawl.start_crawl(scraping_type)
    print("Web scraping started. Do not close server window.")
