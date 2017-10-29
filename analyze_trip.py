import pandas as pd 
import numpy as np
from numpy import linalg 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.linalg
import random
import math

### Read the csv files for training and test set 
### The file is structured in the following way:
### -Each line contains a different restaurant
### -First column name of the restaurant
### -Second column type of cuisine (some mistakes, the scraper should be improved)
### -All the other columns contain the different langauges supported by TripAdvisor

trip=pd.read_csv("restaurants.csv")


print ("Data set shape {}".format(trip.shape))
print ('!-----------------------!')
print trip.head()
print ('!-----------------------!')
print trip.info()

### Searching for different types of cuisines

k=[]
cuisine=trip['Cuisine']
for i in cuisine:
    j = i.replace(' ','')
    k.append(j)
trip['Cuisine']=k

repl_dic = {'': np.NaN}
trip['Cuisine'].replace(repl_dic, inplace=True)
repl_dic = {'Searchingforavail': np.NaN}
trip['Cuisine'].replace(repl_dic, inplace=True)

# Number of unique types of cuisine

print ('!-----------------------!')
print "Number of different types of cuisine"
print trip['Cuisine'].nunique()

print ('!-----------------------!')
print "Different types of cuisine"
print trip['Cuisine'].unique()

### Plotting a barplot for the 12 most popular types of cuisines vs. the number of corresponding restaurants

trip['Cuisine'].value_counts()[:12].plot(kind="bar")
plt.ylabel('Number of restaurants')
plt.title('12 most popular cuisines in Paris vs. the number of corresponding restaurants')
plt.tight_layout()
plt.show()


### Searching for the number of reviews for each language
 
lang=list(trip.columns)[2:]
langi=range(12)
nrev=[]

for i in lang:
    print i,trip[i].sum()
    nrev.append(trip[i].sum()) 

langorder=sorted(range(len(nrev)), key=lambda k: nrev[k], reverse=True)
nrev.sort(reverse=True)
lang = [ lang[i] for i in langorder ]
print lang

### Barplotting the 12 most used languages vs. the number of reviews

plt.bar(langi[:12], nrev[:12], align="center")
plt.xticks(langi, lang, rotation='vertical')
plt.xlim(-0.7,11.7)
plt.ylabel('Number of reviews')
plt.title('12 most used languages vs. number of reviews')
plt.tight_layout()
plt.show()

### Dividing the total number of restaurants in 4 different groups and plotting them:
### 1: > 1000 reviews; 2: 100 to 1000 reviews; 3: 10 to 100 reviews; 4: < 10 reviews

resto=list(trip['Name'])

nrev=np.zeros(4)
trip['sumrev']=trip.sum(axis=1,numeric_only=True)
trip['> 1000']=trip['sumrev']>=1000
trip['100-1000']=((trip['sumrev']<1000) & (trip['sumrev']>=100))
trip['10-100']=((trip['sumrev']<100) & (trip['sumrev']>=10))
trip['< 10']=trip['sumrev']<10
print trip['100-1000']

nrev=np.zeros(4)
nrev[0]=trip['> 1000'].sum(axis=0)
nrev[1]=trip['100-1000'].sum(axis=0)
nrev[2]=trip['10-100'].sum(axis=0)
nrev[3]=trip['< 10'].sum(axis=0)

rang=['> 1000','100-1000','10-100','< 10']
rangi=range(4)

plt.bar(rangi, nrev, align="center")
plt.xticks(rangi, rang, rotation='vertical')
plt.xlabel('Number of reviews')
plt.ylabel('Number of restaurants')
plt.title('Number of restaurants by number of reviews')
plt.tight_layout()
plt.show()

### Looking for the restaurants that are preferred by the locals (the Parisians)
### This could help a person visiting Paris to find less touristic restaurants and experience some real French flavors
### At this stage the best restaurants are ranked according to the highest percentage of reviews written in French
### To avoid bias only restaurants with more than 100 reviews are considered
### This is done to avoid a restaurant with only one review (or few reviews) to be ranked first
### This ranking will be improved by keeping into account other parameters (for example, the customer satisfaction)  

