import os
import nltk 
import difflib
import re
import itertools
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordNERTagger, StanfordPOSTagger
from nltk.stem.wordnet import WordNetLemmatizer

os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_45/bin'  #or your java path
os.environ['CLASSPATH'] = 'C:/Users/Aditya/Desktop/parser/stanford-parser-full-2015-04-20/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'C:/Users/Aditya/Desktop/parser/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar' 
st = StanfordNERTagger('C:/Users/Aditya/Desktop/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz',
               'C:/Users/Aditya/Desktop/stanford-ner-2015-04-20/stanford-ner.jar')
pos = StanfordPOSTagger('C:/Users/Aditya/Desktop/stanford-postagger-2015-04-20/models/english-bidirectional-distsim.tagger',
	'C:/Users/Aditya/Desktop/stanford-postagger-2015-04-20/stanford-postagger-3.5.2.jar')
parser = StanfordParser(model_path="C:/Users/Aditya/Desktop/parser/stanford-parser-full-2015-04-20/englishPCFG.ser.gz")

pattern_uppercase = re.compile('[A-Z]{2,}')
pattern_parens = re.compile('[()]')


wordnet_lemmatizer = WordNetLemmatizer()


auxillary_words = ["be","am","are","is","was","were","being","been","can","could","dare","do","does","did","have","has","had","having","may","might","must","need","ought","shall","should","will","would"]
verb_tags = ["VBZ","VB","VBG"]

sample_question = "What does Aditya like to read?"
sample_likely_sentence = "Aditya likes bowling and reading comic books."

sample_question2 = "What are the national languages of Singapore?"
sample_likely_sentence2= "The national languages of Singapore are Spanish and English."

sample_question3 = "What are the national languages of Singapore?"
sample_likely_sentence3= "The national languages of Singapore are Spanish,Swedish,English and Spanish."






'''
Takes as input the str of an element of a list produced by collect_ADJP_phrases
and collect_NP_phrases and strips out unecessary symbols/ parentheses/ spaces

'''
def extract_string(string):
	string = pattern_uppercase.sub('',string)
	string = pattern_parens.sub('',string)
	string = re.sub('\s+', ' ',string).strip()
	string = re.sub(' , , ',',',string)
	return string

'''

Attempt to find all "ADJP" phrases in the parse tree

'''


def collect_ADJP_phrases(raw_parse):
	if(raw_parse.label()=="ADJP"):
		return [raw_parse]
	else:
		try:
			a = collect_ADJP_phrases(raw_parse[0])
		except:
			a = []
		try:
			b = collect_ADJP_phrases(raw_parse[1])
		except:
			b = []
		try:
			c = collect_ADJP_phrases(raw_parse[2])
		except:
			c= []
		try:
			d= collect_ADJP_phrases(raw_parse[3])
		except:
			d= []	
		return a+b+c+d

'''

Attempt to find all "NP" phrases in the parse tree

'''


def collect_NP_phrases(raw_parse):
	if(raw_parse.label()=="NP"):
		return [raw_parse]
	else:
		try:
			a = collect_NP_phrases(raw_parse[0])
		except:
			a = []
		try:
			b = collect_NP_phrases(raw_parse[1])
		except:
			b = []
		try:
			c = collect_NP_phrases(raw_parse[2])
		except:
			c= []
		try:
			d= collect_NP_phrases(raw_parse[3])
		except:
			d= []	
		return a+b+c+d

#print (list(parser.raw_parse("What is the national language of Singapore?")))[0]
#print (list(parser.raw_parse(sample_likely_sentence3)))[0]
#print (list(parser.raw_parse(sample_likely_sentence2)))[0]
#c  = collect_NP_phrases((list(parser.raw_parse(sample_likely_sentence)))[0])
#for e in c:
#	print extract_string(str(e))


'''

Finds the closest "phrase" that occurs after the "target word" passed in. 

I.e if the sentence is  "Aditya like reading books" and the target word passed in "reading" and
the list of phrases contains "books", then "books will be returned"

'''

