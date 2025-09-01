#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
int points[26] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 10};

int compute(string word);
int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 ff= get_string("Player 2: ");

    int score1 = compute(word1);
    int score2 = compute(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie!\n");
    }
}

int compute(string word)
{
    int scores = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
        {
            scores += points[(word[i]) - 'A'];
        }

        else if (islower(word[i]))
        {
            scores += points[(word[i]) - 'a'];
        }
    }
    return scores;
}
