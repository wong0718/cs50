// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

unsigned int word_counter = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hash_value = hash(word);
    node *cursor = table[hash_value];

    // Go through linked list
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }

        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0;i < strlen(word);i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    for (int i = 0;i < N;i++)
    {
        table[i] = NULL;
    }

    // Open Dictionary
    FILE *file = fopen(dictionary,"r");

    // Fail-safe
    if (file == NULL)
    {
        printf("Unable to open %s\n",dictionary);
        return false;
    }

    // Declare var
    char buffer [LENGTH];

    // Scan dictionary for strings up until eof
    while (fscanf(file,"%s",buffer) != EOF)
    {
        // Allocate memory for new node
        node *new_word = malloc (sizeof(node));

        // Hash word to obtain hash value
        int hash_value = hash(buffer);

        // Insert node into hash table at that location
        strcpy(new_word -> word,buffer);
        new_word -> next = table[hash_value];
        table[hash_value] = new_word;
        word_counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0;i < N;i++)
    {
        // Set cursor to the start of the linked list
        node *tmp = table[i];
        node *cursor = table[i];

        // if node != NULL,free memory
        while (cursor != NULL)
        {
            cursor = cursor -> next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
