# ARGUS

ARGUS is an easy-to-use web mining tool. The program is based on the Scrapy Python framework and is able to crawl a broad range of different websites. On the websites, ARGUS is able to perform tasks like scraping texts or collecting hyperlinks between websites.


## Getting Started

These instructions will get you a copy of ARGUS up and running on your local machine.

Follow these 10 easy steps, which are described in more detail below, to make a successfull ARGUS scraping run:
1.  Install Python 3.6
2.  Install additional Python packages.
3.  Install cURL and add a cURL environment variable to your system.
4.  Download and extract the ARGUS files.
5.  Prepare the settings.txt and your list of website URLs.
6.  Run the scrapyd server by double-clicking on "start_server.bat"
7.  Start your scraping run by double-clicking on "start_scraping.bat"
8.  Check your scraping run using the web interface.
9.  Wait until all jobs have finished.
10. Run the "postprocessing.bat" and check out the results which were saved to the same directory your initial list of website URLs are located in.

### Prerequisites

ARGUS works with Python 3.6, is based on the Scrapy framework and has the following Python package dependencies:

*	Scrapy 1.5.0
*	scrapyd 1.2.0
*	scrapyd-client 1.1.0
*	scrapy-fake-useragent 1.1.0
*	tldextract 2.2.0
*	pandas 0.22.0

