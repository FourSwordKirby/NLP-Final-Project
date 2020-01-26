import nltk

from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer

import os
import subprocess
import shlex
import en

DoPattern = "inc/TregexScripts/YesNoDo.txt"
DidPattern= "inc/TregexScripts/YesNoDid.txt"
DoesPattern = "inc/TregexScripts/YesNoDoes.txt"
AuxPattern = "inc/TregexScripts/YesNoAux.txt"

Patterns = [DoPattern, DidPattern, DoesPattern, AuxPattern];

inputFileLocation = "inc/RulesWorkspace/YesNoSentences.txt"
inputTreeLocation = "inc/RulesWorkspace/results.txt"

# Generates a list of applicable Y/N questions from the list of sentences
def YesNoGeneration(conParseTrees):

    #deleting the contents of the workspace file
    with open(inputTreeLocation, 'w'): pass

    
    f=open(inputTreeLocation, 'w')
    for sentence in conParseTrees.keys():
        f.writelines(str(conParseTrees[sentence]).split('\n'))
        f.writelines("\n")
    f.close()

    Results = dict()
    #applying the yes/no tsurgeon
    for pattern in Patterns:
        print "\n"
        print "current pattern: " + pattern + inputTreeLocation
        proc = subprocess.Popen(['sh','../Libraries/tregex/tsurgeon.sh','-treeFile', inputTreeLocation, pattern], stdout=subprocess.PIPE)
        tmp = proc.stdout.read()
        Results[pattern] = tmp

    #auxilliary verbs
    auxVerbs = set(['am', 'is', 'was', 'were', 'be', 'was', 'were', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'shall', 'will', 'should', 'would', 'may', 'might', 'must', 'can', 'could'])

    parseTrees = []
    #generating parse tree results after pattern application
    currentTree = ""
    for pattern in Patterns:
        for line in Results[pattern].split('\n') :
            line = line.rstrip()
            if line == "" :
                if(currentTree != ""):
                    parseTrees.append(currentTree)
                currentTree = ""
            else:
                currentTree += line

    #generating original parse tree results
    currentTree = ""
    originalTrees = []
    f = open(inputTreeLocation)
    for line in f :
        line = line.rstrip()
        if line == "" :
            if(currentTree != ""):
                originalTrees.append(currentTree)
            currentTree = ""
        else:
            currentTree += line
    f.close();

    #filtering it out so we only have the new results
    parseTrees = set(parseTrees)
    for tree in originalTrees:
        if(tree in parseTrees):
            parseTrees.remove(tree)

    FinalQuestions = [];
    #one more filter to apply "be" word transformations
    for tree in parseTrees:
        t = nltk.Tree.fromstring(tree)
        #Applying verb tense change transformation
        for i in t.subtrees(filter=lambda x: x.label() == 'VERBBASE'):
            verb = i[0]
            if(verb in auxVerbs):
                doLocations = t.subtrees(filter=lambda x: x.label() == 'DO')
                for loc in doLocations:
                    loc[0] = verb;
                    i[0] = ""
            else:
                try:
                    presentVerb = en.verb.present(verb)
                except KeyError, e:
                    presentVerb = verb
                    break;
                i[0] = presentVerb

        #t.pprint()
        words = t.leaves()
        words[0] = words[0].capitalize()
        words[len(words) - 1] = "?"
        FinalQuestions.append(" ".join(words))

    return FinalQuestions;
