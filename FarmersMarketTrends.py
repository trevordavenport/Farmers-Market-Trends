#URL ='http://www.ams.usda.gov/AMSv1.0/getfile?dDocName=STELPRDC5087258'

import pandas as pd
import csv
import os
import openpyxl as opx
import json
import matplotlib.pyplot as plt
import operator
import numpy as np


from openpyxl import load_workbook
from pandas import DataFrame, read_csv
from IPython.display import HTML
import folium

try:
    import mpld3
    from mpld3 import enable_notebook
    from mpld3 import plugins
    enable_notebook()
except Exception as e:
    print "Attempt to import and enable mpld3 failed", e

DEBUG = False

#Parsing local CSV.
location = r'/Users/alisonmetz/Desktop/WorkingWithOpenData/FarmersMarkets.csv'
df = pd.read_csv(location)
df = pd.DataFrame.from_csv(location)
df.columns

#Find the top5 states with the most farmers markets.
Sorted = df.sort(['State'], ascending=True)
top_states = dict()

for states in Sorted.State:
    if states not in top_states:
        top_states[states] = 1
    else:
        top_states[states] += 1

sorted_top_five = dict(sorted(top_states.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
sorted_bottom_five = dict(sorted(top_states.iteritems(), key=operator.itemgetter(1), reverse=False)[:8])

print "Top Five States :\n", sorted_top_five
print "\nBottom Five States :\n", sorted_bottom_five

#Incorrectly Spelled State Names...
#Way to go Department of Agriculture, remove them.
del sorted_bottom_five['Calafornia']
del sorted_bottom_five['Virigina']
del sorted_bottom_five['Miinesota']

#iPython Command
%matplotlib inline
"""
Matplotlib Top 5 Farmers Market States

"""
states_label = sorted_top_five.keys()
y_pos = np.arange(len(states_label))
#error = np.random.rand(len(people))
number_of_markets = sorted_top_five.values()
plt.barh(y_pos, number_of_markets, align='center', alpha=0.4)
plt.yticks(y_pos, states_label)
plt.xlabel('Farmers Markets per State')
plt.title('Top Five Farmers Market States')
plt.show()

#Sort DataFrame by Top Counties.
County_Sorted = df.sort(['County'], ascending=True)
top_counties = dict()

for counties in County_Sorted.County:
    if counties not in top_counties:
        top_counties[counties] = 1
    else:
        top_counties[counties] += 1

all_counties = dict(sorted(top_counties.iteritems(), key=operator.itemgetter(1), reverse=True))
counties_top_five = dict(sorted(top_counties.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
counties_bottom_five = dict(sorted(top_counties.iteritems(), key=operator.itemgetter(1), reverse=False)[:10])

#All of the included Farmers Market Counties
if(DEBUG): 
	all_counties.keys()
	print(len(all_counties)) #1423 Counties

print "Top Counties with Farmers Markets \n", counties_top_five
print "\nCounties with Least Farmers Markets \n", counties_bottom_five

#Drop all NaN Values from County Field
County_Sorted = County_Sorted[pd.notnull(County_Sorted['County'])]
columns = ["County"]
organized = pd.DataFrame(County_Sorted, columns=columns)
organized.head(20)

#Obesity Rates in Los Angeles County and Farmers Market correlation. 
#http://county-food.findthebest.com/l/3344/Los-Angeles
LA_obesity_rate       = 21.5
LA_markets            = counties_top_five['Los Angeles'] #116 total farmers markets in Los Angeles
Alameda_markets       = all_counties['ALAMEDA']   #2 total farmers markets
SD_markets            = all_counties['San Diego'] #47
Orange_markets        = all_counties['Orange']    #60
Riverside_markets     = all_counties['Riverside'] #18
SB_markets            = all_counties['San Bernardino'] #22
CA_total_markets      = sorted_top_five['California'] #754 total farmers markets in CA
total_farmers_markets = len(County_Sorted) #7,390 Total Farmers Markets

LA_percent = (float(LA_markets)/float(CA_total_markets)) * 100 #15.4
Alameda_percent = (float(Alameda_markets)/float(CA_total_markets)) * 100
SD_percent = (float(SD_markets)/float(CA_total_markets)) * 100
Orange_percent = (float(Orange_markets)/float(CA_total_markets)) * 100
Riverside_percent = (float(Riverside_markets)/float(CA_total_markets)) * 100
SB_percent = (float(SB_markets)/float(CA_total_markets)) * 100

percent_dict = {}
percent_dict['Los Angeles'] = LA_percent
percent_dict['Alameda'] = Alameda_percent
percent_dict['San Diego'] = SD_percent
percent_dict['Orange'] = Orange_percent
percent_dict['Riverside'] = Riverside_percent
percent_dict['San Bernardino'] = SB_percent
print "Total LA County Farmers Markets: ", total_farmers_markets

"""
Matplotlib Top 6 CA Counties and Farmers Market Percentage

"""
#fig = plt.figure()
%matplotlib inline

percent_label = percent_dict.keys()
y_pos = np.arange(len(percent_label))
#error = np.random.rand(len(people))
number_of_markets = percent_dict.values()
plt.barh(y_pos, number_of_markets, align='center', alpha=0.4)
plt.yticks(y_pos, percent_label)
plt.xlabel('County Percentage Per State')
plt.title('Top Six California Counties')

#Add Same bar graph but obesity rates in counties.
obesity_dict = {}
obesity_dict['Los Angeles'] = 21.5
obesity_dict['Alameda'] = 23.0
obesity_dict['Orange'] = 22.0
obesity_dict['San Diego'] = 24.0
obesity_dict['Riverside'] = 27.0
obesity_dict['San Bernardino'] = 28.0

obesity_label = obesity_dict.keys()
x_pos = np.arange(len(obesity_label))
obesity_len = obesity_dict.values()
plt.barh(x_pos, obesity_len, align='center', alpha=0.4)
plt.yticks(x_pos, obesity_label)
plt.xlabel('County Percentage Per State')
plt.title('Top Six California Counties')
#plt.legend( (number_of_markets, obesity_len), ("Obesity", "Density"))
plt.show()

#Number of Fast Food Restaurants Per State
#http://www.businessinsider.com/this-interactive-map-shows-exactly-how-many-fast-food-restaurants-there-are-in-every-state-2012-1
CA_fast_food = 27120
NY_fast_food = 17461
MI_fast_food = 7005
OH_fast_food = 7137
IL_fast_food = 8790
N = 5
farmers_markets = (sorted_top_five['California'], sorted_top_five['New York'], sorted_top_five['Michigan'],
                   sorted_top_five['Ohio'], sorted_top_five['Illinois'])
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, farmers_markets, width, color='r')

fast_food = [CA_fast_food, NY_fast_food, MI_fast_food, OH_fast_food, IL_fast_food]
rects2 = ax.bar(ind+width, fast_food, width, color='y')

ax.set_ylabel('Total')
ax.set_title('Fast Food Vs. Farmers Markets')
ax.set_xticks(ind+width)
x = ("California", "New York", "Michigan", "Ohio", "Illinois")
ax.set_xticklabels( x )
ax.legend( (rects1[0], rects2[0]), ('FarmersMarkets', 'FastFood') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
plt.show()

"""
Percentage of Farmers Markets Per 100 Fast Food Joints

"""
ca = float((sorted_top_five['California']) / float(CA_fast_food)) * 100
ny = float((sorted_top_five['New York']) / float(NY_fast_food)) * 100
mi = float((sorted_top_five['Michigan']) / float(MI_fast_food)) * 100
oh = float((sorted_top_five['Ohio']) / float(OH_fast_food)) * 100
il = float((sorted_top_five['Illinois']) / float(IL_fast_food)) * 100
percentage_df = pd.DataFrame([ca,ny,mi,oh,il], columns=["% of Farmers Markets per 100 Fast Food"], index=['CA', 'NY', 'MI', 'OH', 'IL'])
percentage_df

"""
California -> 35:1 Ratio (Fast Food / Farmers Markets)
New York -> 27:1 Ratio (Fast Food / Farmers Markets)
Michigan -> 22:1 Ratio (Fast Food / Farmers Markets)
Ohio -> 24:1 (Fast Food / Farmers Markets)
Illinois -> 26:1 (Fast Food / Farmers Markets)

"""