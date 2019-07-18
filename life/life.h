/**
 * @file life.h
 *
 * @author Eric Binnendyk
 *
 * @date December 7, 2017
 *
 * @brief Function prototypes used in an implemenation of Conway's Game of Life.
 */

#ifndef LIFE_H_
#define LIFE_H_

struct point_t {
        int x;
        int y;
};

#define HEDGE 0
#define TORUS 1
#define KLEIN 2

#define SIZE 1024

unsigned char **init_matrix(int height, int width);
void find_neighbors(int i, int j, int width, int height, int mode, struct point_t *neighbor_coords);
void update_cell(unsigned char **next_gen, unsigned char **life_grid, int x, int y, int width, int height, struct point_t *all_neighbors);
int count_live_neighbors(unsigned char **life_grid, int width, int height, struct point_t *all_neighbors);
void copy_cells(unsigned char **life_grid, unsigned char **next_gen, int width, int height);
int cell_state(unsigned char **life_grid, int width, int height, struct point_t cell);
int out_of_bounds(struct point_t cell, int width, int height);
void free_grid(unsigned char **grid, int width);
int parse_file_106(FILE *patfile, unsigned char **life_grid, int width, int height, struct point_t offset, int mode);
int set_cell(unsigned char **life_grid, int width, int height, struct point_t cell, int value);
void correct_coords(struct point_t *p_curr_cell, int mode, int width, int height);
int parse_file_105(FILE *patfile, unsigned char **life_grid, int width, int height, struct point_t offset, int mode);
struct point_t convert_coords(struct point_t parsed_coords, int width, int height);
int read_file(FILE *patfile, unsigned char **life_grid, int width, int height, struct point_t offset, int mode);
int copy_live_cells(unsigned char **dest, unsigned char **src, int width, int height);
void clear_grid(unsigned char **grid, int width, int height);

#endif
