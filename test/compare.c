#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x value? ");
    int y = get_int("y value? ");

    if (x < y)
    {
        printf("x is less than y\n");
    }
    else if (x > y)
    {
        printf("x is more than y\n");
    }
    else printf("x is equal to y\n");
}
