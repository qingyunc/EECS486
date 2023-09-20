import sys

## I can not find what is wrong from the part2. gsi thinks is from the linksoutput of the part1, they told me that my part2 looks corret to them. Thy said if I get correct for part one I should get correct output for part two.
## Nam Ho read my part 2 line by line and he said part2 looks correct for him

def main():
    Urls = sys.argv[1]
    Links = sys.argv[2]
    thre = float(sys.argv[3])
    
    preds = {}
    cnt_want = {}
    with open(Links, "r") as links:
        for link in links.readlines():
            first = link.split(" ")[0]
            second = link.split(" ")[1].strip()
            if first in cnt_want:
                cnt_want[first] += 1
            else:
                cnt_want[first] = 1
            if second in preds:
                preds[second].append([first])
            else:
                preds[second] = [first]
    
    score_temp = {}
    with open(Urls, "r") as urls:
        for url in urls.readlines():
            url = url.strip()
            score_temp[url] = 0.25
    score_temp["http://eecs.engin.umich.edu"] = 0.25
    
    score_list = {}
    l = len(score_temp)
    
    converge = False
    cnt = 0
    while not converge:
        cnt += 1
        for s in score_temp:
            score = 0.15/l
            for p in preds.get(s, []):
                score += 0.85 * score_temp[p]/cnt_want[p]
            score_list[s] = score
        converge = True
        for a in score_list:
            if abs(score_temp[a] - score_list[a]) > thre:
                converge = False
        score_temp = score_list
    score_sort = dict(
        sorted(score_temp.items(), key=lambda item: item[1], reverse=True))
    
    
    out = open("pagerank.output", "w+")
    for s in score_sort:
        out.write(s + " " + str(score_sort[s]) + "\n")
    
    out.close()

    ans =  open("crawler.pagerank.answers", "w+")
    ans.write("less than 1200s"  + "\n" + str(cnt))

    ans.close()

    

main()