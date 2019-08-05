import golly as g

g.setrule('B3/S23')
rulestring = 'B3/S23'
rule_list = []
rules = g.getdir('temp') + 'rules.txt'

ngens = 100
f = open(rules, 'w')
f.write(rulestring + '\n')
f.close()

def censusgen():
	neighbor_list = []
	bbox = g.getrect()
	for y in range(bbox[1], bbox[1] + bbox[3]):
		for x in range(bbox[0], bbox[0] + bbox[2]):
			numneighs = sum([g.getcell(x, y-1), g.getcell(x+1, y-1), g.getcell(x+1, y), g.getcell(x+1, y+1), g.getcell(x, y+1), g.getcell(x-1, y+1), g.getcell(x-1, y), g.getcell(x-1, y-1)])
			neighbor_census[9*g.getcell(x, y) + numneighs][1] += 1

first = lambda x: x[1]


currrule = [0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0]
rulelist = [currrule]

for x in range(1023):
	neighbor_census = []
	for centerstate in range(2):
		for numneighs in range(9):
			neighbor_census.append([(centerstate, numneighs), 0])

	g.new('%s testing grounds' % rulestring)
	g.select([0, 0, 20, 20])
	g.randfill(50)
	g.select([])
	g.fit()
	g.update()
	for gen in range(ngens):
		censusgen()
		g.step()
		g.fit()
		g.update()

	neighbor_census.sort(key=first)
	currneigh = 0
	counts = [0]
	currcount = 0
	currcombo = -1
	newrule = [0] * 18
	testnum = 0
	while currneigh <= 18:
		nextcount = -1
		for index, count in enumerate(counts):
			if count > currcount or (count == currcount and index > currcombo):
				if nextcount == -1 or nextcount > count:
					nextcount = count
					nextcombo = index
		currcount = nextcount
		currcombo = nextcombo
		if currneigh != 18 and currcount > neighbor_census[currneigh][1] or testnum == 2 ** currneigh:
			currcombo = 2 ** currneigh
			currcount = neighbor_census[currneigh][1]
			newcounts = map(lambda c: c + currcount, counts)
			counts.extend(newcounts)
			currneigh += 1
		changes = [0] * 18
		index = 0
		currcombocopy = currcombo
		while currcombocopy > 0:
			neightup = neighbor_census[index][0]
			cindex = 9 * neightup[0] + neightup[1]
			changes[cindex] = currcombocopy % 2
			currcombocopy /= 2
			index += 1
		for index, change in enumerate(changes):
			newrule[index] = currrule[index] ^ change
		#g.note(str(counts) + ', ' + str(currcombo) + ', ' + str(currcount) + ', ' + str(newrule))
		if newrule not in rulelist:
			currrule = newrule
			rulelist.append(currrule)
			break
		testnum += 1

	rulestring = 'B/S'
	for index, condition in enumerate(currrule):
		if index < 9:
			if condition == 1:
				rulestring = rulestring[:-2] + str(index) + rulestring[-2:]
		else:
			if condition == 1:
				rulestring += str(index - 9)

	f = open(rules, 'a')
	f.write(rulestring + '\n')
	f.close()

	g.setrule(rulestring)

g.open(rules)