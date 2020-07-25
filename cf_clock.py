import time
import calendar
import fractions
import math

def cf_decompose(frac):
    if frac == 0:
        return (None, None)
    pc = math.floor(1 / frac)
    return (pc, 1 / frac - pc)

while True:
    year = time.gmtime().tm_year
    #begin_year = time.struct_time(tm_year=year, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0)
    begin_year = time.strptime(str(year), '%Y')
    begin_sec = int(calendar.timegm(begin_year))
    seconds = int(time.time())
    #begin_next_year = time.struct_time(tm_year=year+1, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0)
    begin_next_year = time.strptime(str(year + 1), '%Y')
    begin_next_sec = int(calendar.timegm(begin_next_year))
    secs_in_year = begin_next_sec - begin_sec
    secs_through_year = seconds - begin_sec

    print("We are {} out of {} seconds through the year".format(secs_through_year, secs_in_year))

    year_frac0 = fractions.Fraction(secs_through_year - 1, secs_in_year)
    year_frac1 = fractions.Fraction(secs_through_year, secs_in_year)
    year_frac2 = fractions.Fraction(secs_through_year + 1, secs_in_year)

    pcs = [0]
    while True:
        (pc0, year_frac0) = cf_decompose(year_frac0)
        (pc1, year_frac1) = cf_decompose(year_frac1)
        (pc2, year_frac2) = cf_decompose(year_frac2)
        pcs.append(pc1)
        if pc0 == None or pc1 == None or pc2 == None or (pc1 != pc0 and pc1 != pc2):
            break

    print(pcs)
    time.sleep(1)
