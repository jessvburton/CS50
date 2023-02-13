#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int a;
    do
    {
        a = get_int("Start size: ");
    }
    while (a < 9);

    // Prompt for end size
    int b;
    do
    {
        b = get_int("End size: ");
    }
    while (b <= a);

    // Calculate number of years until we reach threshold
    int y;
    for (y = 0; a < b; y++)
    {
        int c = a / 3;
        int d = a / 4;
        a = a + c - d;
    }

    // Print number of years
    printf("Years: %i\n", y);
}
