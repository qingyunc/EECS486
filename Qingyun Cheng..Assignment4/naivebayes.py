import preprocess
import math
import sys
import os


def trainNaiveBayes(paths):
    vocabulary = set()
    class_probabilities = {}
    word_probabilities = {'true': {}, 'fake': {}}

    for traningfile in paths:

        with open(traningfile, 'r', encoding='ISO-8859-1') as file:
            text = file.read()
            tokens = preprocess.tokenizeText(text)

            unique_words = set(tokens)
            vocabulary.update(unique_words)

    voc_size = len(vocabulary)

    true_wrd = []
    fake_wrd = []

    true_cnt = 0
    fake_cnt = 0

    for token in tokens:
        if 'fake' in paths:
            fake_cnt += 1
            fake_wrd.append(token)
        else:
            true_cnt += 1
            if token not in true_wrd:
                true_wrd.append(token)

    class_denom = true_cnt + fake_cnt

    class_probabilities['true'] = true_cnt / class_denom
    class_probabilities['fake'] = fake_cnt / class_denom

    for token in tokens:
        word_probabilities['true'][token] = (
            true_wrd.count(token) + 1) / (len(true_wrd) + voc_size)

        word_probabilities['fake'][token] = (
            fake_wrd.count(token) + 1) / (len(fake_wrd) + voc_size)

    return class_probabilities, word_probabilities, true_wrd, fake_wrd, voc_size


def testNaiveBayes(test_paths, class_probabilities, word_probabilities, voc_size, true_wrd, fake_wrd):

    true_score = class_probabilities['true']
    fake_score = class_probabilities['fake']

    test_probabilities = {'fake': fake_score, 'true': true_score}

    with open(test_paths, 'r', encoding='ISO-8859-1') as file_test:
        text = file_test.read()
        tokens = preprocess.tokenizeText(text)

        for token in tokens:
            if token not in word_probabilities['true']:
                test_probabilities['true'] *= math.log(
                    (1 / (len(true_wrd) + voc_size)))
            else:
                test_probabilities['true'] *= math.log(
                    word_probabilities['true'][token])

            if token not in word_probabilities['fake']:
                test_probabilities['fake'] *= math.log(
                    (1 / (len(fake_wrd) + voc_size)))
            else:
                test_probabilities['fake'] *= math.log(
                    word_probabilities['fake'][token])

    if test_probabilities['true'] > test_probabilities['fake']:
        return 'true'
    else:
        return 'fake'
    
def get_top_words(dictionary):
    true_words = sorted(dictionary['true'].items(), key=lambda x:x[1], reverse=True)[:10]
    fake_words = sorted(dictionary['fake'].items(), key=lambda x:x[1], reverse=True)[:10]
    return {'true':true_words, 'fake': fake_words}



def main():
    folder = sys.argv[1]
    list_file = []

    for file in os.listdir(folder):
        paths = os.path.join(folder, file)
        list_file.append(paths)

    out = "./naivebayes.output.fakenewsai.txt"
    ans = "./naivebayes.answers.txt"
    cnt = 0
    with open(out, 'a') as output:
        for file in list_file:

            list_file2 = list_file.copy()
            list_file2.remove(file)

            class_prob, word_prob, true_wrd, fake_wrd, voc_size = trainNaiveBayes(
                list_file2)
            pred_class = testNaiveBayes(
                file, class_prob, word_prob, voc_size, true_wrd, fake_wrd)
            if 'true' in file:
                tmp = 'true'
            else:
                tmp = 'fake'

            if pred_class == tmp:
                cnt += 1

            output.write(file[9:] + " " + pred_class + '\n')

    accuracy = cnt/len(list_file)
    sort_word_prob = get_top_words(word_prob)

    with open(ans, 'w') as answer:
        answer.write(str(accuracy) + '\n')
        for word, prob in sort_word_prob.items():
            answer.write(str(word) + " " + str(prob)+ " "+ '\n')
        
        


if __name__ == "__main__":
    main()
