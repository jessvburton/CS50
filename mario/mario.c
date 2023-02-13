#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt for height
    int h, s, c, r;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    //calculate width/row
    for (r = 0; r < h; r++)

    {
        //space
        for (s = 0; s < h - r - 1; s++)
        {
            printf(" ");
        }

        //# left
        for (c = 0; c <= r; c++)
        {
            printf("#");
        }

        // middle gap
        printf("  ");

        //# right
        for (c = 0; c <= r; c++)
        {
            printf("#");
        }
        printf("\n");
    }
}
