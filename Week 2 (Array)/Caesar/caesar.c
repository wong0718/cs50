#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{

    string key = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0, len = strlen(argv[1]); i < len; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int k = atoi(key);
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isupper(text[i]))
        {
            printf("%c", ((text[i]) - 65 + k) % 26 + 65);
        }

        else if (islower(text[i]))
        {
            printf("%c", ((text[i]) - 97 + k) % 26 + 97);
        }

        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
}
/*
say we have the letter ‘Z’ and a key of 3. The ASCII value of ‘Z’ is 90.

1)Subtract 65 (the ASCII value of ‘A’) to get 25, which is the position of ‘Z’ in the alphabet.
2)Add the key (3) to get 28.
3)Take modulo 26 to get 2, which is the position of the new letter in the alphabet.
4)Add 65 to get 67, which is the ASCII value of ‘C’.
*/

// void rotate(string key,string text)
// {
//     int k = atoi(key);
//     for(int i = 0, len = strlen(text); i < len;i++)
//     {
//         if (isupper(text[i]))
//         {
//             printf("%c", ((text[i]) - 65 + k) % 26 + 65);
//         }

//         else if (islower(text[i]))
//         {
//             printf("%c", ((text[i]) - 97 + k) % 26 + 65);
//         }

//         else
//         {
//             printf("%c",text[i]);
//         }
//         printf("\n");
//     }
// }
