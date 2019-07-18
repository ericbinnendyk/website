/**
 * @file life.c
 *
 * @author Eric Binnendyk
 *
 * @date December 7, 2017
 *
 * @brief Functions used in an implemenation of Conway's Game of Life.
 *
 * @details Functions utilized in an implementation of Conway's Game of Life
   using dynamically allocated arrays of byte arrays to store cells and reading
   patterns from an input file in Life 1.05 or Life 1.06 format.
 *
 * @bug none
 *
 * @todo written in notebook
 */

#include <stdlib.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include "life.h"

/** Given the coordinates of a cell, find the coordinates of its 8 orthogonal
    and diagonal neighbors, and stores them in an array.
 * @param x the x-index of the cell on the grid
 * @param y the y-index of the cell on the grid
 * @param width the width of the grid (length of the array)
 * @param height the height of the grid (length of a sub-array)
 * @param mode an integer determining the behavior at the edges of the Life
   universe: hedge, torus, or Klein bottle.
 * @param neighbor_coords an array of structures representing cell coordinates,
   to be filled with neighbor coordinates.
 * @remarks This function does not use struct point_t to store the location of
   the current cell because it gets called from the iteration through the array.
 */
void find_neighbors(int x, int y, int width, int height, int mode, struct point_t *neighbor_coords)
{
        struct point_t coords[] = {{x - 1, y}, {x - 1, y + 1}, {x, y + 1}, {x + 1, y + 1}, {x + 1, y}, {x + 1, y - 1}, {x, y - 1}, {x - 1, y - 1}};
        int n;
        for (n = 0; n < 8; n++)
                neighbor_coords[n] = coords[n];

        for (n = 0; n < 8; n++)
                correct_coords(&(neighbor_coords[n]), mode, width, height);
}

/** Allocates memory for a matrix of bytes, with specified height and width.
 * @param height the height of the matrix
 * @param width the width of the matrix
 * @return a pointer to the memory allocated
 */
unsigned char **init_matrix(int height, int width)
{
        unsigned char **matrix = calloc(width, sizeof(unsigned char *));
        if (matrix == NULL) {
                fprintf(stderr, "Out of memory. Exiting now.\n");
                exit(ENOMEM);
        }

        int i;
        for (i = 0; i < width; i++) {
                matrix[i] = calloc(height, sizeof(unsigned char));
                if (matrix[i] == NULL) {
                        fprintf(stderr, "Out of memory. Exiting now.\n");
                        exit(ENOMEM);
                }
        }
        return matrix;
}

/** Calculates the state of a cell in the next generation according to the rules
    of Life, and stores the result in a matrix representing the next generation.
 * @param next_gen the matrix of cells of the pattern in the next generation.
 * @param life_grid the matrix of cells; the Life universe
 * @param x the number of the row in the grid containing the cell, or the number
   of the column in the canvas containing the cell
 * @param y the number of the column in the grid containing the cell, or the
   number of the row in the canvas containing the cell
 * @param width the number of rows in the matrix
 * @param height the number of columns in the matrix
 * @param all_neighbors an array holding coordinates of the neighbors of the
   current cell
 */
void update_cell(unsigned char **next_gen, unsigned char **life_grid, int x, int y, int width, int height, struct point_t *all_neighbors)
{
        int state = (life_grid[x])[y];
        int live_count = count_live_neighbors(life_grid, width, height, all_neighbors);
        struct point_t cell = {x, y};
        if (live_count == 3)
                set_cell(next_gen, width, height, cell, 1);
        else if (live_count == 2 && state == 1)
                set_cell(next_gen, width, height, cell, 1);
        else
                set_cell(next_gen, width, height, cell, 0);
}

/** Finds the number of live (state-1) neighbors, orthogonal and diagonal, of a
    cell in the Life matrix.
 * @param life_grid the matrix of cells; the Life universe
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @param all_neighbors an array holding coordinates of the neighbors of the
   current cell
 * @return the number of living neighbors in the grid
 */
int count_live_neighbors(unsigned char **life_grid, int width, int height, struct point_t *all_neighbors)
{
        int count = 0;
        int n;
        for (n = 0; n < 8; n++)
                count += cell_state(life_grid, width, height, all_neighbors[n]);

        return count;
}

/** Given coordinates that determine a cell in a Life grid, finds the state of
    the cell.
 * @param life_grid the matrix of cells; the Life universe
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @param cell the coordinates of the cell in the grid, or the "dummy
   coordinates" -1, -1
 * @return the state of the cell provided (0 for off or 1 for on), or 0 if the
   coordinates do not refer to a cell in the grid
 */
