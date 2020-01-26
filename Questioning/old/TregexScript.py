import nltk
import os
import subprocess
import shlex


# Takes a list of sentences, a pattern and runs them through the trgex.sh file to see if there are any matches. Returns an integer list where each integer
# indicates the index of the sentence in the sentence list which matches the pattern. IMPORTANT: zero indexing is not in effect here i.e "1" in list implies
# the first sentence in the list matched the pattern

from stat_parser import Parser
parser = Parser()
pattern = "NP < (NP=np < NNS) < (NP=np1 < NN)"
pattern2 = "SQ < ((VBZ $ VBZ)$+NP)  "

#the Yes/No pattern should transform the sentence based on the appearance of the first "main" verb

sentence_list = ["People yawn due to lack of sleep", "I will complete the assignment", "They are incredible", "The student who will be praised is yawning"]

f = open('sentencetrees','w')
for x in xrange(len(sentence_list)):
	f.write(str(parser.parse(sentence_list[x]))+'\n')
f.close()

#note change this to where ever the actual tregex script is located
proc = subprocess.Popen(['sh','../Libraries/tregex/tregex.sh','-n',pattern2,'sentencetrees'], stdout=subprocess.PIPE)
tmp = proc.stdout.read()
print [int(s) for s in tmp if s.isdigit()]


