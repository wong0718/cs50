#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void to_upper(char *s);
int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    to_upper(key);
    for (int i = 0, len = strlen(argv[1]); i < len; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < len; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("Key must not contain repeated characters\n");
                return 1;
            }
        }
    }
    string text = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                printf("%c", toupper(key[text[i] - 65]));
            }
            else if (islower(text[i]))
            {
                printf("%c", tolower(key[text[i] - 97]));
            }
            else
            {
                printf("%c", text[i]);
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
}

void to_upper(char *s)
{
    int len = strlen(s);

    for (int i = 0; i < len; i++)
        s[i] = toupper(s[i]);
}
