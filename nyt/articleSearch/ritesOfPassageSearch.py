# Demo code sample. Not indended for production use.

# See instructions for installing Requests module for Python
# http://docs.python-requests.org/en/master/user/install/

import requests
import json
import time
from datetime import timedelta
OUTPUTFILE = 'rites-of-passage'
KICKER = '%22Rites%20Of%20Passage%22'

apiKey = '5eA3yPtQOAOlTBaMbK1BCbfPLk0GDZU8'
validPages=range(200+1)


def writeData(name, data):
    with open(name, 'w') as f:
        json.dump(data, f)

def execute():

    totalStored = 0
    data = []
    apiRequests = 0
    start = time.time()
    queryHits = None
    querySeen = 0

    for page in validPages:

        time.sleep(6)

        # we differentiate between the number of hits specific to the query, and the humber of hits specific to the current page of the query
        url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=kicker.contains%3A({KICKER})&page={page}&api-key={apiKey}'
        reqHeaders = {"Accept": "application/json"}

        print('Request: '+url)

        r = requests.get(url, headers=reqHeaders)
        rj = json.loads(r.text)
        apiRequests += 1

        if 'response' in rj and 'docs' in rj['response']:

            print("Page: "+str(page))
            print("Total API Requests: "+str(apiRequests))

            if not queryHits:
                queryHits = rj['response']['meta']['hits']
                print('Query Hits: '+str(queryHits))
            if queryHits==0:
                print("No Hits. Skipping to next query")
                break

            articles = rj['response']['docs']
            data += articles

            pageHits = len(articles)
            print('Page Hits: '+str(pageHits))

            querySeen += pageHits
            totalStored += pageHits
            print("Total Stored: "+str(totalStored))
            #if we already saw as many hits as those returned by the query, there is no point in moving to the next pages (they will be empty)
            if querySeen>=queryHits:
                print("Net Query Hits: "+str(queryHits))
                print("Seen documents with current query: "+str(querySeen))
                print("Last page. Breaking")
                break


        else:
            print('Error: '+str(rj))

            print('Writing...')
            writeData(f'{OUTPUTFILE}-error.json', data)

            print('Number of total API queries: '+str(apiRequests))

            elapsed=time.time()-start
            print('Elapsed time: '+str(timedelta(seconds=elapsed)))

            print('Total Stored: '+str(totalStored))
            print('Saved: '+str(len(data)))
            exit(0)

    print('Writing...')
    writeData(f'{OUTPUTFILE}.json', data)

    print('Number of total API queries: '+str(apiRequests))

    elapsed = time.time()-start
    print('Elapsed time: '+str(timedelta(seconds=elapsed)))

    print('Total Stored: '+str(totalStored))
    print('Saved: '+str(len(data)))

if __name__ == "__main__":
  execute()
