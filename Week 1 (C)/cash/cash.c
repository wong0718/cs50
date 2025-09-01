#include <cs50.h>
#include <stdio.h>

void num_change(int change);
int change(void);
int main(void)
{
    int n = change();
    num_change(n);
}

int change(void)
{
    int n;
    do
    {
        n = get_int("Change owned: ");
    }
    while (n < 0);
    return n;
}
void num_change(int change)
{
    int count = 0;
    while (change >= 25)
    {
        change = change - 25;
        count++;
    }

    while (change >= 10)
    {
        change = change - 10;
        count++;
    }

    while (change >= 5)
    {
        change = change - 5
        count++;
    }

    while (change >= 1)
    {
        change = change - 1;
        count++;
    }
    printf("Your changes is/are %i(s) of coins\n", count);
}
