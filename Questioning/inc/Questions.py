"""
file: Questions.py
author: Group Neizetze
python: 2.7.10

desc:
dependencies: pyStatParser
wget https://github.com/emilmont/pyStatParser.git
sudo python setup.py install
"""


import sys

import nltk
from YesNoRules import *
from WhQuestion import *

import en
from SentenceAdjustment import editVerb

# Takes in a dict of {heading : paragraph} and returns a list of questions.
def articleToQuestion(article):
    questions = [];

    for heading in article.keys() :
        paragraph = article[heading];

        for sentence in paragraph:
            new_question = rules.who_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)

            new_question = rules.has_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)

            new_question = rules.can_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)
 
    return questions

# Returns the top num questions in questions.
def determineBestQuestions(questions, num):
    # NYI
    return []

"""
********************************************************************************
"""

#used to get the dependency parser working
parserPath = "C:/Users/Roger Liu/Desktop/nlp-Final-Project/Libraries/stanford-parser"
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_40/bin'  #or your java path
os.environ['CLASSPATH'] = parserPath + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parserPath + '/stanford-parser-3.5.2-models.jar'
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


#stanford parser workspace stuff
inputFileLocation = "inc/RulesWorkspace/originalSentences.txt"
conOutputFileLocation = "inc/RulesWorkspace/constituencyParses.txt"
depOutputFileLocation = "inc/RulesWorkspace/dependencyParses.txt"

parserLocation = "../Libraries/stanford-parser"
conParseCommand = "java -classpath %s/stanford-parser.jar -mx1000m edu.stanford.nlp.parser.lexparser.LexicalizedParser %s/" \
               "stanford-parser-3.5.2-models/englishPCFG.ser.gz %s >> %s" % (parserLocation, parserLocation, inputFileLocation, conOutputFileLocation)

depParseCommand = "java -classpath %s/stanford-parser.jar -mx1000m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat conll2007 %s/" \
               "stanford-parser-3.5.2-models/englishPCFG.ser.gz %s >> %s" % (parserLocation, parserLocation, inputFileLocation, depOutputFileLocation)


# Generates a list of questions from a list of sentences.
def simpleQuestionGen(article):

    #deleting the contents of the workspace files
    with open(inputFileLocation, 'w'): pass
    with open(conOutputFileLocation, 'w'): pass
    with open(depOutputFileLocation, 'w'): pass

    #writing the article to a file for the shell scripts to use
    f=open(inputFileLocation, 'w')
    for sentence in article:
	f.writelines(sentence)
	f.writelines("\n")
    f.close()

    print "\n\n getting con parses"
    #Generating the constituency parse once
    subprocess.call(conParseCommand, shell=True)

    print "\n\n getting dep parses"
    #Generating the dependency parse once
    subprocess.call(depParseCommand, shell=True)

    

    #generating the results of the parse

    #dependency parsing first
    depParses = dict()
    currentParse = ""
    i = 0;
    f = open(depOutputFileLocation)
    for line in f :
        if line.decode('ascii', 'ignore').rstrip() == "" :
            if(currentParse != ""):
                #make sure that the sentence is actually machine readable
                try:
                    article[i] = article[i].encode('utf8')
                except UnicodeDecodeError, e:
                    i+=1;
                    currentParse = ""
                    continue;
                depParse = DependencyGraph(currentParse, top_relation_label='root')
                article[i] = editVerb(article[i], depParse)
                depParses[article[i]] = depParse;
                i+=1;
            currentParse = ""
        else:
            currentParse += line
    
    f.close();

    #now consitituency parsing
    conParseTrees = dict()
    currentTree = ""
    i = 0;
    f = open(conOutputFileLocation)
    for line in f :
        line = line.decode('ascii', 'ignore').rstrip()
        if line == "" :
            if(currentTree != ""):
                #make sure that the sentence is actually machine readable
                try:
                    article[i] = article[i].encode('utf8')
                except UnicodeDecodeError, e:
                    i+=1;
                    currentTree = ""
                    continue;
		#generating the dependency parse
		conParseTrees[article[i]] = nltk.ParentedTree.fromstring(currentTree)		
                i+=1;
            currentTree = ""
        else:
            currentTree += line
    f.close();




    

    WhQuestions = WhGeneration(conParseTrees, depParses)

    print "THIS IS WH QUESTIONS"
    for question in WhQuestions:
        print question

    print "THIS IS Y/N QUESTIONS"        
    YesNoQuestions = YesNoGeneration(conParseTrees)
    for question in YesNoQuestions:
        print question
        
    #print YesNoQuestions

    '''
    for sentence in conParseTrees.keys():
        print sentence
        conTree = conParseTrees[sentence];
        #depTree = depParseTrees[sentence];
        print conTree.pretty_print();
        print depTree.pretty_print();
    '''

    return []

