def print_triangle_row(rownum, mult):
    num = mult
    for x in xrange(rownum):
        print num,
        num = num * (rownum - x) / (x + 1)
    print num

def choose(n, r):
    c = 1
    for x in xrange(r):
        c = c * (n - r + x + 1) / (x + 1)
    return c

def print_simplex_layer(dim, level, mult):
    if dim == 1:
        print 1
    elif dim == 2:
        print_triangle_row(level, mult)
    else:
        for sublevel in xrange(level):
            print_simplex_layer(dim - 1, level - sublevel, mult * choose(level, sublevel))
            for x in xrange(dim - 3):
                print
        print mult

while True:
    input = raw_input("Enter the dimension of the Pascal's simplex and the level you want to compute,\n\
separated by a comma: ")
    if input == '':
        break
    while eval(input)[0] <= 0 or eval(input)[1] < 0:
        input = raw_input("Try again: ")
    layer_data = eval(input)
    print_simplex_layer(layer_data[0], layer_data[1], 1)