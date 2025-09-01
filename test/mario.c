#include <cs50.h>
#include <stdio.h>

void print_row(int row, int col);
int get_int_row(void);
int get_int_col(void);

int main(void)

{
    int col = get_int_row();
    int row = get_int_col();
    print_row(row, col);
}

void print_row(int row, int col)
{
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

int get_int_row(void)
{
    int n;
    do
    {
        n = get_int("Row? ");
    }
    while (n < 1);
    return n;
}

int get_int_col(void)
{
    int n;
    do
    {
        n = get_int("Column? ");
    }
    while (n < 1);
    return n;
}
