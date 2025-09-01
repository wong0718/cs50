#include <cs50.h>
#include <stdio.h>

int height (void);
void print_brick(int height);
void print_space(int height);
int main(void)

{
    int n = height();
    print_brick(n);

}

int height (void)
{
    int n;
    do
    {
        n =  get_int("Height? 1 to 8 ");
    }
    while (n <= 0 || n > 8);
    return n;
}

void print_brick(int height)
{
    //for each row
    for(int row = 0; row < height; row++)
    {
        //for each spaces(user input n:n-1,n-2,n-3,...)
        for(int spaces = height - 1; spaces > row; spaces--)
        {
            printf(" ");
        }
        //for each brick
        for(int brick = -1; brick < row; brick++)
        {
            printf("#");
        }
        printf("  ");
        for(int brick = -1; brick < row; brick++)
        {
            printf("#");
        }
        printf("\n");
    }
}


