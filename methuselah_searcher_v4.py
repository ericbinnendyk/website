# Updated to Python 3

import golly as g
import os

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
    return n1 * n2 // gcd(n1, n2)

def print_soup(f, soup):
    soup_in_better_format = [(soup[2*i], soup[2*i + 1]) for i in range(len(soup)//2)]
    for i in range(16):
        for j in range(16):
            if (j, i) in soup_in_better_format:
                f.write('o')
            else:
                f.write('.')
        f.write('\n')

if not os.path.exists('methuselah-searcher/'):
    try:
        os.makedirs('methuselah-searcher/')
    except:
        g.exit('Unable to create directory %s' % 'methuselah-searcher/')

#rawentry1 = g.getstring("Enter the most common naturally occurring periods of oscillators, spaceships, and infinite growth patterns in this rule separated by commas (no spaces):")
rawentry2 = g.getstring("What is the maximum number of generations to run each soup?")
rawentry3 = g.getstring("How many soups do you want to test?")

#periodlist = map(int, rawentry1.split(','))
periodlist = [2]
maxgens = int(rawentry2)
soups = int(rawentry3)
maxperiod = 3072

rulestr = g.getrule().replace('/', '').lower()
periods = [] # population periods found in soup but considered less-common periods
lgrowth = []

totalperiod = 1
for period in periodlist:
    totalperiod = lcm(period, totalperiod)

# find less-common periods from previous run
if os.path.exists('methuselah-searcher/%s/new_periods.txt' % rulestr):
    periods_f = open('methuselah-searcher/%s/new_periods.txt' % rulestr, 'r')
    for line in periods_f:
        if line.startswith('period'):
            # obtain period from log file
            period_str = line[7:]
            i = 0
            for ch in period_str:
                if ch not in '0123456789':
                    break
                i += 1
            period_str = period_str[:i]
            period = int(period_str)
            # if period is a factor of the total period to be checked, we don't need to save it.
            if totalperiod % period != 0:
                periods.append(period)
    periods_f.close()

record = 0
# find previous record
if os.path.exists('methuselah-searcher/%s/records.txt' % rulestr):
    records_f = open('methuselah-searcher/%s/records.txt' % rulestr, 'r')
    for line in records_f:
        if line.startswith('gens'):
            # obtain record from log file
            gens_str = line[5:]
            i = 0
            for ch in gens_str:
                if ch not in '0123456789':
                    break
                i += 1
            gens_str = gens_str[:i]
            gens = int(gens_str)
            if gens > record:
                record = gens
    records_f.close()

longest = [], record # current longest-lasting soup

if not os.path.exists('methuselah-searcher/%s' % rulestr):
    try:
        os.mkdir('methuselah-searcher/%s' % rulestr)
    except:
        g.exit('Unable to create directory %s' % ('methuselah-searcher/%s' % rulestr))

records_f = open('methuselah-searcher/%s/records.txt' % rulestr, 'a')
periods_f = open('methuselah-searcher/%s/new_periods.txt' % rulestr, 'a')
lgrowth_f = open('methuselah-searcher/%s/linear_growth.txt' % rulestr, 'a')

for soupnum in range(soups):
    g.new('')
    # create a random soup and get the cell list for it
    g.select([0,0,16,16])
    g.randfill(50)
    currsoup = g.getcells([0,0,16,16])
    
    totalgens = 0
    sameaslast = 0
    prevgens = [0] * totalperiod
    increase_defined = False
    success = False
    # Run for totalgens plus the smallest number divisible by totalperiod greater than 2048
    while totalgens < maxgens + totalperiod*((2048 / totalperiod) + 1):
        thesegens = []
        for gen in range(totalperiod):
            thesegens.append(int(g.getpop()))
            g.run(1)
        totalgens += totalperiod
        if not increase_defined:
            increase = thesegens
            increase_defined = True
        else:
            new_increase = list(map(lambda x, y: x - y, thesegens, prevgens))
            if new_increase == increase:
                sameaslast += 1
            else:
                sameaslast = 0
            increase = new_increase
        if sameaslast > 2048 / totalperiod:
            # We assume it's stabilized because the population has been periodic for over 2048 generations
            success = True
            totalgens -= totalperiod * (sameaslast + 1)
            # check if stabilization time is record high and report it
            if totalgens > longest[1]:
                longest = currsoup, totalgens
                records_f.write("gens=%d\n" % totalgens)
                print_soup(records_f, currsoup)
                records_f.write('\n')
            break
        prevgens = thesegens
    # Population hasn't stabilized in maxgens into any factor of the predicted period
    if not success:
        # Store populations for 2*maxperiod + 1 consecutive generations in a list
        populations = []
        for gen in range(2 * maxperiod + 1):
            populations.append(int(g.getpop()))
            g.run(1)
        itworks = False
        # check periods in the list of less-common seen periods
        for period in periods:
            for phasenum in range(period):
                itworks = True
                popdiff = populations[phasenum + 1] - populations[phasenum]
                phasenum += period
                while phasenum < 2 * maxperiod:
                    if popdiff != populations[phasenum + 1] - populations[phasenum]:
                        itworks = False
                        break
                    phasenum += period
                if not itworks:
                    break
            if itworks:
                break
        if itworks:
            # less-common but previously seen periodicity detected
            continue
        # check all other periods now
        for period in range(1, maxperiod + 1):
            '''if period in periods or totalperiod % period == 0:
                continue''' # it might oscillate with a common period, just take quite a long time to stabilize
            itworks = True
            for phasenum in range(period):
                popdiff = populations[phasenum + 1] - populations[phasenum]
                phasenum += period
                while phasenum < 2 * maxperiod:
                    if popdiff != populations[phasenum + 1] - populations[phasenum]:
                        itworks = False
                        break
                    phasenum += period
                if not itworks:
                    break
            if itworks:
                break
        if itworks:
            # periodicity detected
            if totalperiod % period != 0:
                # oscillates with an uncommon period
                increase = populations[period] - populations[0]
                '''message = "Found a new period of population! %d." % period
                if increase != 0:
                    message += " Linear growth at rate %d/%d cells per gen." % (increase, period)
                else:
                    message += " Bounded growth."
                g.show(message)
                g.new('')
                g.putcells(currsoup)'''
                # save the new period and continue searching
                periods_f.write("period=%d bounded=%s\n" % (period, 'y' if increase == 0 else 'n'))
                print_soup(periods_f, currsoup)
                periods_f.write('\n')
                # also save the period to the less-common periods list to remember checking it in the future
                periods.append(period)
                '''g.exit() # for now.'''
            else:
                # oscillates with a common period. the only reason it wasn't detected earlier was because it took too long to stabilize.
                if maxgens > longest[1]:
                    longest = currsoup, maxgens
        else:
            # periodicity not detected. assume the soup still hasn't stabilized and report it.
            g.new('')
            g.putcells(currsoup)
            g.show("Found soup unstable after %d generations." % maxgens)
            break
    g.show("Searched %d soups; longest lifespan ~%d" % (soupnum + 1, longest[1]))
    g.update()

if success:
    # managed to detect stabilization of every soup searched, reporting longest result unless previous longer one has been found
    g.new('')
    if longest[0] == []:
        g.show("Search complete. Nothing found lasting longer than previous record of %d generations." % longest[1])
    else:
        g.putcells(longest[0])
        g.show("Found soup stabilizing after ~%d generations" % longest[1])

records_f.close()
periods_f.close()
lgrowth_f.close()
