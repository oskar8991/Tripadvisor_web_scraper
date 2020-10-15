#https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-London_England.html
import re
import selenium
import io
import requests
import bs4
import urllib.request
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from _datetime import datetime
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame

options = webdriver.ChromeOptions()
options.headless = False
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome()
time.sleep(1)
#driver.get("https://tripadvisor.co.uk")
driver.get("https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-London_England.html")
time.sleep(1)

url = driver.current_url
response = requests.get(url)
response = response.text
data = bs4.BeautifulSoup(response, 'lxml')


# NAME, NUMBER OF REVIEWS, AVERAGE REVIEW
# later combine number of reviews and average review into overall score (powerpoint)


################################# COLLECTING ALL PAGE LINKS ############################################
links_full = []
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
page = opener.open(url)
soup = bs4.BeautifulSoup(page,features="lxml")
links_extensions = [tag['href'] for tag in soup.find_all('a', {'class':"_1QKQOve4"})]
for i in range(len(links_extensions)):
    full = "https://www.tripadvisor.co.uk" + links_extensions[i]
    links_full.append(full)

for i in range(30, 1140, 30):
    #### make limit 1000 since last attractions are missing data, etc. (60 for testing) ####
    while i <= 1000:
        i = str(i)
        print("status1: " + i)
        url_curr = 'https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-oa' + i + '-London_England.html'
        r1 = requests.get(url_curr)
        r1 = r1.text
        soup = bs4.BeautifulSoup(r1, "html.parser")

        opener2 = urllib.request.build_opener()
        opener2.addheaders = [('User-agent', 'Mozilla/5.0')]
        page2 = opener2.open(url_curr)
        soup2 = bs4.BeautifulSoup(page2,features="lxml")
        links_extensions = [tag['href'] for tag in soup2.find_all('a', {'class':"_1QKQOve4"})]
        for i in range(len(links_extensions)):
            full = "https://www.tripadvisor.co.uk" + links_extensions[i]
            links_full.append(full)
        break
#print(links_full)


################################# COLLECTING ALL DATA USING PAGE LINKS ############################################
names = []
num_review = []
avg_review = []
count = 0

for link in links_full:
    response = requests.get(link)
    response = response.text
    data = bs4.BeautifulSoup(response, 'lxml')
    num_review_read = data.select('span[class="_3WF_jKL7 _1uXQPaAr"]')
    s1 = str(num_review_read)
    s1 = s1[35:]
    sep = ' '
    stripped = s1.split(sep, 1)[0]
    stripped = stripped.replace(",","")
    if(stripped == ""):
        num_review.append("n/a")
    else:
        num_review.append(stripped)

    name = data.select('[class="ui_header h1"]')
    name = str(name)
    name = name[39:]
    sep2 = '</h1>'
    stripped2 = name.split(sep2, 1)[0]
    if(stripped2 == ""):
        names.append("n/a")
    else:
        names.append(stripped2)

    rating = data.select('span[class="_2Hy7Xxdm"]')
    rating = str(rating)
    rating = rating[25:]
    sep3 = '<'
    stripped3 = rating.split(sep3, 1)[0]
    if(stripped3 == ""):
        #avg_review.append("n/a")
        att2_read = data.select('[class="header heading masthead masthead_h1"]')
        att2 = str(att2_read)
        reversed = att2[::-1]
        reversed = reversed[8:]
        sep6 = ' '
        final = reversed.split(sep6,1)[0]
        final = final[::-1]
        avg_review.append(final)
    else:
        avg_review.append(stripped3)

    count = count + 1
    print("cycle" + str(count))


################################# SAVING DATA ############################################
df = DataFrame({'Name': names, 'Average Rating': avg_review, 'Number of Reviews': num_review})
df.to_excel('data.xlsx', sheet_name='sheet1', index=False)
