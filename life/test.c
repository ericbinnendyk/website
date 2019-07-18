#include <stdio.h>
#include <stdlib.h>

int main(void) {
        int **double_array = malloc(5 * sizeof(int));
        for (int i = 0; i < 5; i++) {
                double_array[i] = malloc(4 * sizeof(int));
                int *this_one = double_array[i];
                for (int j = 0; j < 4; j++)
                        this_one[j] = i * j;
        }
        printf("Two times Three is %d.\n", double_array[2][3]);
        int new_double_array[2][3] = {{1, 2, 3}, {2, 4, 6}};
        printf("2 times 3 is also %d.\n", new_double_array[1][2]);
        //The garbage command!
        for (int i = 0; i < 6; i++)
                printf("%d\n", double_array[0][i]);
        for (int i = 0; i < 6; i++)
                printf("%d\n", new_double_array[0][i]);
        return 0;
}
