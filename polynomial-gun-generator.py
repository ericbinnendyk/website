import golly as g
from fractions import Fraction

#maincomp = g.parse('261bo$173bo83b4ob2o5b3o$172b2o82b2ob3ob2o4b3o$171bob2o82bob3obo7b2o$\
#171bo2b2o82bo3b4o4b2o$169b4ob3o84b2ob3o$168bo2bobo2b2o84b5o13b2o$169bo\
#bobob3o85bo16b2o$170b2ob3obo$170b4o2bobo$173bo3bo$173bo3bo$173bo2bo12b\
#2o$189b2o$288b2o$276b3ob3o5b2o$268bo6b4obo2bo$174b2o89b2o4bo2bobo$260b\
#2o5b2o3bo10bo$260b2o7bob2o3b3o$197b2o78b2o2b2o$197b2o65bo$179b2o82bob\
#2o$178bo2bo69b5o6bo3bo$165b2o4b3o4bo2b2o66b2o5b2o3bo2b2o$177bo2b2o67bo\
#7bo3bobo$164bo3bo8b4o68b2o7bo5bo$169bo81b2o6bo$162bo7bo83bo$161bo4bo\
#69b3o15bo4bo$162bobobo4bo64b3o16b2obo$162bo8bo65bo$163bo4b2obo66b2o$\
#143bo20bob2ob3o67bo$142bobo20b3ob2o67bo2$142bo2bo$144b2o100b2o$145bo\
#90b2o7bo2bo$236b2o8b2o$237bo$237bo$236bobo$142b2o91bo$144bo91bo2b2o$\
#143b2o92bo3bo12b2o$142b3o94b2o12bo2bo$142b2o89bo5bo14b2o$232b3o$173bo\
#57b3obo$171bobo56bo3bo$151bo20b2o55b2o2bo2bo$133b3o14bobo75b3o2b4o$\
#131b7o12bobo77bo3bo2bo$130b9o12bo78bo6bo$129bo7b3o3b3o63b3o20bo2bo$\
#130b3o6bo68bo3bo21b2ob2o$131b2o11b2o15b2o44bo4bo21bo$134bo24bob2o43bo\
#3bo$135bo26b2o42bo2bob3o$109b5o7bo14bo26b2o41bo7bo$107b2o5b2o4bobo34b\
#2obob3o43bo3bobo$107bo7bo4bo38b4o45bo3bob2o$107b2o7bo3bo2bo35b3o48b3ob\
#2o$109b2o6bo3b3o8b2o27bo64b2o$112bo22bo21b2o67b2o$112bo4bo40bo$113b2ob\
#o14bo2bo$132bo77b2o$210b2o15b4o2b2o$211bo15bo2bobob2o$129bo97b2ob2obo\
#16bo$128b2o81bo17bo$127bob2o119bo$126b2o2bo$127b2obo78bo5b3o$126b3o80b\
#o7bo35bo$117bobo14bo74bo5bobo10b2o23b2o$111b2o4b3obobo8b2o81b2o10bo2bo\
#16bo3bo$111b2o6bo2b2o9b2o91bo3bo15b5o$228b2o15bo6bo$170b3o73b3o3b2o$\
#172bo49bo24bo4b2o$171bo48b2o$181bo32b2o2b2o5bo$180b3o15bo15b2o4b2o$\
#119b2o58b2ob2o14bo25bo$119b2o57b2o3bo7b4o3bo22b4o$62b5o7bo104bobobobo\
#5bo3bo24bobo$60b2o5b2o4bobo104b2obo2bo4b2o3bo22bo2b2obo$60bo7bo4bo109b\
#2obo7b3o23bo4bo$60b2o7bo3bo2bo107b2o10b2obo6b2o13bo$62b2o6bo3b3o120b3o\
#6b2o14bo2bo$65bo132bo23b2o$65bo4bo13b2o$66b2obo14b2o$206b2o$138b3o65bo\
#bo$140bo65bo3b3o$139bo66bobo3b4o$206bobo3b4o$205b3ob3o$81bo3bo6b2o112b\
#2o$79bo2bob3o5b2o92b2o13b2o$82bobobo99b2o13b2o$70bobo7bo110b3o$64b2o4b\
#3obob2ob2o109bob2o6bo$64b2o6bo2b2o3bobo3bo86b3o14bob2o5bobo$80bobo89bo\
#3bo22bobo$68b2o101bo4bo15bobo$56b3o8b4o100bo2bobo15b2o$54b7o5b2o2bo\
#100b2obobo15bo$53b9o3bob3o84b5o7bo6b2obo2bo$52bo7b3o3b2obo36b3o43b2o5b\
#2o4bobo7b2o2bo$34b2o17b3o6bo45bo43bo7bo4bo10b3o$35bo2bo4bo10b2o51bo44b\
#2o7bo3bo2bo$32bo2b3obo2bobo12bo96b2o6bo3b3o$32bo2bo4b4o14bo98bo$32bo2b\
#o23bo97bo4bo$35bo6bo115b2obo$34b2obo$42bo$40b2o118bo$159bobo$159bobo\
#39b3o$38bo121bo34bo4bo2bo$37bobo33bo120bo2bo3bo$37bobo32b2o3bo69bo46b\
#2obo2b2o$38bo33b2o4bo66b2ob2o44bo6bobo$72b2o4b2o68b2o43bo5bo3bo$73bobo\
#2b3o64b3o20bo23bo6b2ob2o$72bo5bo68bo3bo15bobo30bo$25bo44bob5o69bo3bo\
#16bobo$24b3o19bo25bo3bo70b3obo16bo$23b2ob2o17bobo21b3o52bo24b2o$24b3o\
#18bobo75bobo22bobo$25bo20bo75b2ob2o22bo$25bobo94b2o16b2o6b2o$25b4o99b\
#2o9bo2bo4b3o$2bo25bo93b3o2bo12bo2bo2b2ob2o$bobo122bob2o15bo2b3o$o3bo\
#19b2ob2o95bo2bo17b2o$bobo19bo5bo97bo11bo$2bo14b3o4bo3bo96b2o11b2o3bo$\
#16bo3bo4bo113bo3b2o$2b4o10b3o2bo103bo13bobob2o$bo4bo9bo3bo102b2ob2o11b\
#o3b2o$3bo13b3o106bo13b3o$o3bo2bo9b2o104bo16b3o$ob3obo118bo$b3obo2$139b\
#o$19bo118b3o$16b5o120bo$15bo122b2ob2o$137b2ob2o$16bo3bo107b2o7b2ob2o$\
#17b3o108b2o8bo2bo$139b3o$6b2o131b2o$6b2o4$136b2o$136b2o2$14b2o$14b2o!')

