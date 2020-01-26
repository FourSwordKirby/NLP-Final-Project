import nltk

from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer

'''
from practnlptools.tools import Annotator

#Testing the abilities of nltk
testString = "I made a poop in my pants"

#part of speech tagging
print(nltk.pos_tag(nltk.word_tokenize(testString)))

print(nltk.__version__)

annotator=Annotator()
notes = annotator.getAnnotations("There are people dying make this world a better place for you and for me.")
print notes['syntax_tree']
'''

import os
from nltk.parse.stanford import StanfordParser
parserPath = "C:\Users\Roger Liu\Desktop\NLP-Final-Project\Libraries\stanford-parser-full-2015-04-20"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'  
# I am using version 3.5.2 because apparently it is the more stable version, you should replace 3.5.2 with whatever version you're using

sentence = "People yawn in public spaces"
parser=StanfordParser()
print list(parser.raw_parse(sentence))
print "what"
