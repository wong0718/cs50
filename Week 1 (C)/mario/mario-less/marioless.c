#include <cs50.h>
#include <stdio.h>

int height(void);
void print_brick(int height);
void print_space(int height);
int main(void)

{
    int h = height();

    for (int i = 0; i < h; i++)
    {
        print_brick(i + 1);
    }
}

int height(void)
{
    int n;
    do
    {
        n = get_int("Height? 1 to 8 ");
    }
    while (n <= 0 || n > 8);
    return n;
}
void print_brick(int height)
{

    for (int j = 8; j > height; j--)
    {
        printf(" ");
    }

    for (int i = 0; i < height; i++)
    {
        printf("#");
    }

    printf("  ");

    for (int k = 0; k < height; k++)
    {
        printf("#");
    }

    printf("\n");
}

// int main() {
//     // Declaring and initializing multiple variables in the for loop's initialization clause
//     for (int i = 0, j = 10; i < 5; i++, j--) {
//         printf("i = %d, j = %d\n", i, j);
//     }
//     return 0;
// }
