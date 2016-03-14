"""
author:

    etctec
desc:
"""

import rules

# Takes in a dict of {heading : paragraph} and returns a list of questions.
def articleToQuestion(article):
    questions = [];

    for heading in article.keys() :
        paragraph = article[heading];

        for sentence in paragraph:
            new_question = rules.who_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)
                
            new_question = rules.has_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)

            new_question = rules.can_rule(sentence)
            if not (new_question == ""):
                questions.append(new_question)
 
    return questions

# Returns the top num questions in questions.
def determineBestQuestions(questions, num):
    # NYI
    return []
