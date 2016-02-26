"""
file: generateQuestions.py
author: Group Neizetze
python: 2.7.10

desc:
"""

import sys
from inc.ArticleParser import *

# Generates numQuestions questions about the article in fileName
def main(fileName, numQuestions):

    # Not going to validate arguments.
    articleFile = open(fileName, 'r')

    # NYI
    print asfd()

    # Clean up.
    articleFile.close()

# Run main()!
if __name__ == '__main__':
#    main(sys.argv[1], int(sys.argv[2]))
    main("SampleArticle.txt", 1)