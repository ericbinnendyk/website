/*
 * File: life.c
 * Author: Eric Binnendyk
 * Date: 9/8/14
 * This program runs Conway's Game of Life.
 */

#include <stdio.h>
#include "simpio.h"
#include "Strlib.h"

#define boardCols 50
#define boardRows 50
#define true 1
#define false 0

/* FillArrayWithFalse */
/* This function gets a boolean array and two variables, x and y (named "cols"
 * and "rows" in the program), and fills the first x columns and y rows with
 * the boolean value FALSE.
 */
void FillArrayWithFalse(bool array[boardCols][boardRows], int cols, int rows)
{
    int row, col;
    for (col = 0; col < cols; col++)
    {
        for (row = 0; row < rows; row++)
        {
            array[col][row] = false;
        }
    }
}

/* NumNeighbors */
/* Given a boolean array, a board that takes up the first (col) columns and
 * (row) rows, and an element specified by a row and column, this function
 * counts the elements with value TRUE in the given element's Moore
 * neighborhood, and returns the neighbor count.
 * The Moore neighborhood of a given cell is the set of all the cells touching
 * it orthogonally or diagonally. In this case, each cell is an element in the
 * first (col) columns and (row) rows of the array.
 */
int NumNeighbors(bool array[boardCols][boardRows], int col, int row, int cols, int rows, bool wrapAround)
{
    int count = 0;  /* return value */
    int loColIter = (!wrapAround && col == 0) ? 0 : col - 1;
    int hiColIter = (!wrapAround && col == cols - 1) ? cols - 1 : col + 1;
    int loRowIter = (!wrapAround && row == 0) ? 0 : row - 1;
    int hiRowIter = (!wrapAround && row == rows - 1) ? rows - 1 : row + 1;
    int neighborCol, neighborRow;
    for (neighborCol = loColIter; neighborCol <= hiColIter; neighborCol++)
    {
        for (neighborRow = loRowIter; neighborRow <= hiRowIter; neighborRow++)
        {
            if (neighborCol != col || neighborRow != row)
            {
                if (wrapAround)
                {
                    int wrapCol = neighborCol;
                    if (neighborCol < 0) wrapCol = neighborCol + cols;
                    else if (neighborCol >= cols) wrapCol = neighborCol - cols;
                    
                    int wrapRow = neighborRow;
                    if (neighborRow < 0) wrapRow = neighborRow + rows;
                    else if (neighborRow >= rows) wrapRow = neighborRow - rows;
                    
                    if (array[wrapCol][wrapRow]) count++;
                } else if (array[neighborCol][neighborRow]) count++;
            }
        }
    }
    return count;
}

/* CopyArray */
/* Given two boolean arrays, array1 and array2, and two variables, x and y
 * (named "cols" and "rows" in the program), this function copies the values of
 * the elements in the first x columns and y rows of array1 to the first x
 * columns and y rows of array2.
 */
void CopyArray(bool array1[boardCols][boardRows], bool array2[boardCols][boardRows], int cols, int rows)
{
    int col, row;
    for (col = 0; col < cols; col++)
    {
        for (row = 0; row < rows; row++)
        {
            array2[col][row] = array1[col][row];
        }
    }
}

/* NextGen */
/* Given a boolean array, and two variables, x and y (named "cols" and "rows" in
 * the program), this function calculates the next generation of the pattern
 * on the first x columns and y rows of the array, with FALSE representing dead
 * cells and TRUE representing live cells.
 */
void NextGen(bool array[boardCols][boardRows], int cols, int rows, bool wrapAround)
{
    bool nextGenArray[boardCols][boardRows];
    CopyArray(array, nextGenArray, cols, rows);
    int col, row;
    for (row = 0; row < rows; row++)
    {
        for (col = 0; col < cols; col++)
        {
            int neighbors = NumNeighbors(array, col, row, cols, rows, wrapAround);
            if (array[col][row])
            {
                if (neighbors != 2 && neighbors != 3) nextGenArray[col][row] = false;
            } else
            {
                if (neighbors == 3) nextGenArray[col][row] = true;
            }
        }
    }
    CopyArray(nextGenArray, array, cols, rows);
}

/* DrawGrid */
/* This function gets a boolean array and two variables, x and y (named "cols"
 * and "rows" in the program), and draws a board from the first x rows and y
 * columns, based on the fact that FALSE values represent dead cells and TRUE
 * values represent live cells. When the board is drawn, hyphens mean dead cells
 * (FALSE values) and asterisks mean live cells (TRUE values).
 */
void DrawGrid(bool array[boardCols][boardRows], int cols, int rows)
{
    int row, col;
    for (row = 0; row < rows; row++)
    {
        for (col = 0; col < cols; col++)
        {
            printf(array[col][row] ? "*" : "-");
        }
        printf("\n");
    }
    printf("\n");
}