#maincomp = finalcomp + snark

maincomp = g.parse('261bo$173bo83b4ob2o5b3o$172b2o82b2ob3ob2o4b3o$171bob2o82bob3obo7b2o$\
171bo2b2o82bo3b4o4b2o$169b4ob3o84b2ob3o$168bo2bobo2b2o84b5o13b2o$169bo\
bobob3o85bo16b2o$170b2ob3obo$170b4o2bobo$173bo3bo$173bo3bo$173bo2bo12b\
2o$189b2o$288b2o$276b3ob3o5b2o$268bo6b4obo2bo$174b2o89b2o4bo2bobo$260b\
2o5b2o3bo10bo$260b2o7bob2o3b3o$197b2o78b2o2b2o$197b2o65bo$179b2o82bob\
2o$178bo2bo69b5o6bo3bo$165b2o4b3o4bo2b2o66b2o5b2o3bo2b2o$177bo2b2o67bo\
7bo3bobo$164bo3bo8b4o68b2o7bo5bo$169bo81b2o6bo$162bo7bo83bo$161bo4bo\
69b3o15bo4bo$162bobobo4bo64b3o16b2obo$162bo8bo65bo$163bo4b2obo66b2o$\
143bo20bob2ob3o67bo$142bobo20b3ob2o67bo2$142bo2bo$144b2o100b2o$145bo\
90b2o7bo2bo$236b2o8b2o$237bo$237bo$236bobo$142b2o91bo$144bo91bo2b2o$\
143b2o92bo3bo12b2o$142b3o94b2o12bo2bo$142b2o89bo5bo14b2o$232b3o$173bo\
57b3obo$171bobo56bo3bo$151bo20b2o55b2o2bo2bo$133b3o14bobo75b3o2b4o$\
131b7o12bobo77bo3bo2bo$130b9o12bo78bo6bo$129bo7b3o3b3o63b3o20bo2bo$\
130b3o6bo68bo3bo21b2ob2o$131b2o11b2o15b2o44bo4bo21bo$134bo24bob2o43bo\
3bo$135bo26b2o42bo2bob3o$109b5o7bo14bo26b2o41bo7bo$107b2o5b2o4bobo34b\
2obob3o43bo3bobo$107bo7bo4bo38b4o45bo3bob2o$107b2o7bo3bo2bo35b3o48b3ob\
2o$109b2o6bo3b3o8b2o27bo64b2o$112bo22bo21b2o67b2o$112bo4bo40bo$113b2ob\
o14bo2bo$132bo77b2o$210b2o15b4o2b2o$211bo15bo2bobob2o$129bo97b2ob2obo\
16bo$128b2o81bo17bo$127bob2o119bo$126b2o2bo$127b2obo78bo5b3o$126b3o80b\
o7bo35bo$117bobo14bo74bo5bobo10b2o23b2o$111b2o4b3obobo8b2o81b2o10bo2bo\
16bo3bo$111b2o6bo2b2o9b2o91bo3bo15b5o$228b2o15bo6bo$170b3o73b3o3b2o$\
172bo49bo24bo4b2o$171bo48b2o$181bo32b2o2b2o5bo$180b3o15bo15b2o4b2o$\
119b2o58b2ob2o14bo25bo$119b2o57b2o3bo7b4o3bo22b4o$62b5o7bo104bobobobo\
5bo3bo24bobo$60b2o5b2o4bobo104b2obo2bo4b2o3bo22bo2b2obo$60bo7bo4bo109b\
2obo7b3o23bo4bo$60b2o7bo3bo2bo107b2o10b2obo6b2o13bo$62b2o6bo3b3o120b3o\
6b2o14bo2bo$65bo132bo23b2o$65bo4bo13b2o$66b2obo14b2o$206b2o$138b3o65bo\
bo$140bo65bo3b3o$139bo66bobo3b4o$206bobo3b4o$205b3ob3o$81bo3bo6b2o112b\
2o$79bo2bob3o5b2o92b2o13b2o$82bobobo99b2o13b2o$70bobo7bo110b3o$64b2o4b\
3obob2ob2o109bob2o6bo$64b2o6bo2b2o3bobo3bo86b3o14bob2o5bobo$80bobo89bo\
3bo22bobo$68b2o101bo4bo15bobo$56b3o8b4o100bo2bobo15b2o$54b7o5b2o2bo\
100b2obobo15bo$53b9o3bob3o84b5o7bo6b2obo2bo$52bo7b3o3b2obo36b3o43b2o5b\
2o4bobo7b2o2bo$34b2o17b3o6bo45bo43bo7bo4bo10b3o$35bo2bo4bo10b2o51bo44b\
2o7bo3bo2bo$32bo2b3obo2bobo12bo96b2o6bo3b3o$32bo2bo4b4o14bo98bo$32bo2b\
o23bo97bo4bo$35bo6bo115b2obo$34b2obo$42bo$40b2o118bo$159bobo$159bobo\
39b3o$38bo121bo34bo4bo2bo$37bobo33bo120bo2bo3bo$37bobo32b2o3bo69bo46b\
2obo2b2o$38bo33b2o4bo66b2ob2o44bo6bobo$72b2o4b2o68b2o43bo5bo3bo$73bobo\
2b3o64b3o20bo23bo6b2ob2o$72bo5bo68bo3bo15bobo30bo$25bo44bob5o69bo3bo\
16bobo$24b3o19bo25bo3bo70b3obo16bo$23b2ob2o17bobo21b3o52bo24b2o$24b3o\
18bobo75bobo22bobo$25bo20bo75b2ob2o22bo$25bobo94b2o16b2o6b2o$25b4o99b\
2o9bo2bo4b3o$2bo25bo93b3o2bo12bo2bo2b2ob2o$bobo122bob2o15bo2b3o$o3bo\
19b2ob2o95bo2bo17b2o$bobo19bo5bo97bo11bo$2bo14b3o4bo3bo96b2o11b2o3bo$\
16bo3bo4bo113bo3b2o$2b4o10b3o2bo103bo13bobob2o$bo4bo9bo3bo102b2ob2o11b\
o3b2o$3bo13b3o106bo13b3o$o3bo2bo9b2o104bo16b3o$ob3obo118bo$b3obo2$139b\
o$19bo118b3o$16b5o120bo$15bo122b2ob2o$137b2ob2o$16bo3bo107b2o7b2ob2o$\
17b3o108b2o8bo2bo$139b3o$6b2o131b2o$6b2o4$136b2o$136b2o2$14b2o$14b2o!')