### The plot shows the 12 restaurants with the highest percentage of reviews in French (decreasing top to bottom)
### The blue bar indicates the total number of reviews
### The red bar indicates the number of reviews in French 

fav_fr=(trip['French']/trip['sumrev']*100).where(trip['100-1000'] | trip['> 1000'])
fav_fr=fav_fr.fillna(0)
fav_fr=list(fav_fr)
name_fr=list(trip['Name'])
rev_fr=list(trip['French'])
tot_fr = list(trip['sumrev'])

frorder=sorted(range(len(fav_fr)), key=lambda k: fav_fr[k], reverse=True)
fav_fr.sort(reverse=True)
name_fr = [name_fr[i] for i in frorder]
rev_fr = [rev_fr[i] for i in frorder]
tot_fr = [tot_fr[i] for i in frorder]

print fav_fr[:12]
print name_fr[:12]

fri=list(reversed(range(12)))
plt.barh(fri[:12], tot_fr[:12], align="center")
plt.barh(fri[:12], rev_fr[:12], align="center", color='red')
plt.legend(('Total reviews','Reviews in French'), bbox_to_anchor=(1,0.7))
plt.yticks(fri, name_fr)
plt.ylim(-1.,)
plt.xlabel('Number of reviews')
plt.title('Top 12 restaurants with the highest percentage of reviews in French')
plt.grid(True)
tot_fr_rev=list(reversed(tot_fr[:12]))
for i, v in enumerate(list(reversed(fav_fr[:12]))):
    plt.text(tot_fr_rev[i]+10, i-0.1, str(np.round(v,1))+'%', color='black', fontweight='bold')
plt.tight_layout()
plt.show()


### Looking for the Italian restaurant that is preferred by Italians
### This could help an Italian visiting Paris to find a restaurant that tastes like home
### Similarly, also non-Italians might be interested in experiencing authentic Italian flavors
### At this stage the best restaurants are ranked according to the highest percentage of reviews written in Italian
### To avoid bias only restaurants with more than 100 reviews are considered
### This is done to avoid a restaurant with only one review (or few reviews) to be ranked first
### This ranking will be improved by keeping into account other parameters (for example, the customer satisfaction) 

### The plot shows the 12 restaurants with the highest percentage of reviews in Italian (decreasing top to bottom)
### The green bar indicates the total number of reviews
### The red bar indicates the number of reviews in Italian 

fav_ital=(trip['Italian']/trip['sumrev']*100).where(trip['100-1000'] | trip['> 1000']) 
fav_ital=fav_ital.fillna(0)
fav_ital=list(fav_ital)
name_ital=list(trip['Name'])
rev_ital=list(trip['Italian'])
tot_ital = list(trip['sumrev'])

italorder=sorted(range(len(fav_ital)), key=lambda k: fav_ital[k], reverse=True)
fav_ital.sort(reverse=True)
name_ital = [name_ital[i] for i in italorder]
rev_ital = [rev_ital[i] for i in italorder]
tot_ital = [tot_ital[i] for i in italorder]

print fav_ital[:12]
print name_ital[:12]

itali=list(reversed(range(12)))
plt.barh(itali[:12], tot_ital[:12], align="center")
plt.barh(itali[:12], rev_ital[:12], align="center", color='green')
plt.legend(('Total reviews','Reviews in Italian'),bbox_to_anchor=(1,0.45))
plt.yticks(itali, name_ital)
plt.ylim(-1.,)
plt.xlabel('Number of reviews')
plt.title('Top 12 restaurants with the highest percentage of reviews in Italian')
plt.grid(True)
tot_ital_rev=list(reversed(tot_ital[:12]))
for i, v in enumerate(list(reversed(fav_ital[:12]))):
    plt.text(tot_ital_rev[i]+10, i-0.1, str(np.round(v,1))+'%', color='black', fontweight='bold')
plt.tight_layout()
plt.show()

