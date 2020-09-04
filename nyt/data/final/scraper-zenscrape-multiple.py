import requests
import argparse
import json
import os
headers = {
  "apikey": "639d9ee0-e3cb-11ea-9438-3b53fce6d30e"
}

def scrape(args):

    for jsonFile in args.jsonList:

        print(f'Scraping {jsonFile}---------------------------------------------------------------------------------')
        
        folderName = os.path.join(args.outputFolder,jsonFile.replace(".json",''))
        if not os.path.isdir(folderName):
            os.mkdir(folderName)

        #open list of JSON files. for each article extract the url and save the response html based on the article title
        with open(jsonFile) as f:
            
            articles = json.load(f)

            for a in articles:

                title = "".join(x if x.isalnum() else "_" for x in a['headline']['main'])

                if os.path.isfile(os.path.join(folderName,title)):
                    print(f'Skipping {title}')
                    continue

                print(f'Requesting {title}')

                url = a['web_url']

                params = (
                   ("url",url),
                );

                response = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params);

                with open(os.path.join(folderName,title),'w') as o:
                    o.write(response.text)

        print('DONE ---------------------------------------------------------------------------------------------')
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NYT Article Scraper based on Zenscraper API")
    parser.add_argument('-o','--outputFolder' , type=str, help='Output folder to use or create')
    parser.add_argument('-l','--jsonList', nargs='+', help='List of article list JSON files', required=True)

    args = parser.parse_args()


    if (os.path.isdir(args.outputFolder) and not os.access(args.outputFolder,os.W_OK)) or (not os.access(os.getcwd(),os.W_OK)):
        print("Error: outputFolder can not be written to or created in the working directory")
        exit(0)
    elif not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)

    for fileName in args.jsonList:
        if not os.path.isfile(fileName):
            print("Error: One or more provided JSON files do not exist")
            exit(0)

    scrape(args)

