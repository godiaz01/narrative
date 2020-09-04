from bs4 import BeautifulSoup
import argparse
import json
import os

BASE_URL = "https://www.thesunmagazine.org"

def scrape(args):

    files = os.listdir(args.htmlFolder)

    sortedFiles = sorted(files,key=lambda file: int(file.replace('.html','')))
    print(sortedFiles)

    corpus = []

    for f in sortedFiles:

        with open(os.path.join(args.htmlFolder,f)) as html:

            soup = BeautifulSoup(html,"lxml")

            articleDiv = soup.find("div",attrs={"class":"list-content list-content-border"})

            articleList = articleDiv.find_all("article")

            for article in articleList:

                title = article.find("h3",attrs={"block-content-title"}).text.strip()
                subtitle = article.find("p",attrs={"block-content-subtitle"}).text.strip()
                excerpt = article.find("div",attrs={"block-content-excerpt"}).text.strip()
                url = BASE_URL+article.find("h3",attrs={"block-content-title"}).find("a")['href']
                metadata = article.find("ul",attrs={"block-content-meta"}).find_all("li")
                if len(metadata)==2:
                    author  = metadata[0].text.replace("By ","").strip()
                    issue  = metadata[1].text.strip()
                elif len(metadata)==1:
                    author  = ''
                    issue  = metadata[0].text.strip()

                articleObj = {
                    "title": title,
                    "subtitle": subtitle,
                    "excerpt": excerpt,
                    "url": url,
                    "author": author,
                    "issue": issue
                }

                if not title or not excerpt or not url or not metadata or not author or not issue:
                    print("Missing:")
                    print(articleObj)
                    

                corpus.append(articleObj)

    with open(args.outputFile,'w') as o:
        json.dump(corpus,o,indent=4)
   

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sun pages HTML text extractor based on Beautiful Soup 4")
    #parser.add_argument('articleListJSON', type=str, help='File that contains list of NYT article metadata JSONs')
    parser.add_argument('htmlFolder', type=str, help='Folder to search for pages html files')
    parser.add_argument('outputFile', type=str, help='Output file to create')
    args = parser.parse_args()

    scrape(args)

