# ARGUS: **A**utomated **R**obot for **G**eneric **U**niversal **S**craping

<p align="center">
  <img src="https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/ARGUS_logo.png?raw=true">
</p>

ARGUS is an easy-to-use web scraping tool. The program is based on the Scrapy Python framework and is able to crawl a broad range of different websites. On these websites, ARGUS performs tasks like scraping texts or collecting hyperlinks between websites.
See related paper: https://link.springer.com/article/10.1007/s11192-020-03726-9

Here you can find two scientific papers using ARGUS scraped web data: 
"Predicting Innovative Firms using Web Mining and Deep Learning": http://ftp.zew.de/pub/zew-docs/dp/dp19001.pdf 
"The Digital Layer: How innovative firms relate on the Web": http://ftp.zew.de/pub/zew-docs/dp/dp20003.pdf

## Getting Started

These instructions will get you a copy of ARGUS up and running on your local machine.

Follow these easy steps, which are described in more detail below, to make a successful ARGUS scraping run:
1.  Install Python 3.6 or newer
2.  Install additional Python packages (see Prerequisites below).
3.  Install cURL and add a cURL environment variable to your system (see below).
4.  Download and extract the ARGUS files.
5.  Start scraping via ARGUS.exe or the ARGUS_noGUI.py file.
6.  Check the scraping process using the web interface and wait until it is finished.
7.  Run postprocessing from ARGUS.exe.


### Prerequisites

ARGUS works with Python 3.6 or higher, is based on the Scrapy framework and has the following Python package dependencies:

*	Scrapy 
*	scrapyd
*	scrapyd-client
*	scrapy-fake-useragent 
*	tldextract
*	pandas 
*   pywin32
*	pdfminer.six
*	urllib