int cell_state(unsigned char **life_grid, int width, int height, struct point_t cell)
{
        /* This happens when cell is -1, -1: a pseudo-point taking the place of
         * the cell's neighbor when it has none. */
        if (out_of_bounds(cell, width, height))
                return 0;
        return (life_grid[cell.x])[cell.y];
}

/** Checks whether or not a pair of coordinates represent a cell in the Life
    matrix and don't need to be corrected to be interpreted as array indices.
 * @param cell the coordinates to check
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @return 0 if the cell is inside the matrix, or 1 if it is not.
 */
int out_of_bounds(struct point_t cell, int width, int height)
{
        return cell.x < 0 || cell.x >= width || cell.y < 0 || cell.y >= height;
}

/** Given two byte matrices with the same width and height, copies the contents
    of one matrix to another.
 * @param dest the matrix to be copied to
 * @param src the matrix to be copied
 * @param width the width of the matrices dest and src
 * @param height the height of the matrices dest and src
 */
void copy_cells(unsigned char **dest, unsigned char **src, int width, int height)
{
        int i, j;
        for (i = 0; i < width; i++) {
                for (j = 0; j < height; j++) {
                        (dest[i])[j] = (src[i])[j];
                }
        }
}

/** Frees a matrix of bytes that have been allocated with malloc and stored as
    an array of pointers to arrays.
 * @param grid the matrix to free
 * @param width the width of the matrix
 */
void free_grid(unsigned char **grid, int width)
{
        int i;
        for (i = 0; i < width; i++)
                free(grid[i]);

        free(grid);
}

/** Parses a file containing a Life pattern in Life 1.06 format and stores it in
    a matrix.
 * @param patfile a pointer to the file to read
 * @param patt_grid the matrix to store the pattern in
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @param offset the offset of the pattern from the center of the grid
 * @param mode an integer determining the behavior at the edges of the Life
   universe: hedge, torus, or Klein bottle.
 * @return 1 if the file is badly formatted, otherwise 0
 * @remarks The pattern read in from the file is processed in "virtual
   coordinates," where 0, 0 is at the center of the grid, as opposed to the
   coordinates used elsewhere that have 0, 0 in the upper left corner.
 */
int parse_file_106(FILE *patfile, unsigned char **patt_grid, int width, int height, struct point_t offset, int mode)
{
        /* We already read the first line */
        int linenum = 1;
        char buf[SIZE];
        int off_grid = 0;
        int overlapping = 0;

        while (fgets(buf, SIZE, patfile) != NULL) {
                struct point_t curr_cell = offset;
                if (buf[0] == '#') {
                        if (buf[1] == 'R') {
                                int buflen = strlen(buf);
                                if (buflen > 3) {
                                        int alien_rule = 1;
                                        if (!strncmp(buf + 3, "23/3", 5))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "B3/S23", 7))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "B3S23", 6))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "b3/s23", 7))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "b3s23", 5))
                                                alien_rule = 0;
                                        if (alien_rule)
                                                return 2;
                                }
                        }
                }
                else if (buf[0] != '\0') {
                        char *tok = strtok(buf, " ");
                        if (tok == NULL) {
                                fprintf(stderr, "Error in file parsing: Too few coordinates on line %d.\n", linenum);
                                return 1;
                        }
                        int x = atoi(tok);

                        tok = strtok(NULL, " ");
                        if (tok == NULL) {
                                fprintf(stderr, "Error in file parsing: Too few coordinates on line %d.\n", linenum);
                                return 1;
                        }
                        int y = atoi(tok);

                        curr_cell.x += x;
                        curr_cell.y += y;

                        struct point_t screen_coords = convert_coords(curr_cell, width, height);
                        correct_coords(&screen_coords, mode, width, height);
                        if (!off_grid && out_of_bounds(screen_coords, width, height))
                                off_grid = 1;
                        if (!overlapping && cell_state(patt_grid, width, height, curr_cell) == 1)
                                overlapping = 1;
                        set_cell(patt_grid, width, height, screen_coords, 1);
                }
                linenum++;
        }
        if (off_grid)
                printf("WARNING: A pattern truncated as it does not fit on the grid.\n");
        if (overlapping)
                printf("WARNING: A pattern wraps around the grid and overlaps with itself.\n");

        return 0;
}

/** Sets the state of a cell in a matrix to a specified value.
 * @param life_grid the matrix of cells; the Life universe
 * @param width the width of the grid
 * @param height the height of the grid
 * @param cell the coordinates of the cell to set
 * @param value the value to set the cell to
 * @return 0 if the cell is set successfully, or 1 if the position provided is
   out of bounds
 */
