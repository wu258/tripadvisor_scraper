from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import pandas as pd
from time import sleep
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)
url = "https://www.tripadvisor.com/Attractions-g255314-Activities-oa*-place_state.html" 
place="Albury" #You can replace your place here.
state="New_South_Wales"       #You can replace your state here.
targe_number=50    #the number of reviews of each loaction you want to collect.
url = url.replace("place",place)
url = url.replace("state",state)
links=[]
location_names=[]

for i in range(0,1000,30):
    target_url=url.replace("*",str(i))
    driver.get(target_url)
    bsobj = BeautifulSoup(driver.page_source, 'html.parser')
    print("strat")
    place_div=bsobj.find('div',{'class':'fVbwn cdAAV cagLQ eZTON dofsx'})
    if place_div is None:
            break
    for div in bsobj.findAll('div',{'class':'fVbwn cdAAV cagLQ eZTON dofsx'}):
        #print(review)
        links_div=div.findChildren("a" , recursive=False)
        if len(links_div)<2:
            continue
        a = links_div[1]['href']
        #print(a)
        location_names.append(a.split('-')[-2])
        a = 'https://www.tripadvisor.in'+ a
        a = a[:(a.find('Reviews')+7)] + '-or{}' + a[(a.find('Reviews')+7):]
        #print(a)
        links.append(a)

reviews_list = []
reviews_location=[]
count=0

for link in links:
    location=location_names[count]
    count=count+1
    flag=0
    collected_number=0
    for i in range(0,1000,5):
        target_link=link.format(i)
        print(target_link)
        html2 = driver.get(target_link)
        bsobj2 = BeautifulSoup(driver.page_source,'html.parser')    
        reviews_div=bsobj2.find('div',{'class':'dHjBB'})
        if reviews_div is None:
            break
        reviews_div=reviews_div.findChildren("div",{'class':'WlYyy diXIH dDKKM'} , recursive=True)
        #print(reviews_div)
        if(len(reviews_div)==0 or 1==flag):
            flag=0
            break
        print(target_link)
        for r in reviews_div:
            if r.span is None or collected_number>=targe_number:
                flag=1
                break
            reviews_list.append(str(r.span.text.strip()))
            reviews_location.append(location)
            collected_number=collected_number+1
            #sleep(1)
            #print(reviews_list)
        dataframe = pd.DataFrame({'location':reviews_location,'content':reviews_list})
        dataframe.to_csv("tripadvisor_reviews_Albury.csv",index=True)#saving to the csv, you can change the name
