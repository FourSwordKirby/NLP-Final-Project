"""
file: ArticleParser.py
author: Group Neizetze
python: 2.7.10

desc: Parses the article to create a python representation to manipulate.
dependencies: tokenizers/punkt/english.pickle
              download nltk, then run nltk.download() -> d -> punkt
"""

import sys
import nltk

# Returns a dictionary of {heading : paragraph} where a paragraph is a list of
# sentences in fileName.
def ingest(fileName):
    articleFile = open(fileName)

    article = dict();
    currentHeading = "";
    previousSentence = "";

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for paragraph in articleFile :
        paragraph = paragraph.decode('utf-8').rstrip()
        sentences = tokenizer.tokenize(paragraph);

        if(len(sentences) == 1 and not(paragraph == "") and previousSentence == ""):
            currentHeading = paragraph
            article[currentHeading] = [];
        elif(not(currentHeading == "")):
            for sentence in sentences:
                if(not (sentence == "")):
                    article[currentHeading].append(sentence)

        previousSentence = paragraph;

    articleFile.close()
    return article

def augment(paragraph):
    # spooky. augment the sentences of the paragraph.
    return paragraph

"""
********************************************************************************
"""

# JUST FOR TESTING. return a list of the sentneces
def simpleIngest(fileName):
    articleFile = open(fileName).decode('ascii', 'ignore')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = []
    for paragraph in articleFile:
        print paragraph
        news = tokenizer.tokenize(paragraph.decode('utf8').rstrip())
        print news
        if len(news) == 0 or news[0][-1:] != '.':
            continue
        for sentence in news:
            try:
                sentence = sentence.encode('utf8')
            except UnicodeDecodeError, e:
                continue;
            sentences.append(sentence)
    return sentences

# JUST FOR TESTING. remove the short sentences. This should probably be fused
# with simpleIngest if we want to make it fast.
def simpleAugment(sentences):
    # get rid of short ones... probably not actually helpful.
    sentences = filter(lambda x: 3 <= len(x.split(' ')) and len(x.split(' ')) <= 20, sentences)
    # pronoun resolution requires some depencency parsing for a passable
    # heuristic. waiting on it.

    #maybe we want to grab sentences with a lot of pronouns?
    #questions which are derived from pronouns may be hard to answer

    #we're returning the 1st 150 sentences
    return sentences[:10]

