from cs50 import get_string
import math

def main():
    text = get_string("Text: ")
    index =compute(text)

    if index <= 0:
        print("Before Grade 1")

    elif 1 <= index < 16:
        print(f"Grade {round(index)}")

    else:
        print("Grade 16+")

def compute(text):
    num_letters = num_sentences = 0
    num_words = 1
    for char in text:
        if char.isalpha():
            num_letters += 1
        if char in " ":
            num_words += 1
        if char in ".!?":
            num_sentences += 1

    L = num_letters / num_words * 100
    S = num_sentences / num_words * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return index

if __name__ == "__main__":
    main()
