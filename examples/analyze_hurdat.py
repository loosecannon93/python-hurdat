#!/usr/bin/python 

# W. Cannon Matthews III 
# CMSC 16200
# Exercise 08A
# 01/27/13


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




# process the *more* manipulated data    
years2 = defaultdict(int) 
for storm in storms:
    dtf_days = storm.damage_trans_days()
    years2[storm.date.year] += dtf_days

sorted_years2 = sorted(years2.iteritems(), key=itemgetter(1))

with open('hurdat_dtf.dat','w') as fh :
    for year in  sorted_years2 :
        fh.write( "%d  %d\n" % year  )
        
(m,b,r,p,err) = stats.linregress(years2.keys(), years2.values() ) 
f1x = "f1(x) = {slope}*x + {intercept}".format(slope=m,intercept=b)

with open('hurdat.gnuplot2','w') as fh :
    fh.write("""
    set xr [1850:2015]
    set yr [0:400]
    {func}
    plot f1(x) , \
         'hurdat_dtf.dat' using 1:2 title 'Manipulated' with points
    load 'save.plt'
    !mv my-plot.ps doctored.ps
    """.format(func=f1x))


# lets make one plot with both next to each other         
with open('hurdat.gnuplot','w') as fh :
    fh.write("""
        set xr [1850:2015]
        set yr [0:400]
        {func1}
        {func2}
        plot f1(x) , 'hurdat_dtf.dat' using 1:2 title 'Manipiulated' with points , \\
             f2(x) , 'hurdat_ss_days.dat' using 1:2 title 'Raw' with points
        load 'save.plt' 
        !mv my-plot.ps combined.ps
       """.format(func1=f1x, func2=f2x))          
