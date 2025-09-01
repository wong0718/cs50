

int main(void)
{
    char c = get_char("Do you concur? y/n ");
    if (c == 'y' || c == 'Y')
     {
        printf("Ok\n");
     }
     else if(c == 'n' || c == 'N')
     {
        printf("Nope\n");
     }
}