snark = g.parse('18bo$2o14b5o$bo13bo5bo$bobo12b3o2bo$2b2o15bob2o$16b4o2bo$11b2o3bo3b2o$\
11b2o4b3o$19bo$19bob2o$18b2ob2o3$10b2o$10bo$11b3o$13bo!', 389, 78)

finalslider = g.parse('bo$2bo$3o19$43bo$42bobo3$42b3o$42b3o$43bo3$43bo$42b3o$42b3o21b2o$60b2o\
4b2o$60bo$42bobo7b2o3b2obo$43bo7bo3bo3bo$50bo14b3o$50bo3bo2bo7b3o$50bo\
5bo7bo3bo$51bo3bo7bo5bo$52b2o10bo3bo$65b3o5$67b2obo$68b2o5$57b2o$58b2o\
8bo$57bo9b3o$66b5o$65bobobobo$65b2o3b2o2$39bo10bo$39b2o9b2o16bo$34b2o\
4b2o7bobo4bo10bobo$30b2o2b2o4b3o13bobo8bobo$30b2o2b2o4b2o15bobo8bo$39b\
2o16bo2bo7b2o$39bo17bobo8b2o$56bobo3b2o4b2o$56bo5bobo$64bo$64b2o!', 246, 118)

slider = finalslider + snark

