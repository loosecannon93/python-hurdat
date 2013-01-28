#/usr/bin/python 

# W. Cannon Matthews III 
# CMSC 16200
# Exercise 08A
# 01/27/13


import datetime
import re

def knots_to_mph(knots) :
    return knots*1.15078
def mph_to_sscat(mph) :
    if mph < 74 : 
        return 0 
    elif mph>=74 and mph<96:
        return 1
    elif mph>=96 and mph<111:
        return 2
    elif mph>=111 and mph<131: 
        return 3 
    elif mph>=131 and mph<156 :
        return 4
    elif mph >= 156:
        return 5 
#dft #3
def damage_transfer(sscat) :
    if sscat == 0 :
        damage = 0
    elif sscat == 1 :
        damage = 1 
    elif sscat == 2 :
        damage = 1.1 
    elif sscat == 3 : 
        damage = 1.2
    elif sscat == 4 :
        damage = 1.3 
    elif sscat == 5 :
        damage = 1.4 
    return damage  
#dtf #2
#def damage_transfer(sscat) :
#    if sscat == 0 :
#        damage = 0.5
#    elif sscat == 1 :
#        damage = 1 
#    elif sscat == 2 :
#        damage = 1.5 
#    elif sscat == 3 : 
#        damage = 2.0
#    elif sscat == 4 :
#        damage = 2.5 
#    elif sscat == 5 :
#        damage = 3.0 
#    return damage  
#dtf #1
#def damage_transfer(sscat) :
#    if sscat == 0 :
#        damage = 0.5
#    elif sscat == 1 :
#        damage = 1 
#    elif sscat == 2 :
#        damage = 2.5 
#    elif sscat == 3 : 
#        damage = 4.5
#    elif sscat == 4 :
#        damage = 6.5 
#    elif sscat == 5 :
#        damage = 10 
#    return damage  

# parse _everything_ incase i wanted to incorporate it into more analysis, ended up not but have this anyway
class QuarterlyRecord:
    def __init__(self,stage,lat,long,wind,press)  :
        self.stage = stage 
        self.lat = lat 
        self.long = lat
        self.wind = wind
        self.press = press 

class DailyData : 
    def __init__(self,date,quarters) : 
        self.date = date
        self.quarters = quarters

class Storm : 
    def __init__(self,date,days,s_number,total_num,name,us_hit,hit_cat):
        self.date = date
        self.days = days
        self.s_number = s_number 
        self.total_num = total_num 
        self.name = name 
        self.us_hit = us_hit
        self.hit_cat = hit_cat    
        self.daily_data = []
    def log_day(self,daily_record) :
        self.daily_data.append(daily_record) 
    def log_trailer(self,max_intensity,hit_states) :
        self.max_intensity = max_intensity
        self.hit_states = hit_states
    def saffir_simpson_days(self) :
        ssdays = 0.0
        for day in self.daily_data : 
            for key in day.quarters :
                sss = mph_to_sscat(knots_to_mph(day.quarters[key].wind))
                ssdays += sss/4.0 
        return ssdays 
    def damage_trans_days(self): 
        dtfdays = 0.0
        for day in self.daily_data : 
            for key in day.quarters : 
                dtf = damage_transfer(mph_to_sscat(knots_to_mph(day.quarters[key].wind)))
                dtfdays += dtf/4.0  
        return dtfdays        
                
                

# this fucntion parses the file, returns a list of all the storms
# parses every field in the data file
def parse() : 
    storms = []
    hurdat = open("hurdat.txt") 
    eof = False 
    while not eof : 
        line = hurdat.readline()
        if line == '' : 
            eof =True 
            break 
        header = {}
        card_num = int( line[0:5] ) 
        header['date'] = datetime.datetime.strptime(line[6:16],"%m/%d/%Y").date()
        header['days']  = int( line[19:21] )  
        header['s_number'] = int( line[22:24] ) 
        header['total_num'] = int( line[30:34] )
        header['name'] = line[35:47].strip()
        header['us_hit'] = ( line[52] == '1') 
        header['hit_cat'] = int( line[58] )

        storm = Storm(**header) 
        for day in range(header['days']) :
            line = hurdat.readline()
            day = {} 
            day['date'] = datetime.datetime.strptime(line[6:11],"%m/%d").date()#.replace(year=header['date'].year()) 

            z00 = {}
            z00['stage'] = line[11]
            z00['lat'] = float(line[12:15])/10
            z00['long']= float(line[15:19])/10 
            z00['wind']= int(line[19:23])
            z00['press']= int(line[23:28])

            z06 = {}
            z06['stage'] = line[28]
            z06['lat'] = float(line[29:32])/10
            z06['long']= float(line[32:36])/10 
            z06['wind']= int(line[36:40])
            z06['press']= int(line[40:45])

            z12 = {}
            z12['stage'] = line[45]
            z12['lat'] = float(line[46:49])/10
            z12['long']= float(line[49:53])/10 
            z12['wind']= int(line[53:57])
            z12['press']= int(line[57:62])
            
            z18 = {}
            z18['stage'] = line[62]
            z18['lat'] = float(line[63:66])/10
            z18['long']= float(line[66:70])/10 
            z18['wind']= int(line[70:74])
            z18['press']= int(line[74:79])

            day['quarters'] = {}
            day['quarters']['z00'] = QuarterlyRecord(**z00)
            day['quarters']['z08'] = QuarterlyRecord(**z06)
            day['quarters']['z12'] = QuarterlyRecord(**z12)
            day['quarters']['z18'] = QuarterlyRecord(**z18)
            storm.log_day( DailyData(**day) )
        line = hurdat.readline()
        trailer = {}
        trailer['max_intensity'] = line[6:8]
        trailer['hit_states'] = []
        for match in  re.finditer('(...)(\d)', line[8:].strip() ):
            trailer['hit_states'].append(match.group(1,2)) 
        storm.log_trailer(**trailer) 
        storms.append(storm) 
    return storms
