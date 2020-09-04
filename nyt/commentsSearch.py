# Demo code sample. Not indended for production use.

# See instructions for installing Requests module for Python
# http://docs.python-requests.org/en/master/user/install/

import requests
import json
import time
import math
from datetime import timedelta
import urllib.parse as parser

periods = ((19960101,20031231),(20040101,20170327))
apiKey = '5eA3yPtQOAOlTBaMbK1BCbfPLk0GDZU8'
validPages=range(200+1)

def writeData(name,data):
    with open(name,'w') as f:
        json.dump(data,f)

def getMaxOffset(x):
    return max(0,(math.ceil(x/25)-1)*25)


def execute():

    with open('lives-column-no-repeats-filtered.json') as f:
        data=json.load(f)
        articleInfo=[]
        cRequests=0
        rRequests=0
        totalComments=0
        totalReplies=0
        for article in data:
            info={}
            articleURL = article['web_url']
            info['web_url']=article['web_url']
            info['commentCount']=0
            info['totalReplies']=0
            encodedURL = parser.quote(articleURL,safe='')
            print('Processing: '+articleURL)
            commentCount=0
            commentOffset=0
            maxCommentOff=0
            print("Processing article...")
            while commentOffset<=maxCommentOff:

                time.sleep(6)
                reqURL=f'https://api.nytimes.com/svc/community/v3/user-content/url.json?url={encodedURL}&offset={commentOffset}&api-key={apiKey}'
                reqHeaders = {"Accept": "application/json"}

                print('Comment Request: '+reqURL)
                r = requests.get(reqURL, headers=reqHeaders)
                response = json.loads(r.text)
                cRequests+=1

                if 'fault' in response or 'results' not in response or 'Error' in response["results"]:
                    print("Bad Response: ")
                    print(str(response))
                    print("API Requests: "+str(cRequests))
                    return None
                
                if not commentCount:
                    commentCount=response['results']['totalParentCommentsFound']
                    info['commentCount']=int(response['results']['totalParentCommentsFound'])
                    print('Article Comments: '+str(commentCount))

                if not maxCommentOff:
                    maxCommentOff = getMaxOffset(commentCount)
                    print("Max Comment Offset: "+str(maxCommentOff))


                comments = response['results']['comments']
                print('Processing returned comments...')


                for c in comments:
                    print("Comment ID: "+str(c['commentID']))
                    print("Reply Count: "+str(c['replyCount']))

                    replyCount=c['replyCount']
                    info['totalReplies']=int(replyCount)
                    commentSequence=c['commentSequence']

#                        if replyCount>3:
#                           print('Requesting replies...')
#                            newReplies=[]
#                            replyOffset=0
#                            maxReplyOffset=getMaxOffset(replyCount)
#                            while replyOffset<=maxReplyOffset:
#                                replyUrl = f"https://api.nytimes.com/svc/community/v3/user-content/replies.json?url={encodedURL}&commentSequence={commentSequence}&offset={replyOffset}&api-key={apiKey}"
#                                print("Reply Request: "+replyURL)
#                               res = requests.get(reqURL, headers=reqHeaders)
#                                resjson = json.loads(r.text)
#                                rRequests+=1
                commentOffset+=25

            articleInfo.append(info)
            totalComments+=info['commentCount']
            totalReplies+=info['totalReplies']

        with open('lives-info.json','w') as f:
            print("Finished")
            print("Articles: "+str(len(articleInfo)))
            print("Total Comments: "+str(totalComments))
            print("Total Replies: "+str(totalReplies))
            json.dump(articleInfo,f,indent=4)

if __name__ == "__main__":
  execute()
