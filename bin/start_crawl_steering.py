# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
#import configparser
import math
import time
import subprocess
import os
import webbrowser


script_dir = os.path.dirname(__file__) 
script_dir_edit = str(script_dir)[:-4] 
    
# %% Crawl:
def start_crawl():
    # Import setting parameters
    from ARGUS_steering import argus_settings

    filepath = argus_settings.filepath 
    delimiter = argus_settings.delimiter    
    encoding = argus_settings.encoding
    index_col = argus_settings.index_col
    url_col = argus_settings.url_col
    lang = argus_settings.lang
    n_cores = argus_settings.n_cores
    limit = argus_settings.limit
    log_level = argus_settings.log_level
    prefer_short_urls = argus_settings.prefer_short_urls

	#check path
    error_message = """
	ABORTING

	ARGUS directory path:
	{}
	includes at least one dot "."
	This will cause problems with ARGUS.
	Please rename or move ARGUS before you continue.
	""".format(script_dir)


    if len(script_dir.split(".")) > 1:
        print(error_message)
        time.sleep(3)
    else:
		#read URL file
        data = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding, index_col=index_col, error_bad_lines=False, engine="python")

		#get ISO codes for language detection
        if lang == "None":
            language_ISOs = ""
        else:
			
            language = lang
            ISO_codes = pd.read_csv(script_dir_edit + r"\misc\ISO_language_codes.txt", delimiter="\t", encoding="utf-8", error_bad_lines=False, engine="python")
            language_ISOs = ISO_codes.loc[ISO_codes["language"] == language][["ISO1","ISO2","ISO3"]].iloc[0].tolist()
            language_ISOs = "{},{},{}".format(language_ISOs[0], language_ISOs[1], language_ISOs[2])
			
		#define number of url chunks to be created from URL file
        n_url_chunks = math.ceil(len(data)/10000)
        if n_url_chunks < int(n_cores):
            n_url_chunks = int(n_cores)

		#generate url chunks
        p = 1
        for chunk in np.array_split(data, n_url_chunks):
            chunk.to_csv(script_dir_edit +"\\chunks\\url_chunk_p" + str(p) + ".csv", sep="\t", encoding="utf-8")
            p+=1
			
        print("Splitted your URLs into ", n_url_chunks, " parts.")
        time.sleep(3)

		#schedule scrapyd jobs
        for p in range(1, n_url_chunks+1):
            url_chunk = script_dir_edit + "\\chunks\\url_chunk_p" + str(p) + ".csv"
			#schedule dual
            subprocess.run("curl http://localhost:6800/schedule.json -d project=ARGUS -d spider=dualspider -d url_chunk={} -d limit={} -d ID={} -d url_col={} -d language={} -d setting=LOG_LEVEL={} -d prefer_short_urls={}"
                           .format(url_chunk, limit, index_col, url_col, language_ISOs, log_level, prefer_short_urls))
						   
	   
        print("Scheduled ", n_url_chunks, " spiders to scrape your URLs.\nOpening web interface...")
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:6800/", new=0, autoraise=True)