int set_cell(unsigned char **life_grid, int width, int height, struct point_t cell, int value)
{
        /* Should only happen when the cell is -1, -1, meaning invalid. */
        if (out_of_bounds(cell, width, height))
                return 1;
        life_grid[cell.x][cell.y] = value;
        return 0;
}

/** Given the coordinates of an out-of-bounds cell, and the boundary rules,
    finds the coordinates of the corresponding cell inside the matrix, or -1, -1
    if the matrix has no corresponding cell.
 * @param p_curr_cell a pointer to the cell to correct
 * @param mode an integer determining the behavior at the edges of the Life
   universe: hedge, torus, or Klein bottle.
 * @param width the number of rows in the matrix
 * @param height the number of colums in the matrix
 */
void correct_coords(struct point_t *p_curr_cell, int mode, int width, int height)
{
        if (p_curr_cell->x < 0 || p_curr_cell->x >= width) {
                int num_horiz_wraps;
                switch (mode) {
                case HEDGE:
                        p_curr_cell->x = -1;
                        p_curr_cell->y = -1;
                        break;
                case TORUS:
                        if (p_curr_cell->x < 0)
                                while (p_curr_cell->x < 0)
                                        p_curr_cell->x += width;
                        else if (p_curr_cell->x >= width)
                                p_curr_cell->x %= width;
                        break;
                case KLEIN:
                        /* When a pattern gets wrapped horizontally around the
                           Klein bottle an odd number of times, it gets flipped
                           across the x-axis. */
                        num_horiz_wraps = 0;
                        if (p_curr_cell->x < 0)
                                while (p_curr_cell->x < 0) {
                                        p_curr_cell->x += width;
                                        num_horiz_wraps++;
                                }
                        else if (p_curr_cell->x >= width) {
                                num_horiz_wraps = p_curr_cell->x / width;
                                p_curr_cell->x %= width;
                        }
                        if (num_horiz_wraps % 2 == 1)
                                p_curr_cell->y = height - 1 - p_curr_cell->y;
                        break;
                }
        }

        if (p_curr_cell->y < 0 || p_curr_cell->y >= height) {
                switch (mode) {
                case HEDGE:
                        p_curr_cell->x = -1;
                        p_curr_cell->y = -1;
                        break;
                case TORUS:
                case KLEIN:
                        if (p_curr_cell->y < 0)
                                while (p_curr_cell->y < 0)
                                        p_curr_cell->y += height;
                        else if (p_curr_cell->y >= height)
                                p_curr_cell->y %= height;
                        break;
                }
        }
}

/** Parses a file containing a Life pattern in Life 1.05 format and stores it in
    a matrix.
 * @param patfile a pointer to the file to read
 * @param patt_grid the matrix to store the pattern in
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @param offset the offset of the pattern from the center of the grid
 * @param mode an integer determining the behavior at the edges of the Life
   universe: hedge, torus, or Klein bottle.
 * @return 1 if the file is badly formatted, 2 if the pattern is in a rule other
   than Life, otherwise 0
 * @remarks The pattern read in from the file is processed in "virtual
   coordinates," where 0, 0 is at the center of the grid, as opposed to the
   coordinates used elsewhere that have 0, 0 in the upper left corner.
   This function is to be called by read_file, after the first line has already
   been read.
 */
