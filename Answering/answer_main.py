"""
file: answer_main.py
author: Group Neizetze
python: 2.7.10

desc:
"""

import sys
import re

from fuzzywuzzy import fuzz
#from inc.ArticleParser import *
#from inc.Questions import *
#from inc.binary import *

import inc.binary
#import inc.what
import inc.who
import inc.where
import reconcile
from nltk import tokenize

THRESHOLD_VALUE = 50

def find_the_answer(question, target_sentence):
    # |array_of_questions| <= |array_of_target_sentences|
    # Classify the questions ---. what, where, who, how, why, binary
    binary_question_keywords = ["be","am","are","is","was","were","being","been","can","could",
    "dare","do","does","did","have","has","had","having","may","might","must","need","ought","shall","should","will","would"]
    # wh_question_keywords = ['who','where','what','when','how','why','which']
    wh_question_keywords = ['who','where','what']

    # As long as the question contains a wh word, it is classified as a WH-question
    # for i in range(0, len(array_of_questions)):
    #question =  array_of_questions[i]
    #target_sentence = array_of_target_sentences[i]

    answer = ''
    for wh_word in wh_question_keywords:
        if wh_word in question:
            # It is a WH-question
            '''
            if wh_word == 'what':
                ###

                answer = inc.what.answerWhatQuestion(question, target_sentence)
                
                array_of_answers.append(answer)
                #array_of_answers.append(answer)
                break
            '''
            if wh_word == 'who':
                ###
                try:
                    answer = inc.who.find_who_question_answer(question, target_sentence)
                except:
                    answer = None
                return answer

            elif wh_word == 'where':
                ###
                try:
                    answer = inc.where.find_where_question_answer(question, target_sentence)
                except:
                    answer = None
                return answer

            #elif wh_word == 'when':
                ###
            #elif wh_word == 'why':
                ###
            #elif wh_word == 'which':
        
        # It is a binary question
        #answer = inc.binary.find_binary_question_answer(question, target_sentence)
        #array_of_answers.append(answer)
    #answer = inc.where.find_where_question_answer(question, target_sentence)
    #answer = inc.what.answerWhatQuestion(question, target_sentence)
    #print answer
    #answer = inc.what.answerWhatQuestion(question, target_sentence)
    #print answer

    
    


def main(fileName, numQuestions):

    f_fileName = open(fileName,'r')
    # Filter out some characters that cannot be printed in the console
    f_fileName_read = f_fileName.read()
    
    raw_file = f_fileName_read.lower().decode('ascii','ignore')
    raw_file2 =f_fileName_read.decode('ascii','ignore')
    #raw_file = (f_fileName.read()).lower().decode('ascii', 'ignore')
    
    f_numQuestions = open(numQuestions, 'r')
    raw_question = (f_numQuestions.read()).lower().decode('ascii', 'ignore').split('\n')
    
    # Build a dictionary that stores a question and all the possible sentences from the article (based on the Fuzzywuzzy score)
    #question_all_answer_sentences_dic = {}
    list_of_all_the_questions = []

    # Add each question to the dictionary
    # So that we could map each question to all of its candidate answer sentences and the Fuzzywuzzy matching score of the candidate answer sentence
    # e.x. "What is Michael's job?" --->  {"Teacher" : 60, "Driver" : 70, "Student" : 80}
    # Will set the threshold value for the score to be 50
    for question in raw_question:
        list_of_all_the_questions.append(question)
   
    # Split the article into sentences
    content = tokenize.sent_tokenize(raw_file)

    # Get rid of unwanted spaces
    for i,s in enumerate(content):
        content[i] = re.sub(r'([A-Za-z0-9 ]+\s{2,})','',s)

    # We assume that target sentence contaisn the answer we're looking for
    # Find the target sentences and store them into a list
    #array_of_target_sentences = []
    count = 1
    for question in list_of_all_the_questions:
        print count
        count += 1
    # for question in array_of_questions:
        highest_fuzz_ratio = 0
        highest_score_sentence = ''

        # Create a boolean to track whether or not a valid answer is found
        #has_a_valid_answer = False

        # create a dictionary to store all the qualified sentences and their scores
        dictionary_of_qualified_sentences = {}
        for sentence_from_the_article in content:

            tmp_fuzz_ratio = fuzz.token_set_ratio(question,sentence_from_the_article)
            
            if (tmp_fuzz_ratio > THRESHOLD_VALUE):
                dictionary_of_qualified_sentences[sentence_from_the_article] = tmp_fuzz_ratio
                # As long as the sentence passes the THRESHOLD_VALUE
                # Store this sentences into the dictionary as well as its Fuzzuwuzzy score

            # Need to remember the sentence wit the highest score just in case that none of the sentences pass the THRESHOLD_VALUE
            if (tmp_fuzz_ratio > highest_fuzz_ratio):

                highest_fuzz_ratio = tmp_fuzz_ratio
                highest_score_sentence = sentence_from_the_article 

        # Sort the dictionary in a descending order
        dictionary_of_qualified_sentences = sorted(dictionary_of_qualified_sentences.items(), key=lambda x: x[1])

        has_a_valid_answer = False
        for sentence_score_pair in dictionary_of_qualified_sentences:
            
            qualified_sentence = sentence_score_pair[0]
            possible_answer = find_the_answer(question, qualified_sentence)
            if possible_answer != None:
                print possible_answer
                has_a_valid_answer = True
                break
        
        if has_a_valid_answer == False:
            # Be here when there is no valid answer
            print '***************************************'
            print highest_score_sentence.replace('\n', ' ')
        else:
            continue
    

    

# Run main() when it is directly run by the terminal
if __name__ == '__main__':
    fileName = sys.argv[1]
    numQuestions = sys.argv[2]
    main(fileName, numQuestions)