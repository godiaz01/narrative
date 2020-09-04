from bs4 import BeautifulSoup
import argparse
import json
import os

def scrape(args):

    log=open('log.csv','w')
    
    #iterate over articles in article file. open corresponding html, scrape text and add it to new JSON that will be written
    with open(args.articleListJSON) as f:
        
        articles = json.load(f)

        for a in articles:

            uri = a['uri']

            with open(os.path.join(args.htmlFolder,uri.split("/")[-1])) as html:

                soup = BeautifulSoup(html,"lxml")

                articleElement = soup.find("section",attrs={"name":"articleBody"})

                if not articleElement:
                    a['text']=None
                    print("Missing articleBody: "+uri)
                    continue

                articleSections = articleElement.find_all("div",attrs={"class":"StoryBodyCompanionColumn"})

                text=""

                for section in articleSections:

                    paragraphs = section.find_all("p")

                    for p in paragraphs:

                        span=""

                        for string in p.strings:
                            span+=string.replace("\n","").strip()+" "

                        text+=span.strip()+"\n\n"

                a['text']=text.strip()

            nytLength = str(a["word_count"])
            extractedLength = str(len(a["text"].split()))
            log.write(uri+','+nytLength+','+extractedLength+'\n')

        with open(args.outputFile,'w') as o:
            json.dump(articles,o,indent=4)

    log.close()
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NYT Article HTML text extractor based on Beautiful Soup 4")
    parser.add_argument('articleListJSON', type=str, help='File that contains list of NYT article metadata JSONs')
    parser.add_argument('htmlFolder', type=str, help='Folder to search for article html files')
    parser.add_argument('outputFile', type=str, help='Output file to create')
    args = parser.parse_args()

    scrape(args)

