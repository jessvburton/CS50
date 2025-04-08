#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // check command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int arg_length = strlen(argv[1]);    //to get the length of string in command line argument
    for (int i = 0; i < arg_length; i++)  //iterate through the length of the argv[1]
    {
        if (!isdigit(argv[1][i]))  //to check if character in argv[1] is not digit
        {
            printf("Usage: ./caesar key");  //if not print this //
            return 1;
        }
    }

    // get text and change to int
    string text = get_string("plaintext: ");
    int k = atoi(argv[1]);

    printf("ciphertext: ");

    if (k < 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0, n = strlen(text); i < n; i++)
        {
            // use formula ci = (pi + k) % 26
            if islower(text[i])
            {
                printf("%c", (((text[i] + k) - 97) % 26) + 97);
            }

            else if isupper(text[i])
            {
                printf("%c", (((text[i] + k) - 65) % 26) + 65);
            }
        }
        // print new line
        printf("\n");
        return 0;
    }
}
