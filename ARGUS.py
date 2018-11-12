####### GUI for ARGUS #######

### The GUI provides the possibility to change the settings for scraping without having to change the txt-file manually, as well as an easier way of initiating the program.
### runs on Python 3.6
### author: Sebastian Schmidt




import os
import sys
from tkinter import filedialog
import tkinter.messagebox
import tkinter as tk
import pandas as pd
import time



global show_filename
show_filename = "Select file"
columns = [None]
delimiter = [None]


clear = lambda: os.system('cls')
clear()

print("""
##################################################
#    _______  ______  ______ _     _ _______     #
#    |_____| |_____/ |  ____ |     | |____       #
#    |     | |    \_ |_____| |_____| ______|     #
#                                                #
# Automated Robot for Generic Universal Scraping #
#                                                #
################################################## 

             >>Jan Kinne - 2018<< 
 
Browse for text file containing your URLs...""")




# create master window to change settings
master = tk.Tk()
master.title("ARGUS")
master.iconbitmap(r'.\misc\ARGUS.ico')



##### FILE SELECT #####

tk.Label(master, text="File Settings", font=("Calibri", 16)).grid(row=0, column=0, sticky=tk.N)


# List name
tkvar1 = tk.StringVar(master)
tkvar1.set("Browse for URL list")
tk.Label(master, textvariable=tkvar1, font=("Calibri", 12)).grid(row=1, column=0, sticky=tk.W + tk.E)


# URL list
e1 = tk.Entry(master)

def select_file(*args):
    filename = filedialog.askopenfilename()
    e1.delete(0, 'end')
    e1.insert (tk.END, filename)
    show_filename = filename.split("/")[-1] 
    tkvar1.set(show_filename)

def change_filename(*args):
    tkvar1.get()
    print("{} selected.\n\nPlease define delimiter and encoding and >>Load Columns<<".format(tkvar1.get()))

tk.Button(master, text="Browse", command=select_file, font=("Calibri", 12)).grid(row=2, column=0, sticky=tk.W + tk.E)
tkvar1.trace("w", change_filename)


# Delimiter
e2 = tk.Entry(master)
tkvar2 = tk.StringVar(master)
delimiters = ["Tab", "Whitespace", "Semicolon", "Comma"]
tkvar2.set("Select") # set the default option
tk.Label(master, text="Delimiter:", font=("Calibri", 12)).grid(row=3, column=0, sticky=tk.W)
popupMenu = tk.OptionMenu(master, tkvar2, *delimiters)
popupMenu.grid(row=3, column=0, sticky=tk.E)
popupMenu.config(font=("Calibri", 12))

def change_dropdown2(*args):
    delimiters_external = ["Tab", "Whitespace", "Semicolon", "Comma"]
    delimiters_internal = ["\\t", " ", ";", ","]
    global delimiter
    delimiter = delimiters_internal[delimiters_external.index(tkvar2.get())]
    e2.delete(0, 'end')
    e2.insert (tk.END, delimiter)

tkvar2.trace('w', change_dropdown2)


# Encoding
e3 = tk.Entry(master)
tkvar3 = tk.StringVar(master)
encodings = ["UTF-8", "Latin-1"]
tkvar3.set("Select") # set the default option
tk.Label(master, text="Encoding:", font=("Calibri", 12)).grid(row=4, column=0, sticky=tk.W)
popupMenu = tk.OptionMenu(master, tkvar3, *encodings)
popupMenu.grid(row=4, column=0, sticky=tk.E)
popupMenu.config(font=("Calibri", 12))

read_file = False
def change_dropdown3(*args):
    encodings_external = ["UTF-8", "Latin-1"]
    encodings_internal = ["utf-8", "latin-1"]
    encoding = encodings_internal[encodings_external.index(tkvar3.get())]
    e3.delete(0, 'end')
    e3.insert (tk.END, encoding)

tkvar3.trace('w', change_dropdown3)


# ID
e4 = tk.Entry(master)

