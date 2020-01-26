"""
file: SentenceAdjustment.py
author: Group Neizetze
python: 2.7.10

desc:
"""
import os
import en

# Load these exactly once.
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.parse.stanford import *

parserPath = "C:/Users/Roger Liu/Desktop/nlp-Final-Project/Libraries/stanford-parser"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'
parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


# Change the verb to a synonym of it.
def editVerb(statement, statementParse):
    # find the verb
    head = statementParse.tree()._label

    synset = lesk(statement, head, 'v')
    if synset is None:
        return statement
    syns = synset.lemma_names()
    for syn in syns:
        syn = matchTense(syn, head)
        try:
            synbase = en.verb.present(syn.lower())
        except KeyError, e:
            break;
        try:
            headbase = en.verb.present(head.lower())
        except KeyError, e:
            break;
        if syn not in head and synbase is not headbase:
            statement = statement.replace(head, syn)
            break
    return statement

#returns a version of verb1 whose tense matches verb2
def matchTense(verb1, verb2):
    desiredTense = en.verb.tense(verb2)

    newVerb = ""
    if desiredTense == "1st singular present":    
        newVerb = en.verb.present(verb1, person = "1")
    elif desiredTense == "2nd singular present":    
        newVerb = en.verb.present(verb1, person = "2")
    elif desiredTense == "3rd signular present":
        newVerb = en.verb.present(verb1, person = "3")
    elif desiredTense == "present plural":    
        newVerb = en.verb.present(verb1, person = "*")
    elif desiredTense == "present participle":
        newVerb = en.verb.present_participle(verb1)
    elif desiredTense == "past":
        newVerb = en.verb.past(verb1)
    elif desiredTense == "1st singular past":
        newVerb = en.verb.past(verb1, person = "1")
    elif desiredTense == "2nd singular past":
        newVerb = en.verb.past(verb1, person = "2")
    elif desiredTense == "3rd signular past":
        newVerb = en.verb.past(verb1, person = "3")
    elif desiredTense == "past plural":
        newVerb = en.verb.past(verb1, person = "*")
    elif desiredTense == "past participle":
        newVerb = en.verb.past_participle(verb1)
    elif desiredTense == "infinitive":    
        newVerb = en.verb.infinitive(verb1)
    return newVerb;

