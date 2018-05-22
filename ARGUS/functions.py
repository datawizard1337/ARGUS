import pandas as pd



#loads urls and IDs from text file
def ImportURLs(filename):
    data = pd.read_csv(filename, delimiter="\t", encoding="utf-8", error_bad_lines=False)
    allowed_domains = [url.split("www.")[-1].lower() for url in list(data["webadresse"])]
    start_urls = ["http://" + url.lower() for url in allowed_domains]
    IDs = [ID for ID in list(data["crefo"])]
    return allowed_domains, start_urls, IDs