# -*- coding: utf-8 -*-
"""
Code to steer ARGUS

Created on Mon Jun  8 16:41:04 2020

@author: JDO
"""

# Modules
import os
import sys
import time

# get path to directory
script_dir = os.path.dirname(__file__)

# Settings
try:
	class argus_settings:   
		os.chdir(script_dir)	# change working directory to project folder
		filepath = sys.argv[1] 	# file path for list containing URLs
		
		# settings for ARGUS spider
		delimiter = "\t"    
		encoding = "utf-8"
		index_col = "id"		# column with IDs
		url_col = "url"		# column with URLs
		lang = "German"		# language
		n_cores = 1		# number of cores
		limit = 10		# scraping limit
		log_level = "INFO"
		prefer_short_urls = "on"

	# Execute scraping
	if __name__ == "__main__":
		os.startfile(script_dir + r"\bin\start_server.bat")		# start scrapyd server
		time.sleep(2)
		# Start crawling
		from bin import start_crawl_steering
		start_crawl_steering.start_crawl()

except:
	print("Usage of script: python script url_list")