tkvar4 = tk.StringVar(master)
tkvar4.set("Select") # set the default option
tk.Label(master, text="ID Column:", font=("Calibri", 12)).grid(row=6, column=0, sticky=tk.W)
popupMenu4 = tk.OptionMenu(master, tkvar4, *columns)
popupMenu4.grid(row=6, column=0, sticky=tk.E)
popupMenu4.config(font=("Calibri", 12))


# URL
e5 = tk.Entry(master)

tkvar5 = tk.StringVar(master)
tkvar5.set("Select") # set the default option
tk.Label(master, text="URL Column:", font=("Calibri", 12)).grid(row=7, column=0, sticky=tk.W)
popupMenu5 = tk.OptionMenu(master, tkvar5, *columns)
popupMenu5.grid(row=7, column=0, sticky=tk.E)
popupMenu5.config(font=("Calibri", 12))


# Load URL list
def change_dropdown45(*args):
    e5.delete(0, 'end')
    column = tkvar5.get()
    e5.insert (tk.END, column)
    e4.delete(0, 'end')
    column = tkvar4.get()
    e4.insert (tk.END, column)

def refresh_dropdown45(*args):
    global columns
    try:
        columns = pd.read_csv(e1.get(), sep=delimiter, nrows=1, encoding=e3.get(), engine="python").columns.values
        popupMenu4 = tk.OptionMenu(master, tkvar4, *columns)
        popupMenu4.grid(row=6, column=0, sticky=tk.E)
        popupMenu4.config(font=("Calibri", 12))
        popupMenu5 = tk.OptionMenu(master, tkvar5, *columns)
        popupMenu5.grid(row=7, column=0, sticky=tk.E)
        popupMenu5.config(font=("Calibri", 12))
        print("\nColumns loaded:")
        print("\n".join(columns))
        print("\nSelect columns and >>Web Scraper Settings<<")
    except:
        print("URL list could not be loaded.\nPlease browse for your file and select correct delimiter and encoding.")


tkvar4.trace('w', change_dropdown45)
tkvar5.trace('w', change_dropdown45)


tk.Button(master, text='Load Columns', command=refresh_dropdown45, font=("Calibri", 12)).grid(row=5, column=0, sticky=tk.W + tk.E)




##### Spider Settings #####

tk.Label(master, text="Web Scraper Settings", font=("Calibri", 16)).grid(row=0, column=1, sticky=tk.N)

# Cores
tk.Label(master, text="Parallel Processes:", font=("Calibri", 12)).grid(row=2, column=1, sticky=tk.W)

e6 = tk.Entry(master)

tkvar6 = tk.StringVar(master)
tkvar6.set("Select") # set the default option
cpu_cores = range(1, os.cpu_count()+1)
popupMenu6 = tk.OptionMenu(master, tkvar6, *cpu_cores)
popupMenu6.grid(row=2, column=1, sticky=tk.E)
popupMenu6.config(font=("Calibri", 12))

def change_dropdown6(*args):
    e6.delete(0, 'end')
    column = tkvar6.get()
    e6.insert (tk.END, column)

tkvar6.trace('w', change_dropdown6)


# Spider
tk.Label(master, text="Spider Type:", font=("Calibri", 12)).grid(row=3, column=1, sticky=tk.W)

e7 = tk.Entry(master)

tkvar7 = tk.StringVar(master)
tkvar7.set("Select") # set the default option
spiders = ["text", "link"]
popupMenu7 = tk.OptionMenu(master, tkvar7, *spiders)
popupMenu7.grid(row=3, column=1, sticky=tk.E)
popupMenu7.config(font=("Calibri", 12))

def change_dropdown7(*args):
    e7.delete(0, 'end')
    column = tkvar7.get()
    e7.insert (tk.END, column)

tkvar7.trace('w', change_dropdown7)


# Limit
tk.Label(master, text="Scrape Limit:", font=("Calibri", 12)).grid(row=4, column=1, sticky=tk.W)

e8 = tk.Spinbox(master, from_=0, to=9999, validate="key", width=9, font=("Calibri", 12))
e8.grid(row=4, column=1, sticky=tk.N + tk.E)



