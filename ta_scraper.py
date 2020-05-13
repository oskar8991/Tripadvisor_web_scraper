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

# name, average review, number of reviews
name_read = data.select("._1QKQOve4")
num_review_read = data.select("._82HNRypW")

names = []
for i in range(len(name_read)):
    x = name_read[i].text
    names.append(x)

num_reviews = []
for i in range(len(num_review_read)):
    x = num_review_read[i].text
    x = x[:-8]
    y = x.replace(',', '')
    num_reviews.append(y)

links_full = []
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
page = opener.open(url)
soup = bs4.BeautifulSoup(page,features="lxml")
links_extensions = [tag['href'] for tag in soup.find_all('a', {'class':"_1QKQOve4"})]
for i in range(len(links_extensions)):
    full = "https://www.tripadvisor.co.uk" + links_extensions[i]
    links_full.append(full)


#https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-London_England.html
#https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-oa30-London_England.html

for i in range(30, 1140, 30):
    while i <= 1080:
        i = str(i)
        url_curr = 'https://www.tripadvisor.co.uk/Attractions-g186338-Activities-c47-t2,3,5,6,7,10,12,13,15,17,19,23,24,25,26,34,39,51,76,91,120,163,175-oa' + i + '-London_England.html'
        r1 = requests.get(url_curr)
        r1 = r1.text
        soup = bs4.BeautifulSoup(r1, "html.parser")

        name_read_cont = soup.select("._1QKQOve4")
        num_review_read_cont = soup.select("._82HNRypW")


        for i in range(len(name_read_cont)):
            x = name_read_cont[i].text
            names.append(x)

        for i in range(len(num_review_read_cont)):
            x = num_review_read[i].text
            x = x[:-8]
            y = x.replace(',', '')
            num_reviews.append(y)


        opener2 = urllib.request.build_opener()
        opener2.addheaders = [('User-agent', 'Mozilla/5.0')]
        page2 = opener2.open(url_curr)
        soup2 = bs4.BeautifulSoup(page2,features="lxml")
        links_extensions = [tag['href'] for tag in soup2.find_all('a', {'class':"_1QKQOve4"})]
        for i in range(len(links_extensions)):
            full = "https://www.tripadvisor.co.uk" + links_extensions[i]
            links_full.append(full)

        break


average_ratings = []
for link in links_full:
    response = requests.get(link)
    response = response.text
    data = bs4.BeautifulSoup(response, 'lxml')
    bubblereview = data.select("._2Hy7Xxdm")
    #[<span class="_2Hy7Xxdm">4.5<!-- --> <span class="_1jcHBWVU _1RZqMyqR uq1qMUbD" style="vertical-align:bottom"></span></span>]
    bubblereview_string = str(bubblereview)
    bubblereview_string = bubblereview_string[25:]
    bubblereview_string = bubblereview_string[:-97]
    average_ratings.append(bubblereview_string)
    print(bubblereview_string)


# 1084 names, 1084 links, 1053 number of ratings (last 31 in dataset dont have ranking/reviews -> default to 0)
for i in range(31):
    num_reviews.append(0)

df = DataFrame({'Name': names, 'Average Rating': average_ratings, 'Number of Reviews': num_reviews})
df.to_excel('test.xlsx', sheet_name='sheet1', index=False)
