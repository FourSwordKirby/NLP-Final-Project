"""
file: generateQuestions.py
author: Group Neizetze
python: 2.7.10

desc:
"""

import sys
sys.path.insert(0, '../Libraries')

from inc.ArticleParser import *
from inc.Questions import *

# Generates numQuestions questions about the article in fileName
def main(fileName, numQuestions):

    # parse the file
    article = simpleAugment(simpleIngest(fileName))
    print article

    # generate the questions
    questions = simpleQuestionGen(article)

    """
    # Transforms the sentences in the article into a list of questions.
    questions = articleToQuestion(article)

    # Print the best questions
    for question in bestQuestions:
        print question
    """

# Run main()
if __name__ == '__main__':
#    main(sys.argv[1], int(sys.argv[2]))
<<<<<<< HEAD:Question Generating/GenerateQuestions.py
    main("SimpleArticle.txt", 1)
=======
    main("SampleArticle.txt", 1)
>>>>>>> 769d9198ff2c84a90bbaf1e51478b482cf1c41bb:Questioning/ask.py
