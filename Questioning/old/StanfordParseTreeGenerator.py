import nltk

from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer

import os
import subprocess
import shlex

''' old pract NLP stuff
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

'''old stanford parser config
import os
from nltk.parse.stanford import StanfordParser
parserPath = "C:/Users/Roger Liu/Desktop/nlp-final-project/Libraries/stanford-parser-full-2015-04-20"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'  
# I am using version 3.5.2 because apparently it is the more stable version, you should replace 3.5.2 with whatever version you're using

sentence = "People yawn in public spaces"
parser=StanfordParser()
print list(parser.raw_parse(sentence))
print "what"
'''

#Using the standford parser on all sentences in 1.txt
pattern = "NP < (NP=np < NNS) < (NP=np1 < NN)"
pattern2 = "SQ < ((VBZ $ VBZ)$+NP)  "
pattern3 = "NP"

inputFileLocation = "testSentences.txt"
outputFileLocation = "results.txt"
parserLocation = "../Libraries/stanford-parser"
command = "java -classpath %s/stanford-parser.jar -mx512m edu.stanford.nlp.parser.lexparser.LexicalizedParser %s/" \
           "stanford-parser-3.5.2-models/englishPCFG.ser.gz %s >> %s" % (parserLocation, parserLocation, inputFileLocation, outputFileLocation)

subprocess.call(command, shell=True)

#displaying each of the sentences as their tree
f = open(outputFileLocation)
parsetrees = []
currentTree = ""
for line in f :
    line = line.rstrip()
    if line == "" :
        parsetrees.append(currentTree)
        currentTree = ""
    else:
        currentTree += line

for tree in parsetrees:
    t = nltk.Tree.fromstring(tree)
    t.draw()
f.close()

#applying tregex on the stuff
proc = subprocess.Popen(['sh','../Libraries/tregex/tregex.sh','-n',pattern3,outputFileLocation], stdout=subprocess.PIPE)



