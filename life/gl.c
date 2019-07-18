/**
 * @file gl.c
 *
 * @author Eric Binnendyk
 *
 * @date December 7, 2017
 *
 * @brief Runs Conway's Game of Life!
 *
 * @details Implementation of Conway's Game of Life in C, using SDL. Reads files
   in life 1.05 and 1.06 formats, and features options to set the cell size,
   cell color, size of the window, and offset of the initial pattern. Suuports
   hedged grids, tori, and Klein bottles.
 *
 * @bug none
 *
 * @todo parse_file_106 should interpret coordinates as pattern coordinates and
   convert to grid coordinates automatically. e.g. in pattern coordinates 0,0 is
   at the center of the grid (done?)
 */

#include <stdlib.h>
#include "SDL2/SDL.h"
#include "sdl.h"
#include "life.h"
#include "unistd.h"

#define ERR_NO_ARG 1
#define ERR_SPRITE 2
#define ERR_UNKNOWN_OPT 3
#define ERR_FILE_PARSE 4
#define ERR_FOPEN 5
#define ERR_NOFILE 6
#define ERR_OFFSET 7
#define ERR_TOO_MANY_PATTS 8
#define ERR_NO_OPTS 9
#define ERR_ALIEN_RULE 10
#define ERR_BAD_WIDTH 11
#define ERR_BAD_HEIGHT 12

#define MAX_PATTERNS 10

#define MIN_WIDTH 20
#define MAX_WIDTH 1280
#define MIN_HEIGHT 20
#define MAX_HEIGHT 576

void print_gen(unsigned char **life_grid, int w, int h);
void exit_error(int err_type);
void print_help(char *prog_name);
void free_all(unsigned char **life_grid, unsigned char **next_gen, unsigned char **patt_grid, int width);
void init_str_array(char **arr, int size);
void init_point_array(struct point_t *arr, int size);

