"""
file: generateQuestions.py
author: Group Neizetze
python: 2.7.10

desc:
"""

import sys
from inc.ArticleParser import ingest, augment
from inc.Questions import articleToQuestion, bestQuestion

# Generates numQuestions questions about the article in fileName
def main(fileName, numQuestions):

    # take in the file, return a dict of sentences where the key is the
    # heading and the value is the list of sentences.
    article = ingest(fileName)

    # for each sentence in sentences, form a list of augmented sentences
    for (heading, paragraph) in article.iteritems():
        article[heading] = augment(paragraph)

    # Transforms the sentences in the article into a list of questions.
    questions = articleToQuestion(article)

    # Find the top questions
    bestQuestions = bestQuestion(questions, numQuestions)

    # Print the best questions
    for question in bestQuestions:
        print question

# Run main()!
if __name__ == '__main__':
#    main(sys.argv[1], int(sys.argv[2]))
    main("SampleArticle.txt", 1)