# Short URLs
tk.Label(master, text="Prefer Short URLs:", font=("Calibri", 12)).grid(row=5, column=1, sticky=tk.W)

e9 = tk.Entry(master)

tkvar9 = tk.StringVar(master)
tkvar9.set("Select") # set the default option
preferences = ["on", "off"]
popupMenu9 = tk.OptionMenu(master, tkvar9, *preferences)
popupMenu9.grid(row=5, column=1, stick=tk.E)
popupMenu9.config(font=("Calibri", 12))

def change_dropdown9(*args):
    e9.delete(0, 'end')
    preference = tkvar9.get()
    e9.insert (tk.END, preference)

tkvar9.trace('w', change_dropdown9)


# Language

tk.Label(master, text="Preferred Language:", font=("Calibri", 12)).grid(row=6, column=1, sticky=tk.W)

e10 = tk.Entry(master)

tkvar10 = tk.StringVar(master)
tkvar10.set("Select")

languages = pd.read_csv(r".\misc\ISO_language_codes.txt", sep="\t", encoding="utf-8", engine="python")
languages = languages["language"].values.tolist()
languages = ["None"] + languages

popupMenu10 = tk.OptionMenu(master, tkvar10, *languages)
popupMenu10.grid(row=6, column=1, sticky=tk.E)
popupMenu10.config(font=("Calibri", 12))

def change_dropdown10(*args):
    e10.delete(0, 'end')
    preference = tkvar10.get()
    e10.insert (tk.END, preference)

tkvar10.trace('w', change_dropdown10)


# LOG level
tk.Label(master, text="Logging Level:", font=("Calibri", 12)).grid(row=7, column=1, sticky=tk.W)

e11 = tk.Entry(master)
e11.insert(tk.END,"INFO")

tkvar11 = tk.StringVar(master)
tkvar11.set("INFO") # set the default option
log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
popupMenu11 = tk.OptionMenu(master, tkvar11, *log_levels)
popupMenu11.grid(row=7, column=1, sticky=tk.E)
popupMenu11.config(font=("Calibri", 12))

def change_dropdown11(*args):
    e11.delete(0, 'end')
    level = tkvar11.get()
    e11.insert (tk.END, level)

tkvar11.trace('w', change_dropdown11)


##### Start Scraping #####

# save entries in settings file
settings_file = """
[input-data]
filepath = {}
delimiter = {}
encoding = {}
ID = {}
url = {}

[system]
n_cores = {}

[spider-settings]
spider = {}
limit = {}
prefer_short_urls = {}
language = {}
log_level = {}
"""

scrapyd_file = """
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   = items
jobs_to_keep = 500
dbs_dir     = dbs
max_proc    = {}
max_proc_per_cpu = 4
finished_to_keep = 500
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher
poll_interval = 0.1

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
"""


from bin import start_crawl

# start scraping process
def start_scraping():
    print("Writing settings file...")
    settings_txt = open(r".\bin\settings.txt", "w", encoding="utf-8")
    settings_txt.truncate()
    settings_txt.write(settings_file.format(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get(), e11.get()))
    settings_txt.close()
    scrapyd_txt = open(r"scrapyd.conf", "w", encoding="utf-8")
    scrapyd_txt.truncate()
    scrapyd_txt.write(scrapyd_file.format(e6.get()))
    scrapyd_txt.close()
    print("Starting server in separate windows...")
    time.sleep(2)
    os.startfile(r".\bin\start_server.bat")
    time.sleep(2)
    start_crawl.start_crawl()
    print("Web scraping started. Do not close server window.")

tk.Button(master, text='Start Scraping', command=start_scraping, font=("Calibri bold", 12)).grid(row=18, column=0, columnspan = 2, sticky=tk.W + tk.E)


##### Functions #####

tk.Label(master, text="Functions", font=("Calibri", 16)).grid(row=19, column=0, sticky=tk.N)


# stop scraping
from bin import kill_all_jobs
import subprocess

