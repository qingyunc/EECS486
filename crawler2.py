import sys
from bs4 import BeautifulSoup
import requests


def main():
    seedFilesName = sys.argv[1]
    maxNumUrl = sys.argv[2]
    seeds = []
    visitedPaths = set()
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 
                'referer': 'https://...'}
    
    crawlerOutput = open("crawler.output", "a")
    linksoutput = open("links.output", "a")
    
    
    isfirstLine = True
    with open(seedFilesName) as file:
        for line in file:
            seeds.append(line.rstrip().rstrip("/"))

            
            if isfirstLine:
                visitedPaths.add(line.rstrip().rstrip("/").lstrip("https://"))
                
            isfirstLine = False

    while len(seeds) < int(maxNumUrl):
        currUrl = seeds.pop(0)
        h = requests.head(currUrl)
        header = h.headers
        content_type = header.get('content-type')
        if content_type == "text/html":

            r = requests.get(currUrl, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            splitedlink = currUrl.split("://")
            documentRoot = splitedlink[1].split("/")[0]
            
            if (not splitedlink[1].startswith("eecs.engin.umich")) and (not splitedlink[1].startswith("eecs.umich")) and (not splitedlink[1].startswith("ece.engin.umich")) and (not splitedlink[1].startswith("cse.engin.umich")):
                continue
            
            linksSet = set()
            linksSet.add(currUrl)
            
            for link in soup.find_all('a'):
                mylink = link.get('href')
                if mylink is None: continue

                mylink = mylink.lstrip("//").rstrip("/")

                if "#" in mylink.split("/")[-1]:
                    mylink = mylink[mylink.rindex('#')+1:]

                if "://" not in mylink:
                    if mylink.startswith("/"):
                        mylink = "https://" + documentRoot + mylink
                    elif mylink.startswith("./"):
                        mylink = currUrl + mylink.lstrip(".")
                    else:
                        goback = mylink.count("../")
                        mylink = mylink.lstrip("../")
                        path = splitedlink[1].split("/")
                        toAppend = ""
                        for i in range(len(path) - goback):
                            toAppend += path[i] + "/"
                        mylink = "https://" + toAppend + mylink
                mylink = mylink.rstrip("/")
                if mylink not in linksSet:
                    linksoutput.write(currUrl + "" + mylink + "\n")
                    linksSet.add(mylink)
                body = mylink.lstrip("https://").rstrip("/")

                if (body not in visitedPaths) and (body.startswith("eecs.engin.umich") or body.startswith("eecs.umich") or body.startswith("ece.engin.umich") or body.startswith("ese.engin.umich")):
                    seeds.append(mylink)
                    crawlerOutput.write(mylink + "/n")
                    visitedPaths.add(mylink.lstrip("https://"))
                        

    crawlerOutput.close()
    linksoutput.close()


main()