Additionally, you need [cURL](https://curl.haxx.se/download.html) to communicate with the ARGUS user interface. An executable Windows 64bit version of cURL can be downloaded [here](https://dl.uxnr.de/build/curl/curl_winssl_msys2_mingw64_stc/curl-7.59.0/curl-7.59.0.zip), for example.
After downloading and extracting, you need to add a cURL environment variable to your system. See [this Stackoverlow thread](https://stackoverflow.com/questions/9507353/how-do-i-install-set-up-and-use-curl-on-windows) if you do not know how to do that.

### Installing

If you are not using Python yet, the easiest way to install Python 3.6 and most of its crucial packages is to use the [Anaconda Distribution](https://www.anaconda.com/download/).
After installing Anaconda, you can use pip to install the packages above by typing “pip install package_name” (e.g., “pip install scrapy”) into your system command prompt. 


## Using ARGUS

If you are interested in how ARGUS processes websites, read the following description of its workflow. Otherwise, you may continue with the next section.

An ARGUS crawl is based on a list of user given firm website addresses (URL) and proceeds as follows:
1.	The first webpage (a website’s main page) is requested using the first address in the given URL list.
2.	A collector item is instantiated, which is used to collect the website’s text, meta-data (e.g. timestamps, number of scraped URLs etc.), and a so called URL stack.
3.	The main page is processed:
    -	Text on the main page is extracted and stored in the collector item.
    -	URLs which refer to subpages of the same website (i.e. domain) are extracted and stored in the collector item’s URL stack.
4.	The algorithm continues to request subpages of the website using URLs from the URL stack. Hereby, it uses a simple heuristic which gives higher priority short URLs and those which refer to subpages in a predefined language.
    -	Texts and URLs are collected from the subpage and stored in the collector item.
    -	The next URL in the URL stack is processed.
5.	The algorithm stops to process a domain when all subpages were processed or as soon as a predefined number of subpages per domain has been processed.
6.	The collected texts are processed (i.e. cleaned) and written to an output file.
7.	The next website is processed by requesting the next URL from the user given URL list. The described process continues until all firm website addresses from the user given list were processed.

### Spider types

Currently, ARGUS comes with two types of spiders: textspiders and linkspiders.
*   **textspider** - these spiders extract texts from websites you give to them.
*   **linkspider** - these spiders extract hyperlinks between websites you give to them. They also collect hyperlinks to websites "out-of-sample", but not between out-of-sample websites and from out-of-sample websites to within-sample websites.

### The settings file

The first thing you have to do when performing an ARGUS crawl is to prepare the “settings.txt” which is located in the ARGUS root directory. In the settings file, the following parameters need to be set:

*	[input-data]
    -	**filepath** – the full path to your text file with website addresses. The file should be delimiter-separated and without BOM (byte order mark). An easy way to see whether your text file uses BOM is to use [Notepad++](https://notepad-plus-plus.org/) and check the “Encoding” in the top panel. The URLs need to be in the format “www.example.com”. The directory of your URL list will also be used to output the scraped data. An example website address can be found in /misc:
    ![example url list](https://github.com/datawizard1337/ARGUS/blob/linkspider/misc/pics/url_list.PNG?raw=true)
    -	**delimiter** – the type of delimiter your text file uses. It is recommended to use tab-delimited text files: \t
    -	**encoding** – the encoding of your text file. It is recommended to use text files in: 
utf-8
    -	**ID** – the field name of your unique website identifier in your website address file.
    -	**url** – the field name of your web addresses in your website address file.
*	[system]
    -	**n_cores** – the number of processor cores you want to dedicate to the ARGUS scraping process. It is recommended to use the total number of cores in your system -1 (i.e. if you have a quad-core processor with 4 cores, you should choose “n_cores = 3”).
*	[spider-settings]
    -   **spider** - select either *text* or *link* to use textspiders or linkspiders to process your websites.
    -	**limit** – the maximum number of subpages (incl. the main/starting page) that will be scraped per domain. Set this to 0 if you want to scrape entire websites (caution is advised as there are websites with ten-thousands of subpages).
    -	**prefer_short_urls** – whether you want ARGUS to prefer downloading the shortest hyperlinks it finds on a website first. ARGUS usually starts at the website’s main page and there it collects all hyperlinks directing to the website’s subpages. After processing the website’s main page, ARGUS follows the found hyperlinks to do the same to website’s subpages until it reached the set **limit**. If **prefer_short_urls** is set to “on”, ARGUS will first visit those subpages with the shortest URLs. The reasoning behind that is that one can assume that the most general (and arguably most important) information is located at the website’s top level webpages (e.g., www.example.com/products). If you want to turn this simple selection heuristic off, choose: off
    -	**language** – the language that will be preferred when selecting the next subpage URL (analogous to **prefer_short_urls**). Note that this simple heuristic just checks the URL for certain [ISO language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). You need to insert the ISO language name as you find it in the “ISO_language_code.txt” in the ARGUS\misc sub directory. So if you want to prefer German language URLs, you would enter: German. If you do not want to use this heuristic, just enter: None.
    -	**log** – the amount of information that is stored in log files. The available options are DEBUG, INFO, WARNING, ERROR, and CRITITCAL. For larger scraping runs, the log level should be set to: INFO.


### Starting a scraping run

Before starting your scraping run, a [scrapyd](http://scrapyd.readthedocs.io/en/stable/overview.html#how-scrapyd-works) server, which handles your scraping jobs, needs to be started. This can be done by running the “start_server.bat”, which opens a separate window that should not be closed during the whole upcoming scraping run. After the server has started, the scraping process can be launched by executing “start_scraping.bat”. This little program will split your list of URLs into handy chunks and starts a separate job for each chunk to speed up the scraping process. The splitting and job scheduling may take a short while. After all jobs were scheduled, the scrapyd web interface will open up in your default web browser (you can also get there by typing “http://127.0.0.1:6800/” into your web browser).
![scrapyd server](https://github.com/datawizard1337/ARGUS/blob/master/misc/pics/scrapyd_server.png?raw=true)

You can safely ignore the lower part about how to schedule a spider, because ARGUS did that for you already. To see the jobs which have been scheduled, click the “Jobs” link. There you will find an overview about the pending, running, and finished jobs. You can also see the time a job was started, its current runtime, and the time it was finished. By clicking on a job’s log link, you can have a look at its log file. The number of running jobs should be equal to the **n_cores** parameter you set in the “settings.txt”.

### Stopping jobs

Sometimes certain jobs stop working or never finish, so you may want to stop and restart them. This can be done by running the “kill_single_job.bat”. You will be asked for the id of the job you want to cancel. The id is a long hash number which can be found in the “Job” column in the “Jobs” web interface section.
![scrapyd jobs](https://github.com/datawizard1337/ARGUS/blob/master/misc/pics/scrapyd_jobs.png?raw=true)

You can stop all processes at once by running the “kill_all_jobs.bat”. This little program will tell the scrapyd server to stop all running and scheduled processes. You will be asked whether you want to delete the data already scraped. If you decide against deleting the scraped data, you may want to run the “postprocessing.bat” as described below.

### Postprocessing

When all jobs are finished, you may close the scrapyd server window to stop the server. Finally, you need to run “postprocessing.bat” which cleans up and writes your scraped data to the directory of your input data.


## Output data

The output file can be found in the same directory your original website address file is located (**filepath** parameter in the settings file). One row equals one webpage and n (n ≤ **limit**) webpages equal one website (identified by its ID). 


### Textspider output

![ARGUS textspider output](https://github.com/datawizard1337/ARGUS/blob/master/misc/pics/ARGUS_textspider.png?raw=true)
*	**ID** – the ID of the website as given in [input-data] section of the settings file.
*	**dl_rank** – the chronological order the webpage was downloaded. The main page of a website (i.e. the URL in your website address file) has rank 0, the first subpage processed after the main page has rank 1, and so on.
*	**dl_slot** – the domain name of the website as found in the user given website address list.
*	**error** – not “None” if there was an error requesting the website’s main page. Can be an HTML error (e.g., “404”), DNS lookup error, or a timeout.
*	**redirect** – is “True” if there was a redirect to another domain when requesting the first webpage from a website. This may indicate that ARGUS scraped a different website than intended. However, it may also be a less severe redirect like “www.example.de” to “www.example.com”. It is your responsibility to deal with redirects.
*	**start_page** – gives you the first webpage that was scraped from this website. Usually, this should be the URL given in your website address file.
*	**text** – the text that was downloaded from the webpage.
*	**timestamp** – the exact time when the webpage was downloaded.
*	**url** – the URL of the webpage.

### Linkspider output

![ARGUS linkspider output](https://github.com/datawizard1337/ARGUS/blob/master/misc/pics/ARGUS_linkspider.png?raw=true)
*	**ID** – the ID of the website as given in [input-data] section of the settings file.
*	**alias** – if there was an initial redirect (e.g. from www.example.de to www.example.com), the domain the spider got redirected to ("example.com" in the example) becomes the websites alias. ~~During postprocessing, hyperlinks are harmonised by transferring alias domains to their associated (*dl_slot*) domains.~~
*	**dl_slot** – the domain name of the website as found in the user given website address list.
*	**error** – not “None” if there was an error requesting the website’s main page. Can be an HTML error (e.g., “404”), DNS lookup error, or a timeout.
*	**links_internal** – the domains of "within-sample" websites found on the focal website. The first element is the focal website itself (this format makes it easiert to import the data as an "adjacency list" into analysis software). Field is empty if no hyperlinks to within-sample websites were found.
*	**links_external** – the domains of "within-sample" and "out-of-sample" websites found on the focal website. The first element is the focal website itself (this format makes it easiert to import the data as an "adjacency list" into analysis software). Field is empty if no hyperlinks were found.
*	**redirect** – is “True” if there was a redirect to another domain when requesting the first webpage from a website. This may indicate that ARGUS scraped a different website than intended. However, it may also be a less severe redirect like “www.example.de” to “www.example.com”. It is your responsibility to deal with redirects.
*	**timestamp** – the exact time when the webpage was downloaded.
*	**url** – the URL of the webpage.

## Why ARGUS?

**ARGUS** stands for "**A**utomated **R**obot for **G**eneric **U**niversal **S**craping".