int parse_file_105(FILE *patfile, unsigned char **patt_grid, int width, int height, struct point_t offset, int mode)
{
        /* We already read the first line in read_file. */
        int linenum = 1;
        char buf[SIZE];
        int off_grid = 0;
        int overlapping = 0;
        int x, y = 0;

        struct point_t tmp_offset = {0, 0};

        while (fgets(buf, SIZE, patfile) != NULL) {
                /* Remove the trailing newline */
                buf[strlen(buf) - 1] = '\0';
                if (buf[0] == '#') {
                        if (buf[1] == 'P') {
                                strtok(buf, " ");

                                char *tok = strtok(NULL, " ");
                                if (tok == NULL) {
                                        fprintf(stderr, "Error in file parsing: Too few coordinates on line %d.\n", linenum);
                                        return 1;
                                }
                                int x_offset = atoi(tok);

                                tok = strtok(NULL, " ");
                                if (tok == NULL) {
                                        fprintf(stderr, "Error in file parsing: Too few coordinates on line %d.\n", linenum);
                                        return 1;
                                }
                                int y_offset = atoi(tok);
                                tmp_offset.x = x_offset;
                                tmp_offset.y = y_offset;

                                y = 0;
                        }
                        else if (buf[1] == 'R') {
                                int buflen = strlen(buf);
                                if (buflen > 3) {
                                        int alien_rule = 1;
                                        if (!strncmp(buf + 3, "23/3", 5))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "B3/S23", 7))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "B3S23", 6))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "b3/s23", 7))
                                                alien_rule = 0;
                                        if (!strncmp(buf + 3, "b3s23", 5))
                                                alien_rule = 0;
                                        if (alien_rule)
                                                return 2;
                                }
                        }
                }
                else if (buf[0] != '\0') {
                        struct point_t curr_cell;
                        x = 0;
                        while (buf[x] != '\0') {
                                if (buf[x] == '*') {
                                        curr_cell.x = offset.x + tmp_offset.x + x;
                                        curr_cell.y = offset.y + tmp_offset.y + y;

                                        struct point_t screen_coords = convert_coords(curr_cell, width, height);
                                        correct_coords(&screen_coords, mode, width, height);
                                        if (!off_grid && out_of_bounds(screen_coords, width, height))
                                                off_grid = 1;
                                        if (!overlapping && cell_state(patt_grid, width, height, screen_coords) == 1)
                                                overlapping = 1;
                                        set_cell(patt_grid, width, height, screen_coords, 1);
                                }
                                x++;
                        }
                        y++;
                }
                linenum++;
        }
        if (off_grid)
                printf("WARNING: Pattern truncated as the given pattern does not fit on the grid.\n");
        if (overlapping)
                printf("WARNING: A pattern wraps around the grid and overlaps with itself.\n");

        return 0;
}

/** Converts the "virtual coordinates" of a cell given in the input file into
    the coordinates of the cell on the grid.
 * @param parsed_coords the coordinates of the cell, read from the input file
 * @param width the number of rows in the Life matrix
 * @param height the number of columns in the Life matrix
 */
struct point_t convert_coords(struct point_t parsed_coords, int width, int height)
{
        struct point_t screen_coords = {parsed_coords.x + width / 2, parsed_coords.y + height / 2};
        screen_coords.y = height - screen_coords.y - 1;
        return screen_coords;
}

/** Parses a file containing a Life pattern and stores the pattern in the grid.
 * @param patfile a pointer to the file to read
 * @param life_grid the matrix to store the pattern in
 * @param width the width of the matrix
 * @param height the height of the matrix
 * @param offset the offset of the pattern from the center of the grid
 * @param mode an integer determining the behavior at the edges of the Life
   universe: hedge, torus, or Klein bottle.
 * @return 0 if the file was read successfully, 2 if the file contains a pattern
   in a rule other than Life, otherwise 1.
 */
int read_file(FILE *patfile, unsigned char **life_grid, int width, int height, struct point_t offset, int mode)
{
        char buf[SIZE];

        clear_grid(life_grid, width, height);

        fgets(buf, SIZE, patfile);
        if (buf == NULL)
                return 1;
        /* .lif files contain a line, usually the first, telling whether the
           pattern is encoded in Life 1.05 or Life 1.06 */
        if (!strncmp(buf, "#Life ", 6)) {
                if (!strncmp(buf, "#Life 1.06", 10)) {
                        return parse_file_106(patfile, life_grid, width, height, offset, mode);
                }
                else if (!strncmp(buf, "#Life 1.05", 10)) {
                        return parse_file_105(patfile, life_grid, width, height, offset, mode);
                }
                else
                        return 1;
        }
        return 1;
}

/** Similar to copy_cells, but only copies the elements of the source matrix
    with the value 1.
 * @param dest the matrix to be copied to
 * @param src the matrix to be copied
 * @param width the width of the matrices dest and src
 * @param height the height of the matrices dest and src
 * @return Returns 0 if every 1 in src got copied to an element of dest that was
   previously 0 (meaning no overlaps), otherwise returns 1.
 */
int copy_live_cells(unsigned char **dest, unsigned char **src, int width, int height)
{
        int overlaps = 0;
        int i, j;
        for (i = 0; i < width; i++) {
                for (j = 0; j < height; j++) {
                        if ((src[i])[j] == 1) {
                                if (!overlaps && (dest[i])[j] == 1)
                                        overlaps = 1;
                                (dest[i])[j] = 1;
                        }
                }
        }

        return overlaps;
}

/** Sets all elements of a matrix to 0.
 * @param grid the matrix to zero out
 * @param width the number of rows in the matrix
 * @param height the number of columns in the matrix
 */
void clear_grid(unsigned char **grid, int width, int height)
{
        int i, j;
        for (i = 0; i < width; i++)
                for (j = 0; j < height; j++)
                        grid[i][j] = 0;
}
