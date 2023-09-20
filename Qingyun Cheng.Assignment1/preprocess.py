import os
from Porter_stemmer import PorterStemmer

contracts = {
    ".": " . ",
    "'s": " 's ",
    "s'": "s ' ",
    "'all": "",
    "'am": "",
    "'cause": "because",
    "'d": " would",
    "'ll": " will",
    "'re": " are",
    "'em": " them",
    "doin'": "doing",
    "goin'": "going",
    "nothin'": "nothing",
    "somethin'": "something",
    "havin'": "having",
    "lovin'": "loving",
    "'coz": "because",
    "thats": "that is",
    "whats": "what is",
    "I'm": "I am",
    "I'm'a": "I am about to",
    "I'm'o": "I am going to",
    "I've": "I have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'd": "I would",
    "I'd've": "I would have",
    "Whatcha": "What are you",
    "amn't": "am not",
    "ain't": "are not",
    "aren't": "are not",
    "'cause": "because",
    "can't": "cannot",
    "can't've": "cannot have",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "daren't": "dare not",
    "daresn't": "dare not",
    "dasn't": "dare not",
    "didn't": "did not",
    "didn’t": "did not",
    "don't": "do not",
    "don’t": "do not",
    "doesn't": "does not",
    "e'er": "ever",
    "everyone's": "everyone is",
    "finna": "fixing to",
    "gimme": "give me",
    "gon't": "go not",
    "gonna": "going to",
    "gotta": "got to",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he've": "he have",
    "he's": "he is",
    "he'll": "he will",
    "he'll've": "he will have",
    "he'd": "he would",
    "he'd've": "he would have",
    "here's": "here is",
    "how're": "how are",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how's": "how is",
    "how'll": "how will",
    "isn't": "is not",
    "it's": "it is",
    "'tis": "it is",
    "'twas": "it was",
    "it'll": "it will",
    "it'll've": "it will have",
    "it'd": "it would",
    "it'd've": "it would have",
    "kinda": "kind of",
    "let's": "let us",
    "luv": "love",
    "ma'am": "madam",
    "may've": "may have",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "ne'er": "never",
    "o'": "of",
    "o'clock": "of the clock",
    "ol'": "old",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "o'er": "over",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shalln't": "shall not",
    "shan't've": "shall not have",
    "she's": "she is",
    "she'll": "she will",
    "she'd": "she would",
    "she'd've": "she would have",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "somebody's": "somebody is",
    "someone's": "someone is",
    "something's": "something is",
    "sux": "sucks",
    "that're": "that are",
    "that's": "that is",
    "that'll": "that will",
    "that'd": "that would",
    "that'd've": "that would have",
    "'em": "them",
    "there're": "there are",
    "there's": "there is",
    "there'll": "there will",
    "there'd": "there would",
    "there'd've": "there would have",
    "these're": "these are",
    "they're": "they are",
    "they've": "they have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they'd": "they would",
    "they'd've": "they would have",
    "this's": "this is",
    "this'll": "this will",
    "this'd": "this would",
    "those're": "those are",
    "to've": "to have",
    "wanna": "want to",
    "wasn't": "was not",
    "we're": "we are",
    "we've": "we have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we'd": "we would",
    "we'd've": "we would have",
    "weren't": "were not",
    "what're": "what are",
    "what'd": "what did",
    "what've": "what have",
    "what's": "what is",
    "what'll": "what will",
    "what'll've": "what will have",
    "when've": "when have",
    "when's": "when is",
    "where're": "where are",
    "where'd": "where did",
    "where've": "where have",
    "where's": "where is",
    "which's": "which is",
    "who're": "who are",
    "who've": "who have",
    "who's": "who is",
    "who'll": "who will",
    "who'll've": "who will have",
    "who'd": "who would",
    "who'd've": "who would have",
    "why're": "why are",
    "why'd": "why did",
    "why've": "why have",
    "why's": "why is",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "you're": "you are",
    "you've": "you have",
    "you'll've": "you shall have",
    "you'll": "you will",
    "you'd": "you would",
    "you'd've": "you would have",

    "to cause": "to cause",
    "will cause": "will cause",
    "should cause": "should cause",
    "would cause": "would cause",
    "can cause": "can cause",
    "could cause": "could cause",
    "must cause": "must cause",
    "might cause": "might cause",
    "shall cause": "shall cause",
    "may cause": "may cause"

}

stop = [
    'a',
    'all',
    'an',
    'and',
    'any',
    'are',
    'as',
    'at',
    'be',
    'been',
    'but',
    'by',
    'few',
    'from',
    'for',
    'have',
    'he',
    'her',
    'here',
    'him',
    'his',
    'how',
    'i',
    'in',
    'is',
    'it',
    'its',
    'many',
    'me',
    'my',
    'none',
    'of',
    'on',
    'or',
    'our',
    'she',
    'some',
    'the',
    'their',
    'them',
    'there',
    'they',
    'that',
    'this',
    'to',
    'us',
    'was',
    'what',
    'when',
    'where',
    'which',
    'who',
    'why',
    'will',
    'with',
    'you',
    'your'

]

def removeSGML(input_str):
    lines = input_str.split("\n")
    list_new = []
    for i in lines:
        if i != '' and i[0] != '<':
            list_new.append(i)
    return list_new

def tokenizeText(string):
    print(type(contracts))
    for k, v in contracts.items():
        string = string.replace(k, v)
    l = string.split()
    return l

def removeStopwords(token_list):
    for i in stop:
        while i in token_list:
            token_list.remove(i)
    return token_list

def stemWords(token_list):
    ps = PorterStemmer()
    for i, j in enumerate(token_list):
        token_list[i] = ps.stem(j, 0, len(j)-1)
    return token_list

def main():
    ans = open("./preprocess.answers.txt", "w+")
    out = open("./preprocess.output", "w+")

    PATH = "/Users/chengqingyun/Desktop/cranfieldDocs/"
    files = os.listdir(PATH)
    txt = ""
    for file in files:
        with open(os.path.join(PATH, file)) as f:
            data = f.read()
        removed_data = removeSGML(data)
        removed_str = "\n".join(removed_data)
        txt += removed_str

        print(removed_str)

    l = tokenizeText(txt)
    print(l)
    l2 = removeStopwords(l)
    print(l2)

    l3 = stemWords(l2)
    print(l3)

    cnt = len(l3)
    di = dict()
    for i in l3:
        if i not in di:
            di[i] = 1
        else:
            di[i] += 1

    di2 = sorted(di.items(), key=lambda x: x[1], reverse=True)

    print()
    for i in range(min(50, len(di2))):
        print(di2[i])

    out.write("Words" + " " + str(len(l3))+"\n")
    out.write("Vocabulary" + " " + str(len(di))+"\n")
    for i in range(min(50, len(di2))):
        out.write("Word" + str(di2[i][0]) + " " + str(di2[i][1])+"\n")

    ans.write(len(str(len(l3))))
    ans.write(str(len(di)))
    for i in range(min(25, len(di2))):
        out.write("Word" + str(di2[-i-1][0]) + " " + str(di2[-i-1][1])+"\n")

main()
