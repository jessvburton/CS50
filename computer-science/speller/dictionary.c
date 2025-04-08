// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include "dictionary.h"
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Number of buckets in hash table
const unsigned int N = 50; // this number can be changed to have more buckets, 26 is the number of letters in alphabet

// Hash table
node *table[N];
int dict_size = 0;

// Returns true if word is in dictionary, else false
// Needs to be case insensitive
bool check(const char *word)
{
    int hash_value = hash(word); //hash word to hash value

    node *n = table[hash_value]; //access linked list at that index

    while (n != NULL) //traverse linked list (strcasecmp)
    {
        if (strcasecmp(word, n -> word) == 0) //keep -> untill you reach NULL
        {
            return true; // in dictionary
        }
        n = n->next;
    }
    return false; // not in dictionary
}

unsigned int hash(const char *word)
// SOURCE: djb2 by Dan Bernstein (http://www.cse.yorku.ca/~oz/hash.html)
// hash function adapted from the above source
{
    {
        unsigned long hash = 5381;
        int c = *word;
        c = tolower(c);

        while (*word != 0)
        {
            hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
            c = *word++;
            c = tolower(c);
        }
        return hash % N; // use % n to get a value in the appropriate range
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r"); // opens dictionary file
    if (file == NULL) // if file NULL returns false
    {
        return false;
    }
    char next_word[LENGTH + 1];
    // Read strings from file one line at a time
    while (fscanf(file, "%s", next_word) != EOF) // repeat until it returns EOF
    {
        // Create a new node for each word
        node *n = malloc(sizeof(node)); // assign memory
        if (n == NULL) // check if return value is NULL
        {
            return false;
        }

        strcpy(n->word, next_word); // Copy word into node using strcpy

        int hash_value = hash(next_word); // hash word to obtain a hash value

        // insert node into hash table at that location (array of linked lists)
        n->next = table[hash_value];
        table[hash_value] = n;
        dict_size++;
    }
    fclose(file); // close file
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n != NULL)
        {
            node *tmp = n;
            n = n -> next;
            free(tmp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}