def stop_scraping():
    result = tk.messagebox.askyesno("WARNING", "Do you want to stop all running and scheduled scraping jobs?")
    if result == True:
        kill_all_jobs.kill_all()
        print("All scraping jobs terminated.")
        result2 = tk.messagebox.askyesno("WARNING", "Scraping jobs stopped. Do you want to delete already scraped data?")
        if result2 == True:
            kill_all_jobs.delete_leftovers(os.getcwd())
        subprocess.run(r"TSKILL scrapyd")

tk.Button(master, text='Stop Scraping', command=stop_scraping, font=("Calibri", 12)).grid(row=21, column=0, sticky=tk.W + tk.E)



# stop single job
from tkinter import simpledialog


def kill_job(job_id=None):
    subprocess.run(r"curl http://localhost:6800/cancel.json -d project=ARGUS -d job={}".format(job_id))

# sub class for asking job id
class StringDialog(simpledialog._QueryString):
    def body(self, master):
        super().body(master)
        self.iconbitmap(r'.\misc\ARGUS.ico')

    def ask_string(title, prompt, **kargs):
        d = StringDialog(title, prompt, **kargs)
        return d.result

def get_job_id():
    job_id = StringDialog.ask_string("Terminate Job", "Enter job you want to terminate:")
    kill_job(job_id)

tk.Button(master, text='Terminate Job', command=get_job_id, font=("Calibri", 12)).grid(row=22, column=0, sticky=tk.W + tk.E)


# postprocessing
from bin import postprocessing
import configparser

def start_postprocessing():
    config = configparser.RawConfigParser()
    config.read(r".\bin\settings.txt")
    if config.get('spider-settings', 'spider') == "text":
        fn = config.get('input-data', 'filepath').split(".")[0] + "_scraped_texts.csv"
        exists = os.path.isfile(fn)
    elif config.get('spider-settings', 'spider') == "link":
        fn = config.get('input-data', 'filepath').split(".")[0] + "_scraped_links.csv"
        exists = os.path.isfile(fn)
    if exists == True:
        overwrite = tk.messagebox.askyesno("WARNING", "Postprocessing will overwrite file {}!\nContinue?".format(fn))
        if overwrite == False:
            return
        else:
            subprocess.run(r"TSKILL scrapyd")
            postprocessing.postprocessing(os.getcwd())
            return
    result = tk.messagebox.askyesno("WARNING", "Do you want to start postprocessing procedure?")
    if result == True:
        subprocess.run(r"TSKILL scrapyd")
        postprocessing.postprocessing(os.getcwd())

tk.Button(master, text='Postprocessing', command=start_postprocessing, font=("Calibri", 12)).grid(row=21, column=1, sticky=tk.W + tk.E)


# aggregate webpage texts
from bin import aggregator


def start_aggregator(*args):
    filepath = filedialog.askopenfilename()
    if os.path.isfile(filepath.split("\\")[0].split(".")[0] + "_aggregated.csv"):
        overwrite = tk.messagebox.askyesno("WARNING", "Aggregating will overwrite file {}!\nContinue?".format(filepath.split("\\")[0].split(".")[0] + "_aggregated.csv"))
        if overwrite == False:
            return
    print("Starting to aggregate webpage texts to website level...")
    output = aggregator.aggregate_webpages(filepath)
    print("Aggregated webpage texts to:\n{}".format(output))



tk.Button(master, text='Aggregate Webpage Texts', command=start_aggregator, font=("Calibri", 12)).grid(row=22, column=1, sticky=tk.W + tk.E)










# initiate post-processing to produce csv-file
def post_process():
	os.startfile("postprocessing.bat")



##### Functions #####

tk.Label(master, text="Functions", font=("Calibri", 16)).grid(row=19, column=0, sticky=tk.N)



# create buttons for functions


#tk.Button(master, text='Kill all jobs', command=kill_all, font=("Calibri", 12)).grid(row=18, column=1, sticky=tk.W + tk.E)
master.grid_columnconfigure(0, minsize=250)
master.grid_columnconfigure(1, minsize=250)
master.mainloop()