import sys

def main():
    urlFile = sys.argv[1]
    linkFile = sys.argv[2]
    threth = float(sys.argv[3])
    
    
    preds = {}
    successorCount = {}
    links = open(linkFile, 'r')
    lines = links.readlines()
    for line in lines:
        sourceUrl = line.split(" ")[0]
        destUrl = line.split(" ")[1]
        destUrl = destUrl.strip()
        if destUrl not in preds:
            preds[destUrl] = [sourceUrl]
        else:
            preds[destUrl].append([sourceUrl])
        if sourceUrl not in successorCount:
            successorCount[sourceUrl] = 1
        else:
            successorCount[sourceUrl] += 1
    currScores = {}
    urls = open(urlFile, 'r')
    urlLines = urls.readlines()
    for urlLine in urlLines:
        urlLine = urlLine.strip()
        currScores[urlLine] = 0.25
    currScores["http://eecs.engin.umich.edu"] = 0.25
    newScores = {}
    N = len(currScores)
    converged = False
    count = 0
    while not converged:
        count += 1
        for key in currScores:
            newScore = 0.15/N
            for predecessor in preds.get(key, []):
                newScore += 0.85 * currScores[predecessor]/successorCount[predecessor]
            newScores[key] = newScore
        converged = True
        for node in newScores:
            if abs(currScores[node] - newScores[node]) > threth:
                converged = False
        currScores = newScores
    sortedScores = dict(
        sorted(currScores.items(), key=lambda item: item[1], reverse=True))
    output = open("pagerank.output", "w")
    for key in sortedScores:
        output.write(key + " " + str(sortedScores[key]) + "\n")
    output.close()
    links.close()
    urls.close()


main()