glider = g.parse('bo$2o$obo!', 119, 157)

def process(polyn):
	termlist1 = polyn.split('+')
	termlist2 = []
	for terms in termlist1:
		splitterms = terms.split('-')
		signedsplitterms = splitterms[:1]
		for term in splitterms[1:]:
			signedsplitterms.append('-' + term)
		termlist2.extend(signedsplitterms)
	parsedterms = []
	for term in termlist2:
		if 'x' in term:
			if term[0] == 'x':
				term = '1' + term
			if term[:2] == '-x':
				term = '-1' + term.strip('-')
			if 'x^' in term:
				coef_exp = term.split('x^')
				parsedterms.append((Fraction(coef_exp[0]), int(coef_exp[1])))
			else:
				parsedterms.append((Fraction(term.split('x')[0]), 1))
		else:
			parsedterms.append((Fraction(term), 0))
	maxexp = 0
	for termtup in parsedterms:
		if termtup[1] > maxexp:
			maxexp = termtup[1]
	processed = [0] * (maxexp + 1)
	for termtup in parsedterms:
		processed[termtup[1]] += termtup[0]
	return processed

def firstvalues(terms):
	vals = []
	for x in xrange(len(terms)):
		sum = 0
		for exp, coef in enumerate(terms):
			sum += coef * x ** exp
		if sum != int(sum):
			g.warn("Polynomial must produce integer values when x is an integer.")
			g.exit()
			return
		vals.append(int(sum))
	return vals

# Returns a list containing the first term of the polynomial,
# the difference between the first two terms,
# the difference between the first two differences,
# the difference between the first two differences of differences, etc.
# I call these terms the starter constants of a sequence of numbers.
# For more information about these values in relation to x^n sequences, see:
# http://mathandnumberystuff.tumblr.com/tagged/starter-constants
def firstdiffs(values):
	if len(values) < 1:
		g.warn("No polynomial entered, apparently.")
		g.exit()
		return # Just for good measure.
	if len(values) == 1:
		return [values[0]]
	if len(values) > 1:
		diffs = []
		for n in xrange(len(values) - 1):
			diffs.append(values[n + 1] - values[n])
		return firstdiffs(diffs) + [values[0]]

def getvaluefromdiffs(startconsts, n):
	if n + 1 < len(startconsts):
		return getvaluefromdiffs(startconsts[len(startconsts) - n + 1:], n)
	currconsts = [0] * (n - len(startconsts) + 1)
	for sc in startconsts:
		nextconsts = [sc]
		for num, val in enumerate(currconsts):
			nextconsts.append(nextconsts[num] + val)
		currconsts = nextconsts
	return currconsts[n]

polyn = g.getstring("Enter your polynomial (like 1/10x^5+9/10x):")
terms = process(polyn)
values = firstvalues(terms)
startconsts = firstdiffs(values)
for diff in startconsts[:-1]:
	if diff <= 0:
		g.warn("One set of differences in this polynomial is not strictly increasing.")
		g.exit()
offset = startconsts[-1]
sc = startconsts[:-1]

