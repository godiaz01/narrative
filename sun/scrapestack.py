import requests
import argparse
import json
import os

KEY1= "57506b4cad773e8da266c2d9d5f8101d"
KEY2= "857c167c1c9581a70d7ef85113a5be1f"

MISSING={"all-of-me","crosstown-with-helen","essay-in-which-my-uncle-eddy-and-i-attend-his-funeral","father-junipero","hero-with-a-thousand-faces","locked-in-to-life","on-nuclear-war-survival-and-the-sun","people-land-and-community","perpetual-motion","sex-and-broadcasting","sporadic-e-or-how-to-spend-more-time-watching-television","the-art-of-dying","the-christ-of-the-double-wides","the-total-fm-guide","thick","this-i-believed","tomatoes-who-stole-the-taste","we-did","what-in-the-name-of-god","who-owns-the-west","why-cook","a-murder-remembered","and-so-on","anything-for-love","a-partial-inventory-of-the-great-mistakes-i-have-made","at-war-with-ourselves","auntie-barba","crip-zen","cut","hidden-clues","homeless-but-not-crazy","learning-to-sleep","making-waves","miracle-of-love","natural-birth-control-natural-birth","pity-the-man-who-doesnt-travel","poet-of-the-ordinary-issue-28","sally-manns-beautiful-and-treacherous-world","still-life-issue-453","sudan-journal","the-distance","the-fox","the-gull","the-odds-of-injury","this-season-s-people-excerpts-from-monday-night-class-caravan","three-tales-of-the-revolution","when-thieves-break-in"}
def scrape(args):

    apiCalls=0
    apiSucc=0
    
    #open list of JSON files. for each article extract the url and save the response html using the last section of uri
    with open(args.articleListJSON) as f:
        
        articles = json.load(f)

        for i in range(0,len(articles)):

            a = articles[i]

            url = a['url']

            if url.split("/")[-1] not in MISSING:
                continue

            params = {
            'access_key': KEY2,
            'url': url
            }

            print("Requesting... "+url)
            response = requests.get('http://api.scrapestack.com/scrape', params)
            apiCalls+=1

            rType = response.headers["content-type"]
            
            #check if response is an html page. if not, something went wrong
            if "text/html" not in rType:
                print("Error: "+response.text)
                continue

            print("Writing...")
            with open(os.path.join(args.outputFolder,url.split("/")[-1]),'w') as o:
                o.write(response.text)
            apiSucc+=1
    print("Finished")
    print(f'API Calls: {apiCalls}')
    print(f'API Successes: {apiSucc}')
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sun Article Scraper based on Scrapestack API")
    parser.add_argument('articleListJSON', type=str, help='File that contains list of article metadata JSONs')
    parser.add_argument('outputFolder', type=str, help='Output folder to use or create')
    args = parser.parse_args()

    if (os.path.isdir(args.outputFolder) and not os.access(args.outputFolder,os.W_OK)) or (not os.access(os.getcwd(),os.W_OK)):
        print("Error: outputFolder can not be written to or created in the working directory")
        exit(0)
    elif not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)

    scrape(args)

