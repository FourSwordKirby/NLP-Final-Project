"""
file: Grammaticality.py
author: Group Neizetze
python: 2.7.10

desc: Used to judge whether a question is good or not.

depdencies:
language-check 0.8 (https://pypi.python.org/pypi/language-check)
"""

import language_check
tool = language_check.LanguageTool('en-US')

# higher numbers are worse.
def languageCheckScore(sentence):
    return len(tool.check(sentence))

""" Testing: languageCheckScore
print languageCheckScore(u'When was Lincoln born?')
print languageCheckScore(u'Who jumps over the lazy dog?')
# not ideal that it doesn't find the number error in jumps, but whatever
print languageCheckScore(u'What does the quick brown fox jumps over?')
print languageCheckScore(u'A sentence with a error in the Hitchhiker\'s Guide tot he Galaxy')
print languageCheckScore(u'What does english is a West Germanic language that was first spoken in early medieval England and is now  ?')
"""