int main(int argc, char *argv[])
{
        if (argc == 1)
                exit_error(ERR_NO_OPTS);

	int width = 800;
	int height = 600;
	int sprite_size = 4; /* either 2, 4, 8, or 16 */
	int m = -66;
	int n = -10;
        /* colors are RGB model valid values [0, 255] */
	unsigned char red = 140;
	unsigned char green = 145;
	unsigned char blue = 250;
        struct sdl_info_t sdl_info; /* this is needed to graphically display the game */

        int mode = HEDGE;

        char *files[MAX_PATTERNS];
        struct point_t offsets[MAX_PATTERNS];

        int num_patterns = 0;
        init_str_array(files, MAX_PATTERNS);
        init_point_array(offsets, MAX_PATTERNS);

        int is_done = 0;
        while (!is_done) {
                switch (getopt(argc, argv, "w:h:e:r:g:b:s:f:o:H")) {
                case EOF:
                        is_done = 1;
                        break;
                case 'w':
                        if (optarg != NULL) {
                                int w_arg = atoi(optarg);
                                if (w_arg >= MIN_WIDTH && w_arg <= MAX_WIDTH)
                                        width = w_arg;
                                else
                                        exit_error(ERR_BAD_WIDTH);
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'h':
                        if (optarg != NULL) {
                                int h_arg = atoi(optarg);
                                if (h_arg >= MIN_HEIGHT && h_arg <= MAX_HEIGHT)
                                        height = h_arg;
                                else
                                        exit_error(ERR_BAD_HEIGHT);
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'e':
                        if (optarg != NULL) {
                                if (!strncmp(optarg, "hedge", 6))
                                        mode = HEDGE;
                                if (!strncmp(optarg, "torus", 6))
                                        mode = TORUS;
                                if (!strncmp(optarg, "klein", 6))
                                        mode = KLEIN;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'r':
                        if (optarg != NULL) {
                                unsigned char r_arg = (unsigned char) atoi(optarg);
                                if (r_arg < 0)
                                        r_arg = 0;
                                else if (r_arg >= 256)
                                        r_arg = 255;
                                red = r_arg;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'g':
                        if (optarg != NULL) {
                                unsigned char g_arg = (unsigned char) atoi(optarg);
                                if (g_arg < 0)
                                        g_arg = 0;
                                else if (g_arg >= 256)
                                        g_arg = 255;
                                green = g_arg;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'b':
                        if (optarg != NULL) {
                                unsigned char b_arg = (unsigned char) atoi(optarg);
                                if (b_arg < 0)
                                        b_arg = 0;
                                else if (b_arg >= 256)
                                        b_arg = 255;
                                blue = b_arg;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 's':
                        if (optarg != NULL) {
                                int s_arg = atoi(optarg);
                                switch (s_arg) {
                                case 2:
                                case 4:
                                case 8:
                                case 16:
                                        sprite_size = s_arg;
                                        break;
                                default:
                                        exit_error(ERR_SPRITE);
                                }
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'f':
                        if (num_patterns >= MAX_PATTERNS)
                                exit_error(ERR_TOO_MANY_PATTS);
                        if (optarg != NULL) {
                                files[num_patterns] = optarg;
                                num_patterns++;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'o':
                        if (optarg != NULL) {
                                char *o_str_x = strtok(optarg, ",");
                                if (o_str_x == NULL)
                                        exit_error(ERR_OFFSET);
                                char *o_str_y = strtok(NULL, ",");
                                if (o_str_y == NULL)
                                        exit_error(ERR_OFFSET);

                                int o_arg_x = atoi(o_str_x);
                                int o_arg_y = atoi(o_str_y);
                                /* ... */
                                offsets[num_patterns - 1].x = o_arg_x;
                                offsets[num_patterns - 1].y = o_arg_y;
                        }
                        else
                                exit_error(ERR_NO_ARG);
                        break;
                case 'H':
                        print_help(argv[0]);
                        exit(0);
                        break;
                default:
                        exit_error(ERR_UNKNOWN_OPT);
                }
        }

        /* set up SDL -- works with SDL2 */
        int w = width / sprite_size;
        int h = height / sprite_size;

        init_sdl_info(&sdl_info, width, height, sprite_size, red, green, blue);
        unsigned char **patt_grid = init_matrix(h, w);
	unsigned char **life_grid = init_matrix(h, w);
        unsigned char **next_gen = init_matrix(h, w);

        if (num_patterns == 0)
                exit_error(ERR_NOFILE);
        for (int i = 0; i < num_patterns; i++) {
                FILE *patfile = fopen(files[i], "r");
                if (patfile == NULL)
                        exit_error(ERR_FOPEN);
                switch (read_file(patfile, patt_grid, w, h, offsets[i], mode)) {
                case 1:
                        exit_error(ERR_FILE_PARSE);
                case 2:
                        exit_error(ERR_ALIEN_RULE);
                }
                fclose(patfile);
                if (copy_live_cells(life_grid, patt_grid, w, h))
                        printf("WARNING: Pattern %s overlaps with a previous pattern.\n", files[i]);
        }

        sdl_render_life(&sdl_info, life_grid);

        /* Has the ability to store less than 9 neighbors (e.g. in the hedged
         * grid) by padding the array with pseudo-coordinates such as -1, -1.
         * A function will be written to return the state of a cell, which
         * will return the value of the corresponding element in the array if
         * the coordinates are valid indexes, and otherwise will return 0 (off).
         */
        struct point_t neighbor_coords[8];

        /* change the modulus value to slow the rendering */
        int modulus = 10;
        int prev_time = -1;
        /* Main loop: loop forever. */
	while (1)
	{
                int curr_time = (int) SDL_GetTicks();
		if (curr_time / modulus > prev_time / modulus) {
                        int i, j;
        		for (i = 0; i < w; i++) {
                                for (j = 0; j < h; j++) {
                                        find_neighbors(i, j, w, h, mode, neighbor_coords);
                                        update_cell(next_gen, life_grid, i, j, w, h, neighbor_coords);
                                }
                        }

                        copy_cells(life_grid, next_gen, w, h);
                        /* print_gen(life_grid, w, h); */
                        sdl_render_life(&sdl_info, life_grid);
                        prev_time = curr_time;
                }

                /* Poll for events, and handle the ones we care about.
                 * You can click the X button to close the window
                 */
		SDL_Event event;
		while (SDL_PollEvent(&event))
		{
			switch (event.type)
			{
			case SDL_KEYDOWN:
				break;
			case SDL_KEYUP:
                        /* If escape is pressed, return (and thus, quit) */
				if (event.key.keysym.sym == SDLK_ESCAPE) {
                                        free_all(life_grid, next_gen, patt_grid, w);
					return 0;
                                }
				break;
			case SDL_QUIT:
                                free_all(life_grid, next_gen, patt_grid, w);
				return 0;
			}
		}
	}
	return 0;
}

/** Prints out the values of an array representing a Life canvas, where '.'
    represents an off cell, and 'o' represents an on cell.
 * @param life_grid the grid of bytes representing life cells.
 * @remarks Useful for debugging.
 */
void print_gen(unsigned char **life_grid, int w, int h)
{
        int i, j;
        for (i = 0; i < w; i++) {
                for (j = 0; j < h; j++)
                        printf(life_grid[i][j] == 0 ? "." : "o");
                printf("\n");
        }
        printf("\n");
}

/** Given an error number, prints a message appropriate to that error and exits.
 * @param err_type an integer representing what error occurred
 */
void exit_error(int err_type)
{
        fprintf(stderr, "ERROR: ");
        switch (err_type) {
        case ERR_NO_ARG:
                fprintf(stderr, "One or more arguments is missing from a command line option.\n");
                break;
        case ERR_SPRITE:
                fprintf(stderr, "Invalid sprite size entered. The valid sprite sizes are 2, 4, 8, and 16.\n");
                break;
        case ERR_UNKNOWN_OPT:
                fprintf(stderr, "Unknown option entered. Use -H to display a list of availible options.\n");
                break;
        case ERR_FILE_PARSE:
                fprintf(stderr, "The file provided cannot be parsed.\n");
                fprintf(stderr, "This program supports the formats Life 1.05 and Life 1.06.\n");
                break;
        case ERR_FOPEN:
                fprintf(stderr, "A file provided does not exist or cannot be opened.\n");
                break;
        case ERR_NOFILE:
                fprintf(stderr, "No input file provided.\n");
                break;
        case ERR_OFFSET:
                fprintf(stderr, "Unable to read one or more offset coordinates.\n");
                break;
        case ERR_TOO_MANY_PATTS:
                fprintf(stderr, "Too many patterns are supplied (the max is %d).\n", MAX_PATTERNS);
                break;
        case ERR_NO_OPTS:
                fprintf(stderr, "No options provided. Use -H to display a list of available options.\n");
                break;
        case ERR_ALIEN_RULE:
                fprintf(stderr, "A file provided contains a pattern in a rule other than Life.\n");
                break;
        case ERR_BAD_WIDTH:
                fprintf(stderr, "The width must be an integer between %d and %d.\n", MIN_WIDTH, MAX_WIDTH);
                break;
        case ERR_BAD_HEIGHT:
                fprintf(stderr, "The height must be an integer between %d and %d.\n", MIN_HEIGHT, MAX_HEIGHT);
                break;
        }
        exit(err_type);
}

/** Prints useful information on how to use each command line option.
 * @param prog_name the name of the binary file containing the compiled source
   code
 */
void print_help(char *prog_name)
{
        printf("Usage: %s -f file [options]\n", prog_name);
        printf("Options:\n");
        printf("  -w: Specify the width of the window\n");
        printf("  -h: Specify the height of the window\n");
        printf("  -e: Specify what happens when the pattern extends beyond the edge of the window.\n");
        printf("          Valid arguments are hedge, torus, and klein.\n");
        printf("  -r: Specify the red component of the color value of the cells as a number from 0 to 255.\n");
        printf("  -g: Specify the green component of the color value of the cells as a number from 0 to 255.\n");
        printf("  -b: Specify the blue component of the color value of the cells as a number from 0 to 255.\n");
        printf("  -s: Specify the size of the cell sprites in number of pixels per edge.\n");
        printf("  -f: Specify the Life file to open, in either Life 1.05 or Life 1.06 format.\n");
        printf("          Use multiple -f options to place multiple files on the grid at once.\n");
        printf("          Up to %d patterns can be open at once.\n", MAX_PATTERNS);
        printf("          This is the only mandatory command.\n");
        printf("  -o: Specify the offset coordinates of the pattern from the center of the grid, separated by a comma.\n");
        printf("  -H: Display this help page.\n");
}

/** Frees the allocated matrices used in the Life program, for instance when
    exiting.
 * @param life_grid a grid of cells to free, representing the current generation
   of the pattern
 * @param next_gen a grid of cells to free, representing the next generation of
   the pattern
 * @param patt_grid a grid of cells to free, acting as a buffer that each
   pattern is loaded into
 * @param width the number of rows in each matrix
 */
void free_all(unsigned char **life_grid, unsigned char **next_gen, unsigned char **patt_grid, int width)
{
        free_grid(life_grid, width);
        free_grid(next_gen, width);
        free_grid(patt_grid, width);
}

/** Initializes an array of strings, of given size, setting each string to NULL.
 * @param arr the array to initialize
 * @param size the size of the array
 */
void init_str_array(char **arr, int size)
{
        int i;
        for (i = 0; i < size; i++)
                arr[i] = NULL;
}

/** Initializes an array of point structures, of given size, setting each point
    to 0, 0.
 * @param arr the array to initialize
 * @param size the size of the array
 */
void init_point_array(struct point_t *arr, int size)
{
        int i;
        for (i = 0; i < size; i++) {
                arr[i].x = 0;
                arr[i].y = 0;
        }
}
