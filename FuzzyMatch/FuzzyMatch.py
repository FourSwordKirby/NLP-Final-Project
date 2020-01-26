# How to use fuzzywuzzy: pip install git+git://github.com/seatgeek/fuzzywuzzy.git@0.10.0#egg=fuzzywuzzy
from fuzzywuzzy import fuzz
from nltk.tag import StanfordNERTagger, StanfordPOSTagger
# How to use nltk: find the whl package at http://www.lfd.uci.edu/~gohlke/pythonlibs/#nltk
from nltk import tokenize
import os

# This script searches through an article with a question and finds the target sentence that
# is mostly likely to contain the answer.

# After the target sentence is found, pass this sentence to the method to find the answer
# There are two kinds of questions: Yes-No questions(aka binary question) and WH-questions.
def find_the_answer(target_sentence, question_sentence):
    # Classify the question: binary, WH-questions
    # Assume find_the_answer could correctly classify the question all the time.
 
    question_sentence = question_sentence.lower().split()

    # Got the line of codes below from Aditya
    binary_question_keywords = ["be","am","are","is","was","were","being","been","can","could","dare","do","does","did","have","has","had","having","may","might","must","need","ought","shall","should","will","would"]
    wh_question_keywords = ['who','where','what','when','how','why','which']

    binary_question_flag = False
    # Check whether or not this question is a binary question by going through a list of keywords in binary questions
    # Sample question 1: What is his name?
    # Sample question 2: Is he from Connecticut?
    # Both of the sample sentences have "is," thus we want to look at the first word in the sentence.
    first_word_of_the_question = question_sentence[0]

    if first_word_of_the_question in binary_question_keywords:
        binary_question_flag = True

    if binary_question_flag:
        # Looking for the word "not" in the sentence; if there is "not", return an answer of "no";
        # otherwise, return an answer of "yes".
        if 'not' in target_sentence:
            return 'No'
        else:
            return 'Yes'

    # If the question is not a binary question (when binary_flag == False), it is a WH-question
    # Or we could do it in an opposite way: if it is not a WH-question, it is a binary question.
    # Download StanfordPOSTagger(ver 3.5.2) at http://nlp.stanford.edu/software/stanford-postagger-2015-04-20.zip
    # Download StanfordNERTagger(ver 3.5.2) at http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip
    # Change the directories of packages of the variables "st" and "java_path" accordingly
    else:
        java_path = "C:/Program Files/Java/jdk1.8.0_65/bin/java.exe"
        os.environ['JAVAHOME'] = java_path
        st = StanfordNERTagger('C:/Users/Barry/Desktop/CMU/2. Second Semester/11611 NLP/project/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'C:/Users/Barry/Desktop/CMU/2. Second Semester/11611 NLP/project/stanford-ner-2015-04-20/stanford-ner.jar')
        r = st.tag('Rami Eid is studying at Stony Brook University in New York'.split())

        # Check which WH word it is in the question
        if first_word_of_the_question == 'who':
            # Who question
            person = ''
            for i in range(0, len(r)):
                if person != '':
                    break
                if r[i][1] == 'PERSON':
                    person += r[i][0] + ' '
                    while (i + 1 < len(r) and r[i+1][1] == 'PERSON'):
                        i += 1
                        person += r[i][0]

            return person

        elif first_word_of_the_question == 'where':
            # Where question
            # Find the label, LOCATION, in the sentence
            location = ''
            for i in range(0, len(r)): # i < len(r)
                if location != '':
                    break
                if r[i][1] == 'LOCATION':
                    location += r[i][0] + ' '
                    while (i + 1 < len(r) and r[i+1][1] == 'LOCATION'):
                        i += 1
                        location += r[i][0]
            return location

        # For "when" questions, change the st variable to:
        # st = StanfordNERTagger('C:/Users/Barry/Desktop/CMU/2. Second Semester/11611 NLP/project/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
        #       'C:/Users/Barry/Desktop/CMU/2. Second Semester/11611 NLP/project/stanford-ner-2015-04-20/stanford-ner.jar')
        # r = st.tag('Rami Eid is studying at Stony Brook University in New York on Tuesday'.split())
        '''
        elif first_word_of_the_question == 'when':
            date = ''
            for i in range(0, len(r)): # i < len(r)
                if date != '':
                    break
                if r[i][1] == 'DATE':
                    date += r[i][0] + ' '
                    while (i + 1 < len(r) and r[i+1][1] == 'DATE'):
                        i += 1
                        date += r[i][0]
            #print 'date' + date
            return date
        '''


def find_the_sentence(array_of_questions, name_of_article):
    f = open("Test_Data\\"+name_of_article ,'r')
    # preprocess the article
    raw = f.read().decode('ascii', 'ignore')
    # split the article into sentences
    content = tokenize.sent_tokenize(raw)

    array_of_target_sentences = []
    for question in array_of_questions:
        fuzz_ratio = 0
        target_sentence = ""
        for item in content:
            tmp_fuzz_ratio = fuzz.partial_ratio(question,item)
            if (tmp_fuzz_ratio > fuzz_ratio):
                fuzz_ratio = tmp_fuzz_ratio
                target_sentence = item

        array_of_target_sentences.append(target_sentence)

    
    for answer in array_of_target_sentences:
        print answer
        print

    array_of_answers = []
    # Answer each question by looking at the answer sentences
    '''
    for i in range(0, len(array_of_target_sentences)):
        array_of_answers.append(find_the_answer(array_of_target_sentences[i], a[i]))
        print i
        print array_of_target_sentences[i]

    return array_of_answers
    '''

# q1 and q2 are two sample questions
q1 = "Is Chinese a branch of the Sino-Tibetan language family?"
q2 = "Is Standard Chinese based on the Beijing dialect of Mandarin?"
q3_time_question = "When can Chinese be traced back over?"

# put q1 and q2 questions into an array and pass this array into the method.
a = []
a.append(q1)
a.append(q2)
a.append(q3_time_question)

name_of_article = "Chinese_Language.txt"
find_the_sentence(a, name_of_article)