/* This function asks the user whether they want a wrap-around grid, asks them
 * how many generations they want the pattern to run, and then draws the board
 * for each generation according to the rules specified, as well as displaying
 * the generation number.
 */
void Run(bool array[boardCols][boardRows], int cols, int rows)
{
    printf("Do you want the pattern on a wrap-around grid (y/n)? ");
    bool wrapAround = false;
    while (true)
    {
        string answer = ConvertToLowerCase(GetLine());
        char firstChar = IthChar(answer, 0);
        if (firstChar == 'y')
        {
            wrapAround = true;
            break;
        } else if (firstChar == 'n')
        {
            wrapAround = false;
            break;
        } else
        {
            printf("I do not understand your answer.\n");
            printf("Try again: ");
        }
    }
    printf("How many generations do you want the pattern to run? ");
    int numGens = GetInteger();
    int gen;
    for (gen = 1; gen <= numGens; gen++)
    {
        NextGen(array, cols, rows, wrapAround);
        printf("Generation %d\n", gen);
        DrawGrid(array, cols, rows);
        printf("Press Enter to go to next generation.\n");
        GetLine();
    }
}

/* GetPattern */
/* This function gets a pattern, either by having the user enter the coordinates
 * of the cells, or by having the user enter the name of a pre-defined pattern
 * and then placing it in the middle of the board.
 */
void GetPattern(bool array[boardCols][boardRows], int cols, int rows)
{
    FillArrayWithFalse(array, cols, rows);
    printf("\nNow set up the pattern.\n");
    printf("Enter one of the following preset patterns,\n");
    printf("or enter the coordinates of each cell in the pattern.\n");
    printf("Blinker\n");
    printf("Caterer\n");
    printf("Glider\n");
    printf("HWSS\n");
    printf("LWSS\n");
    printf("MWSS\n");
    printf("R-pentomino\n");
    printf("Traffic light\n");
    printf("\nEnter pattern name or coordinate (x, y): ");
    string entry = ConvertToLowerCase(GetLine());
    int midCol = cols / 2;
    int midRow = rows / 2;
    while (!StringEqual(entry, ""))
    {
        if (StringEqual(entry, "blinker"))
        {
            array[midCol - 1][midRow] = true;
            array[midCol][midRow] = true;
            array[midCol + 1][midRow] = true;
            break;
        } else if (StringEqual(entry, "caterer"))
        {
            array[midCol - 2][midRow - 3] = true;
            array[midCol - 4][midRow - 2] = true;
            array[midCol][midRow - 2] = true;
            array[midCol + 1][midRow - 2] = true;
            array[midCol + 2][midRow - 2] = true;
            array[midCol + 3][midRow - 2] = true;
            array[midCol - 4][midRow - 1] = true;
            array[midCol][midRow - 1] = true;
            array[midCol - 4][midRow] = true;
            array[midCol - 1][midRow + 1] = true;
            array[midCol - 3][midRow + 2] = true;
            array[midCol - 2][midRow + 2] = true;
            break;
        } else if (StringEqual(entry, "glider"))
        {
            array[midCol - 1][midRow - 1] = true;
            array[midCol][midRow - 1] = true;
            array[midCol + 1][midRow - 1] = true;
            array[midCol + 1][midRow] = true;
            array[midCol][midRow + 1] = true;
            break;
        } else if (StringEqual(entry, "hwss"))
        {
            array[midCol - 3][midRow - 2] = true;
            array[midCol - 2][midRow - 2] = true;
            array[midCol - 1][midRow - 2] = true;
            array[midCol][midRow - 2] = true;
            array[midCol + 1][midRow - 2] = true;
            array[midCol + 2][midRow - 2] = true;
            array[midCol - 4][midRow - 1] = true;
            array[midCol + 2][midRow - 1] = true;
            array[midCol + 2][midRow] = true;
            array[midCol - 4][midRow + 1] = true;
            array[midCol + 1][midRow + 1] = true;
            array[midCol - 2][midRow + 2] = true;
            array[midCol - 1][midRow + 2] = true;
            break;
        } else if (StringEqual(entry, "lwss"))
        {
            array[midCol - 2][midRow - 2] = true;
            array[midCol - 1][midRow - 2] = true;
            array[midCol][midRow - 2] = true;
            array[midCol + 1][midRow - 2] = true;
            array[midCol - 3][midRow - 1] = true;
            array[midCol + 1][midRow - 1] = true;
            array[midCol + 1][midRow] = true;
            array[midCol - 3][midRow + 1] = true;
            array[midCol][midRow + 1] = true;
            break;
        } else if (StringEqual(entry, "mwss"))
        {
            array[midCol - 3][midRow - 2] = true;
            array[midCol - 2][midRow - 2] = true;
            array[midCol - 1][midRow - 2] = true;
            array[midCol][midRow - 2] = true;
            array[midCol + 1][midRow - 2] = true;
            array[midCol - 4][midRow - 1] = true;
            array[midCol + 1][midRow - 1] = true;
            array[midCol + 1][midRow] = true;
            array[midCol - 4][midRow + 1] = true;
            array[midCol][midRow + 1] = true;
            array[midCol - 2][midRow + 2] = true;
            break;
        } else if (StringEqual(entry, "r-pentomino"))
        {
            array[midCol][midRow - 1] = true;
            array[midCol + 1][midRow - 1] = true;
            array[midCol - 1][midRow] = true;
            array[midCol][midRow] = true;
            array[midCol][midRow + 1] = true;
            break;
        } else if (StringEqual(entry, "traffic light"))
        {
            array[midCol - 1][midRow - 3] = true;
            array[midCol][midRow - 3] = true;
            array[midCol + 1][midRow - 3] = true;
            array[midCol - 3][midRow - 1] = true;
            array[midCol + 3][midRow - 1] = true;
            array[midCol - 3][midRow] = true;
            array[midCol + 3][midRow] = true;
            array[midCol - 3][midRow + 1] = true;
            array[midCol + 3][midRow + 1] = true;
            array[midCol - 1][midRow + 3] = true;
            array[midCol][midRow + 3] = true;
            array[midCol + 1][midRow + 3] = true;
            break;
        } else {
            bool colEntered = false;
            bool rowEntered = false;
            int col = 0;
            int row = 0;
            int entryLength = StringLength(entry);
            int index;
            for (index = 0; index < entryLength; index++)
            {
                char indexChar = IthChar(entry, index);
                if (isdigit(indexChar)) break;
            }
            for (; index < entryLength; index++)
            {
                char indexChar = IthChar(entry, index);
                if (isdigit(indexChar))
                {
                    colEntered = true;
                    col = 10 * col + StringToInteger(CharToString(indexChar));
                } else break;
            }
            for (; index < entryLength; index++)
            {
                char indexChar = IthChar(entry, index);
                if (isdigit(indexChar)) break;
            }
            for (; index < entryLength; index++)
            {
                char indexChar = IthChar(entry, index);
                if (isdigit(indexChar))
                {
                    rowEntered = true;
                    row = 10 * row + StringToInteger(CharToString(indexChar));
                } else break;
            }
            if (!colEntered)
            {
                printf("No column coordinate was entered. Try again: ");
                entry = GetLine();
            } else if (!rowEntered)
            {
                printf("No row coordinate was entered. Try again: ");
                entry = GetLine();
            } else
            {
                if (col >= cols || row >= rows)
                {
                    printf("Column or row not in board. Try again: ");
                    entry = GetLine();
                } else
                {
                    array[col][row] = true;
                    printf("%d, %d entered.\n", col, row);
                    DrawGrid(array, cols, rows);
                    printf("Enter another coordinate (x, y) or press Enter to end: ");
                    entry = GetLine();
                }
            }
        }
    }
    printf("\n");
}