def closest_phrase(string, target_word, list_of_phrases):
	target_index = string.index(target_word)
	min_diff = 10000
	closest_phrase = ''
	for phrase in list_of_phrases:
		temp_diff = string.index(phrase) - target_index
		if(temp_diff > 0 and temp_diff < min_diff):
			min_diff = temp_diff
			closest_phrase = phrase
	return closest_phrase



'''
Attempts to answer "What" questions based on question string and the sentence determined to most likely contain
the answer.

So far able to handle two type of "What" questions

1) "What does Aditya like to read?" (sentence ends with a verb) -> find NP in answer sentence closest to verb in sentence
2) "What is the language of Singapore"? ('is' is second word and question has one NP) -> match NP in answer sentence and try to find ADJP next to
	matched NP. if no ADJP present then return closest NP in answer sentence


'''

def answerWhatQuestion(question_string,likely_sentence_string):
	question_string_tokenized = nltk.word_tokenize(question_string)
	likely_sentence_string_tokenized = nltk.word_tokenize(likely_sentence_string)

	question_string_pos_tagged =  pos.tag(question_string_tokenized)
	get_noun_phrases_in_question_raw = collect_NP_phrases((list(parser.raw_parse(question_string)))[0])
	noun_phrases_in_question = [extract_string(str(e)) for e in get_noun_phrases_in_question_raw]

	likely_sentence_string_pos_tagged = pos.tag(likely_sentence_string_tokenized)
	get_noun_phrases_in_likely_sentence_raw = collect_NP_phrases((list(parser.raw_parse(likely_sentence_string)))[0])
	noun_phrases_in_likely_sentence = [extract_string(str(e)) for e in get_noun_phrases_in_likely_sentence_raw]

	if(question_string_pos_tagged[len(question_string_pos_tagged)-2][1] in verb_tags):
		question_has_verb_at_end = True
	else:
		question_has_verb_at_end = False
	if question_has_verb_at_end:
		verb_at_end_of_question = question_string_pos_tagged[len(question_string_pos_tagged)-2][0]
		
		verbs_in_likely_sentence = [elem[0] for elem in likely_sentence_string_pos_tagged if elem[1] in verb_tags]
		target_verb = ''
		for verb in verbs_in_likely_sentence:
			if(wordnet_lemmatizer.lemmatize(verb,'v') == wordnet_lemmatizer.lemmatize(verb_at_end_of_question,'v')):
				target_verb = verb
		if(target_verb==''):
			return noun_phrases_in_likely_sentence[0]
		answer = closest_phrase(likely_sentence_string,target_verb, noun_phrases_in_likely_sentence)
		return answer
	if(question_string_tokenized[1] in auxillary_words and len(noun_phrases_in_question)==1):
		np_found_in_likely_sentence_index = -1
		for x in xrange(len(noun_phrases_in_likely_sentence)):
			if(noun_phrases_in_likely_sentence[x].lower()==noun_phrases_in_question[0].lower()):
				np_found_in_likely_sentence_index = x
		if(np_found_in_likely_sentence_index==-1):
			return noun_phrases_in_likely_sentence[0]
		get_ADJP_phrases_in_likely_sentence = collect_ADJP_phrases((list(parser.raw_parse(likely_sentence_string)))[0])
		ADJP_phrases_in_likely_sentence = [extract_string(str(e)) for e in get_ADJP_phrases_in_likely_sentence]
		if(len(ADJP_phrases_in_likely_sentence)>0):
			answer = closest_phrase(likely_sentence_string,noun_phrases_in_likely_sentence[np_found_in_likely_sentence_index],ADJP_phrases_in_likely_sentence)
		else:
			target_phrase = noun_phrases_in_likely_sentence[np_found_in_likely_sentence_index]
			noun_phrases_in_likely_sentence.remove(noun_phrases_in_likely_sentence[np_found_in_likely_sentence_index])
			answer = closest_phrase(likely_sentence_string,target_phrase,noun_phrases_in_likely_sentence)
		return answer


		


c = answerWhatQuestion(sample_question,sample_likely_sentence)
print c
c2 = answerWhatQuestion(sample_question2,sample_likely_sentence2)
print c2
c3 = answerWhatQuestion(sample_question3,sample_likely_sentence3)
print c3