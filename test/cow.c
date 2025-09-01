#include <cs50.h>
#include <stdio.h>

// int main(void)
// {
//     printf("Moo"\n)
//     printf("Moo"\n)
//     printf("Moo"\n)
// }

// or
// {
//     int i = 3;
//     while (i > 0)
//     {
//         printf("moo\n");
//         i--;
//     }
// }

// better

// {
//     int i = 0;
//     while (i < 3)
//     {
//         printf("moo\n");
//         i++;
//     }
// }

// for loop
int get_positive_int(void);
void moo(int n);
int main(void)

{
    int times = get_positive_int();
    moo(times);
}

int get_positive_int(void)
{
    int n;
    do
    {
        n = get_int("Number :");
    }
    while (n < 1);
    return n;
}

// output moo input
void moo(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("moo\n");
    }
}
