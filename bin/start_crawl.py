# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import configparser
import math
import time
import subprocess
import os
import webbrowser


def start_crawl():
	#read config file
	config = configparser.RawConfigParser()   
	config.read(r".\bin\settings.txt")

	#check path
	error_message = """
	ABORTING

	ARGUS directory path:
	{}
	includes at least one dot "."
	This will cause problems with ARGUS.
	Please rename or move ARGUS before you continue.
	""".format(os.getcwd())

	if len(os.getcwd().split(".")) > 1:
		print(error_message)
		time.sleep(3)
	else:
		#read URL file
		data = pd.read_csv(config.get('input-data', 'filepath'), delimiter=config.get('input-data', 'delimiter'), 
						   encoding=config.get('input-data', 'encoding'), index_col=config.get('input-data', 'ID'), error_bad_lines=False, engine="python")

		#get ISO codes for language detection
		if config.get('spider-settings', 'language') == "None":
			language_ISOs = ""
		else:
			language = config.get('spider-settings', 'language')
			ISO_codes = pd.read_csv(os.getcwd() + "\\misc\\ISO_language_codes.txt", delimiter="\t", encoding="utf-8", error_bad_lines=False, engine="python")
			language_ISOs = ISO_codes.loc[ISO_codes["language"] == language][["ISO1","ISO2","ISO3"]].iloc[0].tolist()
			language_ISOs = "{},{},{}".format(language_ISOs[0], language_ISOs[1], language_ISOs[2])
			
		#define number of url chunks to be created from URL file
		n_url_chunks = math.ceil(len(data)/10000)
		if n_url_chunks < int(config.get('system', 'n_cores')):
			n_url_chunks = int(config.get('system', 'n_cores'))

		#generate url chunks
		p = 1
		for chunk in np.array_split(data, n_url_chunks):
			chunk.to_csv(os.getcwd() +"\\chunks\\url_chunk_p" + str(p) + ".csv", sep="\t", encoding="utf-8")
			p+=1
			
		print("Splitted your URLs into ", n_url_chunks, " parts.")
		time.sleep(3)

		#schedule scrapyd jobs
		for p in range(1, n_url_chunks+1):
			url_chunk = os.getcwd() + "\\chunks\\url_chunk_p" + str(p) + ".csv"
			#schedule textspider
			if config.get('spider-settings', 'spider') == "text":
				subprocess.run("curl http://localhost:6800/schedule.json -d project=ARGUS -d spider=textspider -d url_chunk={} -d limit={} -d ID={} -d url_col={} -d language={} -d setting=LOG_LEVEL={} -d prefer_short_urls={}"
						   .format(url_chunk, config.get('spider-settings', 'limit'), config.get('input-data', 'ID'), config.get('input-data', 'url'), language_ISOs, config.get('spider-settings', 'log_level'), config.get('spider-settings', 'prefer_short_urls')))
			#schedule linkspider
			elif config.get('spider-settings', 'spider') == "link":
				subprocess.run("curl http://localhost:6800/schedule.json -d project=ARGUS -d spider=linkspider -d url_chunk={} -d limit={} -d ID={} -d url_col={} -d language={} -d setting=LOG_LEVEL={} -d prefer_short_urls={}"
						   .format(url_chunk, config.get('spider-settings', 'limit'), config.get('input-data', 'ID'), config.get('input-data', 'url'), language_ISOs, config.get('spider-settings', 'log_level'), config.get('spider-settings', 'prefer_short_urls')))
			#schedule dual
			elif config.get('spider-settings', 'spider') == "dual":
				subprocess.run("curl http://localhost:6800/schedule.json -d project=ARGUS -d spider=dualspider -d url_chunk={} -d limit={} -d ID={} -d url_col={} -d language={} -d setting=LOG_LEVEL={} -d prefer_short_urls={}"
						   .format(url_chunk, config.get('spider-settings', 'limit'), config.get('input-data', 'ID'), config.get('input-data', 'url'), language_ISOs, config.get('spider-settings', 'log_level'), config.get('spider-settings', 'prefer_short_urls')))

						   
		print("Scheduled ", n_url_chunks, " spiders to scrape your URLs.\nOpening web interface...")
		time.sleep(3)
		webbrowser.open("http://127.0.0.1:6800/", new=0, autoraise=True)