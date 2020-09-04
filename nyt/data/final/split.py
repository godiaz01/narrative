import requests
import argparse
import json
import os
import random
import math
headers = {
  "apikey": "639d9ee0-e3cb-11ea-9438-3b53fce6d30e"
}
SIZE = 50
SEED = 86903

def split(args):

    data = [(f.replace('-filtered', ''), json.load(open(f))) for f in args.jsonList]
    total = sum([len(d[1]) for d in data])
    print(f"Initial size of {total}; Expect {math.ceil(total/SIZE)} splits of size {SIZE}")
    c = 1
    stop = False
    while not stop:
        split = []
        csv = [['Column','Title','HTML','Class']]
        size = 0
        while size < 50 and not stop:
            for (column, corpus) in data:
                n = len(corpus)
                if n > 0:
                    ri = random.randrange(n)
                    article = corpus.pop(ri)
                    split.append(article)
                    title = article['headline']['main']
                    html = "".join(x if x.isalnum() else "_" for x in title)
                    csv.append([column, title, html, '?'])
                    size += 1
                if size == 50:
                    break
                total = sum([len(d[1]) for d in data])
                if total == 0:
                    stop = True
                    break
        print(f"Writing split {c}")
        with open(os.path.join(args.outputFolder, f"split-{c}.json"), 'w') as o:
            json.dump(split, o, indent=4)
        with open(os.path.join(args.outputFolder, f"split-{c}.csv"), 'w') as o:
            for entry in csv:
                line = ",".join(entry)
                o.write(line+'\n')
        c += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Splitter")
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

    random.seed(SEED)

    split(args)
