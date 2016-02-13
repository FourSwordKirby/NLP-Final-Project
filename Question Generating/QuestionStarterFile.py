import nltk
from pattern.en import parse

#Testing the abilities of nltk
testString = "I made a poop in my pants"

#part of speech tagging
print(nltk.pos_tag(nltk.word_tokenize(testString)))

#parse tree tests
print(parse(testString, relations=True, lemmata=True))
