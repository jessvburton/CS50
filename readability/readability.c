#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;

    // get text from user
    string text = get_string("Text: ");

    // count letters and count sentences
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }

        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }

        else if (isspace(text[i]))
        {
            words++;
        }
    }

    // calulation
    // L = average no. letters per 100 words
    float L = 100.0 * letters / words;

    // S = average no. sentences per 100 words
    float S = 100.0 * sentences / words;
    float grade = (0.0588 * L) - (0.296 * S) - 15.8;

    //print grade
    if (grade >= 1 && grade <= 16)
    {
        printf("Grade %i\n", (int) round(grade));
    }

    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }

    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
}
