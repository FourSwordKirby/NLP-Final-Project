import nltk
from nltk.tag import pos_tag
from nltk.tokenize import  word_tokenize

vb_list = ["VBZ","VB","VBD","VBG","VBN","VBP"]

test_sentence = "Aditya likes apples. He likes to play video games too."
test_sentence_2 = "Bob likes movies and chocolates but also likes to eat alot of food as well"
test_sentence_3= "Billy is a great and wonderful man."
test_sentence_4 = "Aditya can talk in French"
test_sentence_5 = "Aditya has been a topper"
test_sentence_6 = "Aditya liked apples."
test_sentence_7 = "Bob was a bad child"


'''
Aditya likes apples ... -> Who likes apples?
Billy is a great man... -> Who is a great man?


'''

def who_rule(sentence):
	tagged = pos_tag(word_tokenize(sentence))
	tags_only = [ x[1] for x in tagged]
	words_only = [x[0] for x in tagged]
	if "NNP" not in tags_only:
		return ""
	if not (set(vb_list) & set(tags_only)):
		return ""
	vtag = list(set(vb_list).intersection(set(tags_only)))[0]
	V_index = tags_only.index(vtag)
	if(tags_only.index("NNP")+1!=V_index):
		return ""
	if "NNS" in tags_only:
		NNS_index = tags_only.index("NNS")
		return "Who "+ " ".join(words_only[V_index:NNS_index+1])+"?"
	else:
		if "NN" not in tags_only:
			return ""
		NN_index = tags_only.index("NN")
		return "Who "+ " ".join(words_only[V_index:NN_index+1])+"?"


def has_rule(sentence):
	tagged = pos_tag(word_tokenize(sentence))
	tags_only = [ x[1] for x in tagged]
	words_only = [x[0] for x in tagged]
	if "NNP" not in tags_only:
		return ""
	NNP_index = tags_only.index("NNP")
	if "has" not in words_only:
		return ""
	else:
		has_index = words_only.index("has")
		return "Has "+words_only[NNP_index]+" "+ " ".join(words_only[has_index+1:len(words_only)])+"?"

def can_rule(sentence):
	tagged = pos_tag(word_tokenize(sentence))
	tags_only = [ x[1] for x in tagged]
	words_only = [x[0] for x in tagged]
	if "NNP" not in tags_only:
		return ""
	NNP_index = tags_only.index("NNP")
	if "can" not in words_only:
		return ""
	else:
		can_index = words_only.index("can")
		return "Can "+words_only[NNP_index]+" "+ " ".join(words_only[can_index+1:len(words_only)])+"?"

# t1 =who_rule(test_sentence_7)
# print t1

# start_time = time.time()
# t1 =who_rule(test_sentence_3)
# print t1
# t2 = who_rule(test_sentence)
# print t2
# t3 = who_rule(test_sentence_2)
# print t3
# end_time = time.time()
# print end_time-start_time
