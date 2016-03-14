#usage of fuzzywuzzy: pip install git+git://github.com/seatgeek/fuzzywuzzy.git@0.10.0#egg=fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#usage of nltk: find the whl package at http://www.lfd.uci.edu/~gohlke/pythonlibs/#nltk 
from nltk import tokenize

# This script searches through an article with a question and finds the target sentence that 
# is mostly likely to contain the answer.


#q1 and q2 are two sample questions
q1 = "Is Chinese a branch of the Sino-Tibetan language family?"
q2 = "Is Standard Chinese based on the Beijing dialect of Mandarin?"

f = open("Test_Data\Chinese_Language.txt",'r')
#proprocess the article
raw = f.read().decode('utf8')
#split the article into sentences
content = tokenize.sent_tokenize(raw)

fuzz_ratio = 0
target_sentence = ""
count = 0
for item in content:
    tmp_fuzz_ratio = fuzz.partial_ratio(q1,item)
    if (tmp_fuzz_ratio > fuzz_ratio):
        fuzz_ratio = tmp_fuzz_ratio
        target_sentence = item
    count += 1

print target_sentence