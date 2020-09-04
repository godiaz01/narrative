import requests
import argparse
import json
import os
headers = {
  "apikey": "9f317bc0-be27-11ea-a28c-298c4765c5b4"
}

def scrape(args):

    for page in range(1,204+1):

        url = f'https://www.thesunmagazine.org/sections/essays-memoirs-true-stories/page/{page}'

        params = (
           ("url",url),
        );

        response = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params);

        rType = response.headers["content-type"]
            
        #check if response is an html page. if not, something went wrong
        if "text/html" not in rType:
            print("Error: "+response.text)
            continue

        writePath = os.path.join(args.outputFolder,url.replace('https://','').split('/')[-1]+'.html')
        print(writePath)
        with open(writePath,'w') as o:
            o.write(response.text)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sun Mag Article Scraper based on Zenscraper API")
    #parser.add_argument('articleListJSON', type=str, help='File that contains list of NYT article metadata JSONs')
    parser.add_argument('outputFolder', type=str, help='Output folder to use or create')
    args = parser.parse_args()

    if (os.path.isdir(args.outputFolder) and not os.access(args.outputFolder,os.W_OK)) or (not os.access(os.getcwd(),os.W_OK)):
        print("Error: outputFolder can not be written to or created in the working directory")
        exit(0)
    elif not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)

    scrape(args)

