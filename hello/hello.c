#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Greet user by name
    string answer = get_string("What's your name?");
    printf("Hello, %s\n", answer);
}
