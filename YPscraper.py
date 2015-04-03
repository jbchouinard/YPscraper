#YPScraper.py
#This program searches YellowPages.ca and parses the results
#The output is a python storage (.pickle) file containing the name, address, and category
#of the businesses found
#
# me@jeromebchouinard.ca

import urllib.request
import pickle
import re

#Define term and location to search for on YellowPages.ca
search="groceries" #or search="restaurants" in this case
location="Montreal"
#Number of pages of results on YellowPages.ca for the search (must be checked manually)
no_page=60 

#Load existing matrix from stored pickle file, or create empty one
pickle_file='data.pickle'
try:
    with open(pickle_file, 'rb') as f:
        businesses = pickle.load(f)
except IOError:
    businesses=[]

#Download and parse HTML pages to extract name, address and category of businesses
query='/' + search + '/' location
for i in range(1,max_page):
    f=urllib.request.urlopen('http://www.yellowpages.ca/search/si/'+str(i)+query)

    while(True):
        try:
            raw_html=f.readlines()
            break
        except AttributeError:
            print("Attribute error, reloading page")
            f=urllib.request.urlopen('http://www.yellowpages.ca/search/si/'+str(i)+query)
            
    #Use Regular Expressions to find name, address and category in the HTML page
    for line in raw_html:
        dline = line.decode('utf-8')
        title=re.search(r'class="listingTitle">([^<]*)<', dline)
        address=re.search(r'class="address">([^<]*)<', dline)
        category=re.search(r'class="ypgCategoryLink"><a title="([^"]*)"', dline)
        if title!=None and address!=None:
            businesses.append([title.group(1), address.group(1), "none"])
        if category!=None:
            businesses[-1][2]=category.group(1)

#Remove duplicates
businesses.sort()
delete=[]
for i in range(1, len(businesses)):
    if businesses[i][1] == businesses[i-1][1]:
        if businesses[i-1][2] == "none":
            delete.append(i-1)
        else:
            delete.append(i)

delete.reverse()
      
for i in delete:
    businesses.pop(i)

#Store data in pickle file
with open(pickle_file, 'wb') as f:
    pickle.dump(businesses, f)
