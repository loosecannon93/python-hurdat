#!/usr/bin/python 


import hurdat
from collections import defaultdict
from operator import itemgetter
from scipy import stats

storms = hurdat.parse()

# process the "raw" storms based on the saf-simp scale hours     
years = defaultdict(int) 

for storm in storms:
    ss_days = storm.saffir_simpson_days()
    years[storm.date.year] += ss_days

sorted_years = sorted(years.iteritems(), key=itemgetter(1))

with open('hurdat_ss_days.dat','w') as fh :
    for year in  sorted_years :
        fh.write("%d  %d \n" % year  )

# do a regression         
(m,b,r,p,err) = stats.linregress(years.keys(), years.values() ) 
f2x = "f2(x) = {slope}*x + {intercept}".format(slope=m,intercept=b)

with open('hurdat.gnuplot1','w') as fh :
    fh.write(""" 
    set xr [1850:2015]
    set yr [0:400]
    {func}
    plot f2(x) ,\
    'hurdat_ss_days.dat' using 1:2 title 'Raw' with points
    load 'save.plt'
    !mv my-plot.ps raw.ps
    """.format(func=f2x)) 


