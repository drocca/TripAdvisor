import requests
from bs4 import BeautifulSoup
import locale
import numpy as np
import re

### For the Tripadvisor page of Paris restaurants this script extract:
### -The name of each restaurant 
### -The type of cuisine of each restaurant (still a bit buggy)
### -The number of reviews in each language for each restaurant

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

lan_list = ["French", "English", "Italian", "Chinese", "Arabic", "Czech", "Danish", "Dutch", "German", "Greek", "Hebrew", "Hungarian", "Indonesian", "Japanese", "Korean", "Norwegian", "Polish", "Portuguese", "Russian", "Serbian", "Slovak", "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese"]

lan_n = len(lan_list)

lan_l_recompile=[re.compile("French"), re.compile("English"), re.compile("Italian"), re.compile("Chinese"), re.compile("Arabic"), re.compile("Czech"), re.compile("Danish"), re.compile("Dutch"), re.compile("German"), re.compile("Greek"), re.compile("Hebrew"), re.compile("Hungarian"), re.compile("Indonesian"), re.compile("Japanese"), re.compile("Korean"), re.compile("Norwegian"), re.compile("Polish"), re.compile("Portuguese"), re.compile("Russian"), re.compile("Serbian"), re.compile("Slovak"), re.compile("Spanish"), re.compile("Swedish"), re.compile("Thai"), re.compile("Turkish"), re.compile("Vietnamese")] 

for i in range(0, 14760, 30):
	tmp_url = 'https://www.tripadvisor.com/Restaurants-g187147-oa'+str(i)+'-Paris_Ile_de_France.html#EATERY_OVERVIEW_BOX'
	r = requests.get(tmp_url)
	soup = BeautifulSoup(r.content, "lxml")

	for link in soup.find_all('a', class_="property_title"):
#    print(link.get('href'))
	    resto_url='https://www.tripadvisor.com'+link.get('href')
#    print resto_url
	    resto = requests.get(resto_url)
	    soup_resto = BeautifulSoup(resto.content, "lxml")
	    name = soup_resto.find_all("title")
	    namer = name[0].get_text().split(',')[0]
	    typet = soup_resto.find_all("div", class_="text")
	    if (len(typet)!=0): 
		typer = typet[-1].get_text().split(',')[0]
	    else:
		typer = " "
#	    print namer
#	    print typer
#    print name.get_text()
	    lnnum = np.zeros(lan_n) 
	    for language in soup_resto.find_all("label", string=lan_l_recompile): #, for="taplc_location_review_filter_controls_0_filterLang_more_it"): 
#	print language
	        txt=language.get_text()
	        splt=txt.split(' ')
	        splt[-1] = splt[-1].encode("utf-8")
	        splt[0] = splt[0].encode("utf-8")
	        splt[-1] = splt[-1].translate(None, "()")
#        print splt
		indices = [i for i, s in enumerate(lan_list) if splt[0] in s]
		j = indices[0]
		lnnum[j] = locale.atoi(splt[-1])
#	    print lnnum
	    w=namer+","+typer[:20]
	    for i in lnnum:
	        w+=","+str(i)
	    print w