g.new('%s gun' % polyn)
if sc[0] == 1:
	gun = g.parse('bo$2o$obo13$4b2o$2o2b2o$2o2bob2o13bo2bob2obo2bo$5b3o13b4ob2ob4o$21bo2b\
	ob2obo2bo2$5b2o$5b2o31bo24b2o$38b2o23bo$33b2o4b2o13b2o5bobo$29b2o2b2o\
	4b3o11b3o5b2o$29b2o2b2o4b2o9bob2o$38b2o10bo2bo$38bo11bob2o$9b5o28bo10b\
	3o$8bob3obo27bobo9b2o6b2o$9bo3bo28b2o18b2o$10b3o$11bo2$8b2o$9bo$6b3o\
	21b2o$6bo10bo12b2o$15b3o7b2o$14bo9b4o8bo25b3o$14b2o7b2o10b4o22bo3bo$\
	22b2o11bob3o20bo5bo$23bobo13b2o19bo5bo$25bobo10bo24bo$25b3o33bo3bo$26b\
	o35b3o$9b2obob2o9bo37bo$9bo5bo30b3o9b2o$10bo3bo31bo9bo2bo$11b3o27bo5bo\
	7bo7b2o$39b4o12bo6bo2bo$33b2o3bobob2o11bo7b2o$33b2o2bo2bob3o11bo2bo$6b\
	2o30bobob2o14b2o$6bo2bo29b4o$41bo2$6bob2o$b2o2bobo$bo4bo$5bo$2bo2bo!', 119, 157)
	g.putcells(gun)
else:
	gun = g.parse('30b2o$29bobo$28bo6b2o$28bo2bo2bo2bob2o$28bo6b2o2b2o$18b3o8bobo$30b2o$\
	18bobo$17b5o$16b2o3b2o$16b2o3b2o2$30bo$30bobo$33b2o4b2o$33b2o4b2o$33b\
	2o$30bobo$30bo2$17b2o$17b2o6$11b2o$9bo2bo$8bo7b5o$2o6bo6bo5bo$2o6bo7b\
	2o3bo$9bo2bo7bo11b2o$11b2o19bobo10b2o2b2ob2o3b2ob2obo$22b2o8bo12bo2bob\
	obobobobobob2o$18bobo2bo22bobobobobobo3bo$16b3ob2o23b2obob3obob5o6bo\
	11b2o$15bo33b5o12bobo10b2o$16b3ob2o36bo3b2o2bobo$18bob2o35bobo2bo2b2ob\
	2o$57bobo3bobo$50b3o5bob4o2bob2o$51bo8bo3bobob2o$51bo7bo3bobo$58bo3bob\
	o$13b2o43b2o3bo$14bo22b2o$14bobo20bo$15b2o18bobo$35b2o34b2o$71b2o$86b\
	2o$22b3ob4o55bo2bo$21bo2b3o2bo56b2obo$20bo4bo63bo$21bobo2b3o60b2o$23bo\
	b2o47b2o$23b3o49bo$24bo21b2o24b3o$46b2o11b2o11bo$39bo19bo$23b2o15b2o\
	18b3o$19b2o2b2o14b2o21bo$18bobo$18bo$17b2o!', 129, 160) + g.parse('42bo$42b2o$41b2obo$40bo2b3o$39bobobo$38bobobo$36b3o2bo$37bob2o$38b2o$\
	35bo3bo$34bobo$34b2o$38b2o$38bobo$33b2o5bo$33b2o5b2o17$17b2o$17bo$15bo\
	bo$15b2o2$2o$2o2$9b2o$9b2o6b2o$17b2o3$5bo$4bobo$4b2o6b2o$12bo$13b3o$\
	15bo!', 187 + 30*(sc[0] - 2), 213 + 30*(sc[0] - 2))
	gun = g.evolve(gun, 180)
	g.putcells(gun)

usedconsts = [sc[0]]
mainx, mainy = 0, 0
for n, diff in enumerate(sc[1:]):
	if n == len(sc) - 2:
		usedslider = finalslider
	else:
		usedslider = slider
	usedconsts.append(diff)
	repos = diff - 1
	newslider = g.evolve(usedslider, 480*repos)
	g.putcells(maincomp, mainx, mainy)
	ahead = 0
	maketime = 1440*diff - 960
	hittime = 480
	_ = hittime - maketime
	num = 0
	vals = [diff]
	while num <= len(sc) + 1 or _ < 0:
		num += 1
		vals.append(getvaluefromdiffs(usedconsts, num))
		if hittime - maketime < 0:
			ahead += maketime - hittime
			g.run(maketime - hittime)
		maketime = 1440*vals[num] - 1440*diff + 480
		hittime = 960*sum(vals) - 480*vals[num] - 480*diff + 480 + ahead
		_ = hittime - ahead - maketime
	g.putcells(newslider, mainx + 120*repos, mainy + 120*repos)
	mainx += 64
	mainy += -293
	if n != len(sc) - 2:
		g.run(1440)
	g.fit()

#print "A glider is emitted at generation %d + 960n if and only if there is a non-negative integer x such that n = %s." % (int(g.getgen()) + 237 - 960*offset, polyn)