Installation of scrapyd requires you to install [C++ Build Tools](https://www.microsoft.com/en-US/download/details.aspx?id=48159) first. Additionally, you need [cURL](https://curl.haxx.se/download.html) to communicate with the ARGUS user interface. An executable Windows 64bit version of cURL can be downloaded [here](https://dl.uxnr.de/build/curl/curl_winssl_msys2_mingw64_stc/curl-7.59.0/curl-7.59.0.zip), for example.
After downloading and extracting, you need to add a cURL environment variable to your system. See [this Stackoverlow thread](https://stackoverflow.com/questions/9507353/how-do-i-install-set-up-and-use-curl-on-windows) if you do not know how to do that.

### Installing

If you are not using Python yet, the easiest way to install Python 3.6 and most of its crucial packages is to use the [Anaconda Distribution](https://www.anaconda.com/download/). Make sure that a Python environment variable was set during the installation. See [this Stackoverlow thread](https://stackoverflow.com/questions/34030373/anaconda-path-environment-variable-in-windows) if you do not know how to do that. Do the same for the Anaconda script folder in "Anaconda3\Scripts".
After installing Anaconda, you can use pip to install the packages above by typing “pip install package_name” (e.g., “pip install scrapy”) into your system command prompt. 


## Start Scraping

**Warning: Please make sure that ARGUS and your URL file are not located in directories with paths containing ".", e.g. "C:\my.folder\data.txt"!**

Either use the ARGUS GUI to start your scraping run:

![ARGUS_GUI](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/ARGUS_GUI.png?raw=true)

Alternatively you may edit the parameters in the **ARGUS_noGUI.py** file and then start it with the shell command **python ./ARGUS_noGUI.py 'c:/my_urls.txt'**. 

![ARGUS_GUI](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/ARGUS_noGUI.png?raw=true)

### File Settings

All parameters that are necessary are marked with an asterisk ***** in the GUI. The other parameters are optional.

-	**Browse** – browse for your file containing website URLs and IDs. The file should be without BOM (byte order mark). An easy way to see whether your text file uses BOM is to use [Notepad++](https://notepad-plus-plus.org/) and check the “Encoding” in the top panel. The URLs need to be in the format “www.example.com”. The directory of your URL list will also be used to output the scraped data. An example website address can be found in /misc:


![example url list](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/url_list.PNG?raw=true)

-	**Delimiter** – the type of delimiter your text file uses. ARGUS takes the following options: *Tab*, *Whitespace*, *Semicolon*, *Comma*.
-	**Encoding** – the encoding of your text file. ARGUS takes the following options: *UTF-8*, *Latin-1*, *ASCII*.
-	**Load Columns** – after defining your file, delimiter, and column, hit this button to load column names.
-	**ID Column** – the field name of your unique website identifier in your website address file.
-	**URL Column** – the field name of your URLs in your website address file. Make sure there are no empty URL entries (rows) in your data.

### Web Scraper Settings

-	**Parallel Processes** – the number of processor cores you want to dedicate to the ARGUS scraping process. It is recommended to use the total number of cores in your system -1 (i.e. if you have a quad-core processor with 4 cores, you should choose 3 cores).
-	**Scrape Limit** – the maximum number of subpages (including the main/starting page) that will be scraped per domain. Set this to 0 if you want to scrape entire websites (caution is advised, as there are websites with ten-thousands of subpages).
-	**Prefer Short URLs** – select whether you want ARGUS to prefer downloading the shortest hyperlinks it finds on a website first. ARGUS usually starts at the website’s main page and there it collects all hyperlinks directing to the website’s subpages. After processing the website’s main page, ARGUS follows the found hyperlinks to do the same to website’s subpages until it reaches the set **Scrape Limit**. If **Prefer Short URLs** is set to “on”, ARGUS will first visit those subpages with the shortest URLs. The reasoning behind that is that one can assume that the most general (and arguably most important) information is located at the website’s top level webpages (e.g. www.example.com/products).
-	**Preferred Language** – the language that will be preferred when selecting the next subpage URL (analogous to **Prefer Short URLs**). Note that this simple heuristic just checks the URL for certain [ISO language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). The complete list of ISO codes is provided within the GUI. If you do not want to use this heuristic, select *None*.

### Advanced Settings

-	**Logging Level** – the amount of information that is stored in scraping log files. For larger scraping runs, the log level should be set to *INFO*. ARGUS provides the following options: *DEBUG*, *INFO*, *WARNING*, *ERROR*, *CRITICAL*.
-	**Download Maxsize** – define the maximum size of a webpage or pdf in MB that should be considered.
-	**Timeout** – define the number of seconds the scraper should wait until a timeout error is assigned to a non-responding website.

### Start Scraping

Hit **Start Scraping** when all your settings are correct. This will open up a seperate Scrapy server that should not be closed during the following scraping run. 

Your list of URLs will be split into handy chunks and a separate job will be started for each chunk to speed up the scraping process.  After all jobs were scheduled, the scrapyd web interface will open up in your default web browser (you can also get there by typing “http://127.0.0.1:6800/” into your web browser).

![scrapyd server](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/scrapyd_server.png?raw=true)

### Stopping jobs

Sometimes certain jobs stop working or never finish, so you may want to stop and restart them. This can be done by hitting **Terminate Job**. You will be asked for the ID of the job you want to cancel. The ID is a long hash number which can be found in the “Job” column in the “Jobs” web interface section.
![scrapyd jobs](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/scrapyd_jobs.PNG?raw=true)

You can stop all processes at once by clicking **Stop Scraping**. You will be asked whether you want to delete the data that has already been scraped. If you decide against deleting the scraped data, you may want to run **Postprocessing** to process your already scraped data (see below).

### Postprocessing

When all jobs are finished (or you decided to **Stop Scraping**), you need to hit **Postprocessing** which writes your scraped data to the directory of your input data and does some clean up. Depending on the size of your output, this might take some time.

### Aggregate Webpage Texts

By default, texts downloaded will be stored at the webpage level (see *Output data* below). If you need your texts aggregated at the website level, run **Aggregate Webpage Texts**.


## Output data

The output file can be found in the same directory your original website address file is located. 

One row equals one webpage and n (n ≤ **Scrape limit**) webpages equal one website (identified by its ID).

![ARGUS textspider output](https://github.com/datawizard1337/ARGUS/blob/dualspider_pdf/misc/pics/ARGUS_dualspider.png?raw=true)
*	**ID** – the ID of the website as given in **ID Column**.
*	**dl_rank** – the chronological order the webpage was downloaded. The main page of a website (i.e. the URL in your website address file) has rank 0, the first subpage processed after the main page has rank 1, and so on.
*	**dl_slot** – the domain name of the website as found in the user given website address list.
*	**alias** – if there was an initial redirect (e.g. from www.example.de to www.example.com), the domain the spider got redirected to ("example.com" in the example) becomes the websites alias.
*	**error** – not “None” if there was an error requesting the website’s main page. Can be an HTML error (e.g., “404”), DNS lookup error, or a timeout.
*	**redirect** – is “True” if there was a redirect to another domain when requesting the first webpage from a website. This may indicate that ARGUS scraped a different website than intended. However, it may also be a less severe redirect like “www.example.de” to “www.example.com”. It is your responsibility to deal with redirects.
*	**start_page** – gives you the first webpage that was scraped from this website. Usually, this should be the URL given in your website address file.
*	**title** – the title of the website as indicated in the website's meta data.
*	**keywords** – the keywords as indicated in the website's meta data.
*	**description** – a short description of the website as indicated in the website's meta data.
*	**language** – the language of the website as indicated in the website's HTML code.
*	**text** – the text that was downloaded from the webpage. It includes the respective HTML tags or the tag <pdf> if the text was extracted from an online PDF.
*	**links** – the domains of websites (*within-sample* and *out-of-sample*) found on the focal website. The field is empty if no hyperlinks were found.
*	**timestamp** – the exact time when the webpage was downloaded.
*	**url** – the URL of the webpage.


## How ARGUS works

An ARGUS crawl is based on a list of user given firm website addresses (URL) and proceeds as follows:
1.	The first webpage (a website’s main page) is requested using the first address in the given URL list.
2.	A collector item is instantiated, which is used to collect the website’s content, meta-data (e.g. timestamps, number of scraped URLs etc.) and a so-called URL stack.
3.	The main page is processed:
    -	Content from the main page is extracted and stored in the collector item.
    -	URLs which refer to subpages of the same website (i.e. domain) are extracted and stored in the collector item’s URL stack.
4.	The algorithm continues to request subpages of the website using URLs from the URL stack. Hereby, it can use a simple heuristic which gives higher priority to short URLs and those URLs which refer to subpages in a predefined language.
    -	Content and URLs are collected from the subpage and stored in the collector item.
    -	The next URL in the URL stack is processed.
5.	The algorithm stops processing a domain when all subpages or a predefined number of subpages per domain have been processed.
6.	The collected content is processed and written to an output file.
7.	The next website is processed by requesting the next URL from the user given URL list. The described process continues until all websites from the user given list have been processed.


## FAQ

**Why does ARGUS.exe not open?**
-	Check whether you have installed all the necessary prerequisites.
-	The issue might be related to your scrapyd installation. Try opening the ARGUS.py in your command line and check for the error messages. A re-installation of some packages (e.g. lxml and numpy, depending on your error message) can help.
-	In some cases the ARGUS_noGUI.py should work nonetheless.
-	Check whether you have changed the inner structure of ARGUS. The ARGUS.exe should be under …/ARGUS-master/ARGUS-master/ARGUS.exe.
-	It is also conceivable that problems are caused by another, interfering Python installation on your computer. Therefore, it is recommended to only have one Python installation while using ARGUS.

**ARGUS opens and starts scraping, but there is no output. What is the problem?**
-	This is probably related to scrapyd. Try opening the scrapyd server manually before starting ARGUS. Just type ‘scrapyd’ into your command line. You might need to re-install some packages, depending on the error message you receive.
-	If you already had some of the packages needed by ARGUS installed, try updating them. Older version or irregular installations (e.g. mixing pip and conda) could possibly lead to problems. Perhaps you need to restart your computer afterwards.
-	Check whether you have installed curl. Just open your command line and type in ‘curl’. If it does not work, you might have to add curl to your environment variable PATH.

**Why does ARGUS not open on my Unix-based system (e.g. Mac)?**
-	Even though Python is meant to be compatible on most systems, there have been problems due to some (relative) paths, as Windows and Unix systems use slashes/backslashes differently. We are currently working on a Mac version that will be released soon.

**I get an error message stating that ‘ID invalid’ (or similar). What is the issue?**
-	Check whether you have chosen the correct delimiter and column names for your input file.

**One job is running for hours without scraping any data. What went wrong?**
-	Sometimes ARGUS encounters a website that causes the spider to malfunction. Then it is suggested to kill the job based on its ID that can be found on the Scrapy webpage.

