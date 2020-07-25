#include <stdio.h>
#include <stdlib.h>

struct node {
    unsigned int digits6;
    struct node *next;
};

typedef struct node Longint;

#define MAXARRAYSIZE 1000000 // Used to be 920553. I'm sure that had some significance.
#define SIZE 1 << 10
int numarray[MAXARRAYSIZE];

void init_array(int array[], size_t size)
{
    for (int index = 0; index < size; index++) {
        array[index] = 0;
        if (!(index + 1) % 10000)
            printf("Initialized %d out of %zu array elements", index + 1, size);
    }
}

Longint *make_new_node(int digits)
{
    Longint *end = malloc(sizeof(Longint));
    if (end == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }
    end->digits6 = digits;
    end->next = NULL;
    return end;
}

void free_and_return(Longint *lnum, int failed)
{
    while (lnum) {
        Longint *lnext = lnum->next;
        free(lnum);
        lnum = lnext;
    }
    exit(failed);
}

void power_of_333667(Longint *lnum)
{
    int prevcarry = 0;
    int carry;
    while (1) {
        /* int digits = lnum->digits6; //maxvalue = 999999
        digits *= 501; //maxvalue = 500999499
        int carry = digits / 1000000; //maxvalue = 500
        digits %= 1000000; //maxvalue = 999999
        digits *= 666, carry *= 666; //maxvalues = 665999334, 333000
        carry += digits / 1000000; //maxvalue = 333665
        digits %= 1000000; //maxvalue = 999999
        digits += lnum->digits6; //maxvalue = 1998999
        if (digits > 1000000) digits -= 1000000, /* maxvalue = 998999 if it gets here, 999999 otherwise */ /* carry++; /* maxvalue = 333666 */
        /* digits += prevcarry; //maxvalue = 1333665
        if (digits > 1000000) digits -= 1000000, /* maxvalue = 333665 if it gets here, 999999 otherwise */ /* carry++; /* maxvalue = 333666 */
        long long int digits = (long long int) lnum->digits6 * 333667;
        digits += prevcarry;
        carry = digits / 1000000;
        digits %= 1000000;
        lnum->digits6 = (int) digits;
        if (lnum->next == NULL) {
            if (carry != 0) {
                lnum->next = make_new_node(carry);
                if (lnum->next == NULL)
                    free_and_return(lnum, 1);
            }
            return;
        }
        prevcarry = carry;
        lnum = lnum->next;
    }
}

int zeroes_at_begin(int digits)
{
    /* int digits_copy = digits;
    int zeroes = 6;
    while (digits_copy != 0) {
        digits_copy /= 10;
        zeroes -= 1;
    } */
    /* char* digitstring = malloc(7 * sizeof(char));
    int index;
    /* for (index = 0; index < zeroes; index++) digitstring[index] = '0'; */
    /* for (index = 5; index <= 0; index--, digits /= 10) digitstring[index] = '0' + (char) (digits % 10);
    digitstring[6] = '\0';
    printf("digitstring is %s\n", digitstring);
    return digitstring; */
    int numzeroes = 6;
    while (digits) {
        digits /= 10;
        numzeroes--;
        // Remember, the only case where it prints 0s at the beginning is if the number itself is 0.
    }
    return numzeroes;
}

int main(void)
{
    char buf[SIZE];

    printf("What number do you want to take 333667 to the power of? ");
    fgets(buf, SIZE, stdin);
    int exp = atoi(buf);
    if (exp < 0) {
        printf("Cannot do negative numbers. Exiting.\n");
        return 1;
    }
    if (exp > 1000000) {
        printf("Exponent too big (must be 10^6 or less).\n");
        return 1;
    }
    Longint *ppower = make_new_node(1);
    if (ppower == NULL)
        free_and_return(ppower, 1);

    for (int iter = 0; iter < exp; iter++) {
        power_of_333667(ppower);
        if ((iter - 1) % 10000 == 0)
            printf("Multiplied by 333667 %d times out of %d.\n", iter - 1, exp);
    }

    init_array(numarray, MAXARRAYSIZE);
    Longint *ppower_copy = ppower;
    int index = 0;
    printf("Printing digits to array...\n");
    while (ppower_copy != NULL) {
        numarray[index] = ppower_copy->digits6;
        ppower_copy = ppower_copy->next;
        index++;
    }
    index -= 1;

    int latest = index;
    FILE *pow_file = fopen("power.txt", "w");

    // At the beginning, we don't want to print, say, "012345" instead of "12345"
    for (; index >= 0; index--) {
        if (!(index + 1) % 10000)
            printf("Printing digits to file - %d left\n", 6 * (index + 1));

        int chunk = numarray[index];
        if (index != latest) {
            int numzeroes = zeroes_at_begin(chunk);
            while (numzeroes != 0) {
                fprintf(pow_file, "%d", 0);
                numzeroes--;
            }
        }
        fprintf(pow_file, "%d ", chunk);
        fflush(pow_file);
    }
    fclose(pow_file);
    printf("All done!!! Open power.txt to see 333667^%d.\n", exp);

    free_and_return(ppower, 0);
}
