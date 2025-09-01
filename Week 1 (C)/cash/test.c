#include <cs50.h>
#include <stdio.h>
long number(void);
void checksum(long input);
int main(void)
{
    long n = number();
    checksum(n);
}

long number(void)
{
    long n;
    do
    {
        n = get_long("Number: ");
    }
    while (n <= 0);
    return n;
}

void checksum(long number)
{
    int total_sum = 0, pos = 0;
    while (number != 0)
    {

        if (pos % 2 != 0)
        { // Every other digit (odd)

            int temp = 2 * (number % 10);

            if (temp > 9)
            {

                total_sum += (temp % 10 + temp / 10); // 12 1+2
            }
            else
            {

                total_sum += temp;
            }
        }
        else
        {

            total_sum += number % 10;
        }
        number = number / 10;
        pos++;
    }
    printf("%d\n",total_sum);
}
