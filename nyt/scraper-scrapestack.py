import requests
import argparse
import json
import os

def scrape(args):

    apiCalls=0
    apiSucc=0
    
    #open list of JSON files. for each article extract the url and save the response html using the last section of uri
    with open(args.articleListJSON) as f:
        
        articles = json.load(f)

        for a in articles:

            url = a['web_url']

            params = {
            'access_key': '57506b4cad773e8da266c2d9d5f8101d',
            'url': url
            }

            uri = a["uri"]

            print("Requesting... "+url)
            response = requests.get('http://api.scrapestack.com/scrape', params)
            apiCalls+=1

            rType = response.headers["content-type"]
            
            #check if response is an html page. if not, something went wrong
            if "text/html" not in rType:
                print("Error: "+response.text)
                continue

            print("Writing...")
            with open(os.path.join(args.outputFolder,uri.split("/")[-1]),'w') as o:
                o.write(response.text)
            apiSucc+=1
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NYT Article Scraper based on Scrapestack API")
    parser.add_argument('articleListJSON', type=str, help='File that contains list of NYT article metadata JSONs')
    parser.add_argument('outputFolder', type=str, help='Output folder to use or create')
    args = parser.parse_args()

    if (os.path.isdir(args.outputFolder) and not os.access(args.outputFolder,os.W_OK)) or (not os.access(os.getcwd(),os.W_OK)):
        print("Error: outputFolder can not be written to or created in the working directory")
        exit(0)
    elif not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)

    scrape(args)

