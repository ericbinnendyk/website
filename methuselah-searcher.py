import golly as g

def gcd(n1, n2):
	if n1 < n2:
		return ord_gcd(n1, n2)
	else:
		return ord_gcd(n2, n1)

def ord_gcd(l, g):
	if g % l == 0:
		return l
	return gcd(g % l, l)

def lcm(n1, n2):
	return n1 * n2 / gcd(n1, n2)

rawentry1 = g.getstring("Enter the most common naturally occurring periods of oscillators and spaceships in this rule separated by commas (no spaces):")
rawentry2 = g.getstring("What is the maximum number of generations to run each soup?")
rawentry3 = g.getstring("How many soups do you want to test?")

periodlist = map(int, rawentry1.split(','))
maxgens = int(rawentry2)
soups = int(rawentry3)

totalperiod = 1
for period in periodlist:
	totalperiod = lcm(period, totalperiod)

longest = [], 0
for soupnum in range(soups):
	g.new('')
	g.select([0,0,5,5])
	g.randfill(50)
	currsoup = g.getcells([0,0,5,5])
	currpop = g.getpop()
	sameaslast = 0
	totalgens = 0
	success = False
	while totalgens < maxgens:
		g.run(totalperiod)
		totalgens += totalperiod
		if g.getpop() == currpop:
			sameaslast += 1
		else:
			sameaslast == 0
		currpop = g.getpop()
		if sameaslast == 5:
			# We assume it's stabilized
			success = True
			totalgens -= totalperiod * 5
			if totalgens > longest[1]:
				longest = currsoup, totalgens
			break
	if not success:
		g.new('')
		g.putcells(currsoup)
		g.show("Found soup lasting longer than %d generations" % maxgens)
		break
	g.show("Searched %d soups; longest lifespan ~%d" % (soupnum + 1, longest[1]))
	g.update()

if success:
	g.new('')
	g.putcells(longest[0])
	g.show("Found soup stabilizing after ~%d generations" % longest[1])
