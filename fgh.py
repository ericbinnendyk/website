def fghlist(funcs):
	omitted = 0
	if len(funcs) == 0:
		return funcs
	
	newfuncs = funcs[:]
	if funcs[1][0] == 0:
		newfuncs[0] += 1
		newfuncs[1][1] -= 1
			
	elif funcs[1][0] == 1:
		if funcs[0] > 20:
			omitted = funcs[0]
			newfuncs[0] *= 2
			newfuncs[1][1] -= 1
			
		#This case should be put together...
		else:
			newfuncs.insert(1, [0, funcs[0]])
			newfuncs[2][1] -= 1
			
			if newfuncs[2][1] == 0:
				del newfuncs[2]
	
	#... w/th this one.
	else:
		newfuncs.insert(1, [funcs[1][0] - 1, funcs[0]])
		newfuncs[2][1] -= 1
		
		if newfuncs[2][1] == 0:
			del newfuncs[2]
	
	if newfuncs[1][1] == 0:
		del newfuncs[1]
	
	if omitted > 0:
		print "%d steps omitted..." % omitted
	
	printf(newfuncs)
	
	if len(newfuncs) == 1:
		return newfuncs
	
	if newfuncs[1][0] > 0:
		raw_input()
	
	return newfuncs

def printf(a):
    i = 0
    for n in a:
            if i == 0:
                    astr = str(n)
                    i = 1
            else:
                    if n[1] < 16:
                        for x in xrange(n[1]):
                            astr = 'f%d ' % n[0] + astr
                    else:
                        astr = '{f%d}*%d ' % (n[0], n[1]) + astr
    print astr

def fgh(funcs):
	printf(funcs)
	while len(funcs) > 1:
		funcs = fghlist(funcs)

numtup = input("Enter x, y values where the fast-growing hierarchy expression is f_x(y): ")
funcs = [numtup[1], [numtup[0], 1]]
fgh(funcs)