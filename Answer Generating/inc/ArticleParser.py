import sys
import math
import nltk
import re

"""
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer


def removeHeaders():
    return;

import os
from nltk.parse.stanford import StanfordParser
parserPath = "C:\Users\Roger Liu\Desktop\NLP-Final-Project\Libraries\stanford-parser-full-2015-04-20"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'  
# I am using version 3.5.2 because apparently it is the more stable version, you should replace 3.5.2 with whatever version you're using

sentence = "Alexa is yawning"
parser=StanfordParser()
print list(parser.raw_parse(sentence))
print "what"
"""

# Returns a dictionary of {heading : paragraph} where a paragraph is a list of
# sentences in fileName.
def ingest(fileName):
    articleFile = open(fileName)

    article = dict();
    currentHeading = "";
    previousSentence = "";

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for paragraph in articleFile :
        paragraph = paragraph.decode('utf8').rstrip()
        #sentences = re.split('\\.',paragraph)
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

# Maps each sentence to a list of derived sentences, then flattens.
# eg. pronoun resolution, ``Harry potter, the boy who lived,''
def augment(paragraph):
    # NYI
    return paragraph


