#include <cs50.h>
#include <stdio.h>

long number(void);
void checksum(long number);
int main(void)
{
    long n = number();
    checksum(n);
}

long number(void)
{
    long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number <= 0);
    return number;
}

void checksum(long number)
{
    long number_copy;
    number_copy = number;
    int total_sum = 0, pos = 0, total_length = 0;
    // 1234
    // sum of 1 + 3
    // pos = 0
    // 1234 % 10 = 4, pos = 0
    // 123 % 10 = 3, pos = 1 (odd)
    // 12 % 10 = 2 pos = 2 (even)
    // 1 % 10 = 1 pos = 3
    // 0
    while (number != 0)
    {
        if (pos % 2 != 0) // if !=0,is odd
        {
            int temp = 2 * (number % 10);

            if (temp > 9)
            {
                total_sum += (temp % 10 + temp / 10);
            }
            else // <9
            {
                total_sum += temp;
            }
        }
        else // even
        {
            total_sum += number % 10;
        }
        number = number / 10;
        pos++;
        total_length++;
    }
    // printf("total sum is %d\n", total_sum);
    // printf("total length is %d\n", total_length);

    while (number != 0)
        ;
    if (total_sum % 10 == 0)
    {
        // American Express numbers start with 34 or 37, uses 15-digit number
        // MasterCard numbers start with 51, 52, 53, 54, or 55, uses 16-digit numbers
        // Visa numbers start with 4, uses 13- and 16-digit numbers.
        long amex_start = number_copy / 10000000000000;
        long mastercard_start = number_copy / 100000000000000;
        long visa_start = number_copy / 1000000000000;
        if ((amex_start == 34 || amex_start == 37) && total_length == 15)
        {
            printf("AMEX\n");
        }


        else if ((mastercard_start >= 51 && mastercard_start <= 55) && total_length == 16)
        {
            printf("MASTERCARD\n");
        }
        // printf("amex start is %ld\n", amex_start);
        // printf("visa start is %ld\n", visa_start);
        // printf("mastercard start is %ld\n", mastercard_start);


        else if ((total_length == 13 || total_length == 16) &&
                 (visa_start == 4 || mastercard_start / 10 == 4))
        {
            printf("VISA\n");
        }


        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
