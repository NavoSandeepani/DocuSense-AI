from question_answering import answer_question

text = """
Trevor, Lansford and Black published a paper in 2004.
"""

answer = answer_question(
    "What year was the paper published?",
    text
)

print(answer)