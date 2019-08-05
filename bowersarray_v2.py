# This is another Bowers Array evaluating program I made for Jonathan Bowers' birthday!
# And like the previous one, I will probably be updating it with new features in the following days,
# so it can run longer and take more shortcuts before it starts decrimenting an incredibly huge number by one each time enter is pressed.
# .ui mi djica lo nu la'o gy. Jonathan Bowers .gy cu se jbedetnunsla

def subarray_string(sub):
	string = '{'
	for index, num in enumerate(sub):
		string += str(num)
		if index != len(sub) - 1:
			string += ', '
	string += '}'
	return string

def array_string(a, a_num):
	string = '{\n'
	for index, sub in enumerate(a):
		string += subarray_string(sub)
		if index + 1 != len(a):
			string += ', \n'
		else:
			string += '}'
	return string

def print_array(a, a_num):
	print 'A%d = ' % a_num + array_string(a, a_num)
	raw_input()

def find_pilot(a):
	pilotindex = 0
	for num in a:
		if num == 1:
			pilotindex += 1
		else:
			break
	
	return pilotindex

def copy_list(a):
	b = a[:]
	for index, sub in enumerate(b):
		b[index] = sub[:]
	
	return b

def step_eval(a, a_num):
	print "This time when we go into the function, the whole array is equal to %s" % str(a)
	#We're assuming the array has been trimmed of all its excess 1's. (This process continues happening in this very function.)
	if len(a[0]) <= 2:
		index = 1
		for sub in a[1:]:
			if len(sub) != 0:
				break
			index += 1
	else:
		index = 0
		sub = a[0]
	
	print "First one."
	print_array(a, a_num)
	
	if index == 0:
		pilotindex = find_pilot(sub[2:]) + 2
	else:
		pilotindex = find_pilot(sub)
	
	b = copy_list(a)
	subb = b[index]
	b[0][1] -= 1
	
	sub[pilotindex] -= 1
	
	if (len(sub) - 1 == pilotindex) and (sub[pilotindex] == 1):
		del sub[pilotindex]
	
	if (len(a) - 1 == index) and (a[index] == []):
		del a[index]
	
	for i in xrange(1, pilotindex - 1):
		print "Setting sub[%d] to %d." % (index, a[0][0])
		sub[index] = a[0][0]
	
	for i in xrange(0, index):
		a[i] = [a[0][0]] * a[0][1]
	
	if pilotindex > 0:
		sub[pilotindex - 1] = 'A%d' % (a_num + 1)
		print "Second one. We just set sub[%d] to %s." % (pilotindex - 1, sub[pilotindex - 1])
		print_array(a, a_num)
		
		sub[pilotindex - 1] = eval_array(b, a_num + 1)
	
	return a

def eval_array(a, a_num):
	if len(a) == 0:
		return 1
	
	if len(a) == 1 and len(a[0]) == 1:
		return a[0]
	
	if a[0][1] == 1:
		print 'A%d = ' % a_num + array_string(a, a_num) + ' = %d' % a[0][0]
		raw_input()
		return a[0][0]
	
	while len(a) > 1 or len(a[0]) > 2:
		a = step_eval(a, a_num)
	print 'A%d = ' % a_num + array_string(a, a_num) + ' = %d^%d' % (a[0][0], a[0][1])
	raw_input()
	return a[0][0] ** a[0][1]

print "Welcome to Eric's ALL-NEW Array Manager! This program will evaluate Bowers arrays even better than before!"

a = []
sub = []

entry = input("Let's get started!\nEnter the first member of your array, A0\n(or 0 to go to the next row, or a non-positive number to finish): ")

while entry >= 0:
	while entry > 0:
		sub.append(entry)
		entry = input("Enter the next member of A0, 0 to go to the next row, or a non-positive number to finish: ")
	
	while sub[-1] == 1:
		del sub[-1]
		if len(sub) == 0:
			break
	
	a.append(sub)
	if entry < 0:
		break
	
	sub = []
	entry = input("Enter the next member of A0, 0 to go to the next row, or a non-positive number to finish: ")

while a[-1] == []:
	del a[-1]
	if len(a) == 0:
		break

print "Your array is: " + array_string(a, 0)
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