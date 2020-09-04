import requests
import json
import os
import argparse

def scrape(args):

    apiCalls=0
    apiSucc=0
    
    #open list of JSON files. for each article extract the url and save the response html using the last section of uri
    with open(args.articleListJSON) as f:
        
        articles = json.load(f)

        for a in articles:

            if apiCalls==1000:
                break

            print('URL: '+a['url'])
            response = requests.get(
                url="https://app.scrapingbee.com/api/v1/",
                params={
                    "api_key": "1FBZFQL9P8TUA2UMRTBS5LEEIG95FMHAQ0WIZNQZX12C4J1WTM6EAJORVRT2RJKP6B236WF2KLG7FOYY",
                    "url": a['url']
                }
            )
            apiCalls+=1

            rType = response.headers["content-type"]
            
            #check if response is an html page. if not, something went wrong
            if "text/html" not in rType:
                print("Error: "+response.text)
                continue

            with open(os.path.join(args.outputFolder,a['url'].split("/")[-1]),'w') as o:
                o.write(response.text)
            apiSucc+=1

    print("Finished")
    print(f'API Calls: {apiCalls}')
    print(f'API Successes: {apiSucc}')
        


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sun Mag Article Scraper based on ScarpingBee API")
    parser.add_argument('articleListJSON', type=str, help='File that contains list of article metadata JSONs')
    parser.add_argument('outputFolder', type=str, help='Output folder to use or create')
    args = parser.parse_args()

    if (os.path.isdir(args.outputFolder) and not os.access(args.outputFolder,os.W_OK)) or (not os.access(os.getcwd(),os.W_OK)):
        print("Error: outputFolder can not be written to or created in the working directory")
        exit(0)
    elif not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)

    scrape(args)