"""
file: Questions.py
author: Group Neizetze
python: 2.7.10

desc:
"""

import nltk

# Load these exactly once.
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.parse.stanford import *

import os
import subprocess
import shlex
import en


parserPath = "C:/Users/Roger Liu/Desktop/nlp-Final-Project/Libraries/stanford-parser"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'
parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

inputFileLocation = "inc/RulesWorkspace/WhSentences.txt"
outputFileLocation = "inc/RulesWorkspace/results.txt"
parserLocation = "../Libraries/stanford-parser"
command = "java -classpath %s/stanford-parser.jar -mx512m edu.stanford.nlp.parser.lexparser.LexicalizedParser %s/" \
           "stanford-parser-3.5.2-models/englishPCFG.ser.gz %s >> %s" % (parserLocation, parserLocation, inputFileLocation, outputFileLocation)


def categorize(sentence, word):
    cur = lesk(sentence, word, 'n')
    if cur is None: return 'Who'
    cur = cur.lexname()
    if cur == 'noun.person': return 'Who'
    elif cur == 'noun.location': return 'Where'
    elif cur == 'noun.time': return 'When'
    else: return 'What'

""" Testing: categorize
# LOL Wordnet can't categorize Sam as a person.
print "Sam: " + categorize('I talked to Sam.', 'Sam')
# LOL Wordnet can't categorize I as a person.
print "I: " + categorize('I talked to Sam.', 'I')
print "Mary: " + categorize('Mary is my friend.', 'Mary')
print "Boston: " + categorize('I go to school in Boston.', 'Boston')
print "library: " + categorize('I read at the library.', 'library')
print "fox: " + categorize('The fox hid the dog.', 'fox')
print "tree: " + categorize('The birds sang in the tree.', 'tree')
print "brush: " + categorize('The fox hid in the brush.', 'brush')
print "festival: " + categorize('The festival was fun.', 'festival')
"""

# Generates a list of questions from a list of sentences.
def WhGeneration(conParseTrees, depParses):

    #deleting the contents of the workspace file
    with open(outputFileLocation, 'w'): pass

    # Put the subjects here.
    subjects = set()
    # Put all generated questions here.
    questions = []

    # Find the subject, if there is one.
    def getSubjects(parse):
        triples = list(parse.triples())
        for triple in triples:
            if 'nsubj' in triple:
                subjects.add(triple[2][0])

    def transformSubject(subject, np, sentence):
        question = sentence.replace(np, categorize(sentence, subject))
        question = question[:-1] + '?'
        questions.append(question)
        #print "Subject" +  question

    def transformNonsubject(np, sentence, auxVerb):
        for parse in dep_parser.raw_parse(np):
            head = parse.tree()._label
            break
        question = sentence.replace(np, '')
        question = question[:-1] + '?'
        question = question[:1].lower() + question[1:]
        question = " " + auxVerb + " " + question
        question = categorize(sentence, head) + question
        question = question[:-1] + '?'
        questions.append(question)
        #print question

    # Find the NP for the subject. Only look shallowly.
    def transformNounPhrases(subjects, tree):
        sentence = ' '.join(tree.leaves())
        for subtree in tree.subtrees(lambda t: t._label == 'NP'):
            crawlNode = subtree
            isclose = False;
            for i in xrange(3):
                crawlNode = crawlNode.parent()
                if(crawlNode.label() == "ROOT"):
                    isclose = True;
                    break;

            if(not isclose):
                continue;
            
            leaves = subtree.leaves()
            subjectSet = set(leaves).intersection(subjects)
            isSubject = len(subjectSet) > 0

            if isSubject:
                transformSubject(next(iter(subjectSet)),
                        str(subtree.flatten())[4:-1],
                        sentence)
            else:
                VBPcount = len(list(tree.subtrees(lambda t: t._label == 'VBP')))
                VBDcount = len(list(tree.subtrees(lambda t: t._label == 'VBD')))
                VBZcount = len(list(tree.subtrees(lambda t: t._label == 'VBZ')))

                maxValue = max(VBPcount, VBDcount, VBZcount)
                if(maxValue == VBPcount):
                    auxVerb = "do"
                elif(maxValue == VBDcount):
                    auxVerb = "did"
                elif(maxValue == VBZcount):
                    auxVerb = "does"
                transformNonsubject(str(subtree.flatten())[4:-1],
                        sentence, auxVerb)

    for sentence in conParseTrees.keys():
        getSubjects(depParses[sentence])
        transformNounPhrases(subjects, conParseTrees[sentence])

    return questions

""" Testing: simpleQuestionGen
simpleQuestionGen("The quick brown fox jumps over the lazy dog.")
simpleQuestionGen("I talked to Sam.")
simpleQuestionGen("Abraham Lincoln was born on February 12, 1809.")
"""



""" Testing: editVerb
editVerb("Who talked to Sam ?")
"""

