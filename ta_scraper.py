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
    #TEMP (i<=1100) should be picked (set to 60 for quicker testing)
    #################### make it 1000 since last attractions are missing data, etc. 
    while i <= 1100:
        i = str(i)
        print("status1: " + i)
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
count = 0
for link in links_full:
    response = requests.get(link)
    response = response.text
    data = bs4.BeautifulSoup(response, 'lxml')
    bubblereview = data.select("._2Hy7Xxdm")
    #[<span class="_2Hy7Xxdm">4.5<!-- --> <span class="_1jcHBWVU _1RZqMyqR uq1qMUbD" style="vertical-align:bottom"></span></span>]
    bubblereview_string = str(bubblereview)
    bubblereview_string = bubblereview_string[25:]
    bubblereview_string = bubblereview_string[:-97]
    if bubblereview_string == "":
        #https://www.tripadvisor.co.uk/Attraction_Review-g186338-d17712763-Reviews-Wimbledon_Centre_Court-London_England.html
        for div in data.find_all(class_="attractions-attraction-review-header-attraction-review-header__ratingContainer--1lMqm"):
            #status2: (==) <span class="ui_bubble_rating bubble_45"></span>
            rating = div.find(class_= re.compile('ui_bubble_rating bubble_\d*'))
            rating_string = str(rating)
            rating_string = rating_string[37:]
            rating_string = rating_string[:-9]
            format_string = rating_string[:1] + '.' + rating_string[1:]
            if format_string == "":
                average_ratings.append("0")
            else:
                average_ratings.append(format_string)
            count = count + 1
            print("status2 (if): " + format_string + "[" + str(count) + "]")
            break   #prevents duplicated print
    else:
        average_ratings.append(bubblereview_string)
        count = count + 1
        print("status2 (else): " + bubblereview_string + "[" + str(count) + "]")

#average_ratings_cleaned = [x for x in average_ratings if x]

print(len(names)) #1084
print(len(num_reviews)) #1053
print(len(average_ratings)) #count reached 1052 -> 1053 (LAST 31 DONT HAVE RANKING/REVIEW)

# 1084 names, 1084 links, 1053 number of ratings (last 31 in dataset dont have ranking/reviews -> default to 0)
#next run 1048 for average_ratings len? Make method to fill to 1084 depending on current length of both
'''
for i in range(31):
    num_reviews.append(0)

while(len(average_ratings) < 1084):
    average_ratings.append("0")
'''


######## MAJORITY OF CODE CORRECT BUT PAGE 2+ INCORRECT [GATHER COLLECTION OF 'NEXT' LINKS AND USE CODE FROM THAT] #########################
######## RUN TEST FOR FIRST 3 PAGES INTO DATAFRAME AND SEE IF CORRECT (WILL COVER ALL CASES - IF,ELSE) #####################################
######## REPULLS THE SAME NUMBER_OF_REVIEW DATA FROM PAGE 1 ONTO PAGE 2,3,4,5,.... #########################################################

df = DataFrame({'Name': names, 'Average Rating': average_ratings, 'Number of Reviews': num_reviews, 'Link': links_full})
df.to_excel('test.xlsx', sheet_name='sheet1', index=False)
