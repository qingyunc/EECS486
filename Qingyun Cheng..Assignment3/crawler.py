import sys
from bs4 import BeautifulSoup
import requests


def main():
    
    seed_file = sys.argv[1]
    max_num = sys.argv[2]
    seeds = []
    visit_path = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                   'Content-Type': 'text/html',
                   'referer': 'https://...'}

    crawler_output = open("crawler.output", "w+")
    links_output = open("links.output", "w+")

    first_line = True
    
    with open(seed_file) as file:
        for line in file:
            x = line.rstrip()
            y = x.rstrip("/")
            seeds.append(y)

            if first_line:
                a = line.rstrip()
                b = a.rstrip("/")
                c = b.lstrip("https://")
                visit_path.add(c)
            first_line = False
    while 0 < len(seeds) < int(max_num):
        url = seeds.pop(0)
        req = requests.get(url, headers=headers)
        txt = BeautifulSoup(req.text, "html.parser")

        temp_link = url.split("://")
        root = temp_link[1]
        root = root.split("/")[0]

        if not (temp_link[1].startswith("eecs.engin.umich") or temp_link[1].startswith("eecs.umich") or temp_link[1].startswith("ece.engin.umich") or temp_link[1].startswith("cse.engin.umich")):
            continue

        link_list = set()
        link_list.add(url)

        for a in txt.find_all('a'):
            link_want = a.get('href')
            if link_want:
                link_want = link_want.lstrip("//")
                link_want = link_want.rstrip("/")

                if "://" not in link_want:
                    if link_want.startswith("/"):
                        link_want = "https://" + root + link_want
                    elif link_want.startswith("./"):
                        link_want = url + link_want.lstrip(".")
                    else:
                        link_prev = link_want.count("../")
                        link_want = link_want.lstrip("../")
                        
                        r = temp_link[1].split("/")
                        space = ""
                        for i in range(len(r)-link_prev):
                            space += r[i] + "/"
                        link_want = "https://" + space + link_want

                if "#" in link_want.split("/")[-1]:
                    link_want = link_want[link_want.rindex('#')+1:]

                link_want = link_want.rstrip("/")
                if link_want not in link_list:
                    links_output.write(url + " " + link_want + "\n")
                    link_list.add(link_want)
                middle = link_want.lstrip("https://").rstrip("/")

                if (middle not in visit_path) and (middle.startswith("eecs.engin.umich") or middle.startswith("eecs.umich") or middle.startswith("ece.engin.umich") or middle.startswith("ese.engin.umich")):
                    seeds.append(link_want)
                    crawler_output.write(link_want + "/n")
                    visit_path.add(link_want.lstrip("https://"))

    crawler_output.close()
    links_output.close()


main()
