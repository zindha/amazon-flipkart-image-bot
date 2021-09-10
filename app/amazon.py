from selectorlib import Extractor
import requests
from fake_useragent import UserAgent
import random
import json
from time import sleep
import urllib.request


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('app/products.yml')

def scrape(url):
    ProxyList = []
    with open("app/proxy_list.txt") as Pl:
        i = 0
        while i<400:
            content = Pl.readline().split(' ')[0]
            content = content.split(':')
            ProxyList.append(content)
            i +=1

    RandomItem = random.randrange(0, 399)
    number = RandomItem

    IpAndPort = ProxyList[number]
    IP = IpAndPort[0]
    PORT = IpAndPort[1]

    print(IP)
    print(PORT)

    headers = {
        # 'dnt': '1',
        # 'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'sec-fetch-site': 'same-origin',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-user': '?1',
        # 'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        # 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    proxy = {str(IP):str(PORT)}
    r = requests.get(url, headers=headers, proxies=proxy)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

# product_data = []
with open("app/urls.txt",'r') as urllist, open('app/amazon_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            try:
                data['images'] = data['images'] .split('\":')[0].split('{"')[1]
                urllib.request.urlretrieve(data['images'])
        
            except:
                continue
            
            try:
                json.dump(data,outfile)
                outfile.write("\n")
                print("Done")
            except:
                continue