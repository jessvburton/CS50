from cs50 import get_string
from cs50 import get_float

letters, words, sentences, i = 0, 1, 0, 0

text = get_string("Text: ")  # get text from user
length = len(text)

while i < length:  # count letters and count sentences
    if text[i].isalpha():
        letters += 1
    elif text[i].isspace():
        words += 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1
    i += 1

L = 100.0 * letters / words  # L = average no. letters per 100 words
S = 100.0 * sentences / words  # S = average no. sentences per 100 words
grade = round((0.0588 * L) - (0.296 * S) - 15.8)  # calulation

# print grade
if grade >= 1 and grade <= 16:
    print(f"Grade {grade}")
elif grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
