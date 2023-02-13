#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //get number
    float change;
    do
    {
        change = get_float("change: $ ");
    }
    while (change < 0);

    //change to cents and round
    int cents = round(change * 100);

    //calculate number of coins
    int coins = 0;
    while (cents >= 25)
    {
        cents = cents - 25;
        coins ++;
    }

    while (cents >= 10)
    {
        cents = cents - 10;
        coins ++;
    }

    while (cents >= 5)
    {
        cents = cents - 5;
        coins ++;
    }

    while (cents >= 1)
    {
        cents = cents - 1;
        coins++;
    }

    //print min number of coins
    printf("%i\n", coins);
}
