# This is another Bowers Array evaluating program I made for Jonathan Bowers' birthday!
# And like the previous one, I will probably be updating it with new features in the following days,
# so it can run longer and take more shortcuts before it starts decrimenting an incredibly huge number by one each time enter is pressed.
# .ui mi djica lo nu la'o gy. Jonathan Bowers .gy cu se jbedetnunsla

def array_string(a):
	string = '{'
	for index, num in enumerate(a):
		string += str(num)
		if index != len(a) - 1:
			string += ', '
	string += '}'
	return string

def print_array(a, a_num):
	string = 'A%d = ' % a_num + array_string(a)
	print string
	raw_input()


def find_pilot(a):
	pilotindex = 2
	for num in a[2:]:
		if num == 1:
			pilotindex += 1
		else:
			break
	
	return pilotindex

def eval_array(a, a_num):
	if len(a) == 0:
		return 1
	
	if len(a) == 1:
		return a[0]
	
	while len(a) > 2:
		print_array(a, a_num)
		if a[1] == 1:
			return a[0]
		
		pilotindex = find_pilot(a)
		
		b = a[:]
		b[1] -= 1
		
		a[pilotindex] -= 1
		
		if (len(a) - 1 == pilotindex) and (a[pilotindex] == 1):
			del a[pilotindex]
		
		for index in xrange(1, pilotindex - 1):
			a[index] = a[0]
		
		a[pilotindex - 1] = 'A%d' % (a_num + 1)
		print_array(a, a_num)
		
		a[pilotindex - 1] = eval_array(b, a_num + 1)
	
	print 'A%d = ' % a_num + array_string(a) + ' = %d^%d' % (a[0], a[1])
	raw_input()
	return a[0] ** a[1]

print "Welcome to Eric's ALL-NEW Array Manager! This program will evaluate Bowers arrays even better than before!"

a = []

entry = input("Let's get started!\nEnter the first member of your array, A0 (or a non-positive number to finish): ")

while entry > 0:
	a.append(entry)
	entry = input("Enter the next member of A0, or a non-positive number to finish: ")

while a[-1] == 1:
	del a[-1]

print "Your array is: " + array_string(a)
print "Now it's time to EVALUATE your array!!! After each step, press enter to go to the next one!"

value = eval_array(a, 0)
print "Your array has finished evaluating. Its value is: %d\n" % value
raw_input()

print "Of course we're happy with the value you got, but it doesn't convey the"
print "true potential of Bowers Exploding Array Function."
print "If you really want to get an inkling of how EXPLOSIVE this function is,"
print "restart the program and try to find an array whose evaluation runs into"
print "a very large number and starts decrementing it by 1, or freezes trying"
print "to finish evaluating an array because it involves exponentiation of"
print "numbers too large to handle."
raw_input()

print "I would like to wish a happy 47th birthday to Jonathan Bowers. He has"
print "revolutionized the fields of polytopes and large numbers, and he is now"
print "working on searching regiments of dimensions 6 and up. His contributions"
print "to mathematical fields are immeasurable."