/* Introduction */
/* This function gets a boolean array called array. It prints a sentence about
 * what this program does, and then prompts the user to enter the number of rows
 * and columns in the Game of Life board. If the number entered for the number
 * of rows or columns is not between 1 and 50, it prompts the user to try again,
 * because array only stores up to 50 rows and columns. When the entered values
 * are in the range of 1-50, this function calls GetPattern with the number of
 * columns and rows specified, and after the pattern is entered, it calls Run
 * with the same number of rows and columns.
 */
void Introduction(bool array[boardCols][boardRows])
{
    printf("This program runs a pattern on Conway's Game of Life.\n\n");
    while (true)
    {
        printf("Enter the number of rows in the board (8-%d): ", boardRows);
        int rows = GetInteger();
        while (rows < 8 || rows > boardRows)
        {
            printf("Number not in specified range. Try again: ");
            rows = GetInteger();
        }
        printf("Enter the number of columns in the board (8-%d): ", boardCols);
        int cols = GetInteger();
        while (cols < 8 || cols > boardCols)
        {
            printf("Number not in specified range. Try again: ");
            cols = GetInteger();
        }
        GetPattern(array, cols, rows);
        printf("Here is the grid, at generation 0:\n");
        DrawGrid(array, cols, rows);
        Run(array, cols, rows);
        printf("Do you want to play again (y/n)? ");
        char firstChar;
        while (true)
        {
            string playAgain = ConvertToLowerCase(GetLine());
            firstChar = IthChar(playAgain, 0);
            if (firstChar == 'n' || firstChar == 'y')
            {
                break;
            } else
            {
                printf("I do not understand your answer.\n");
                printf("Try again: ");
            }
        }
        if (firstChar == 'n') break;
    }
}

/* main */
/* The main loop initializes a boolean array called CellArray, and calls the
 * function Introduction on the array.
 */
int main(void)
{
    bool cellArray[boardCols][boardRows];
    Introduction(cellArray);
    return 0;
}
