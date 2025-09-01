#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
// L=avrg letters per 100 words, S = = avrg sentences per 100 words
// index = 0.0588 * L - 0.296 * S - 15.8
// spaces + 1 = num of words
//  . ! ? = num of sentences
float compute(string text);
int main(void)
{
    string text = get_string("Text: ");

    float index = compute(text);
    if (index <= 0)
    {
        printf("Before Grade 1\n");
    }

    else if (index >= 1 && index < 16)
    {
        printf("Grade %d\n", (int) round(index));
    }

    else
    {
        printf("Grade 16+\n");
    }
}

float compute(string text)
{
    int num_letters = 0, num_words = 1, num_sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            num_letters++;
        }

        else if (text[i] == ' ')
        {
            num_words++;
        }

        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            num_sentences++;
        }
    }
    // printf("number of letters:%d\n",num_letters);
    // printf("number of words:%d\n",num_words);
    // printf("number of sentences:%d\n",num_sentences);
    float L = (float) num_letters / (float) num_words * 100;
    float S = (float) num_sentences / (float) num_words * 100;
    float index = (0.0588 * L - 0.296 * S - 15.8);
    printf("index is %f\n", index);
    // printf("L is %f\n",L);
    // printf("S is %f\n",S);
    return index;
}
