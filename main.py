# Created By : Asish Kumar Mundhra
# Date : 30/9/20


# import os
# from config import *
# from app import app
from selenium import webdriver 
import time
import re
import pandas as pd
from newspaper import Article
import datetime
import json
# import pymongo
# from pymongo import MongoClient


driverpath = './chromedriver.exe'
driver = webdriver.Chrome(driverpath)


# db = client.test

def maketimeobject(publish):
    # print("hare startinggg")
    # https://stackoverflow.com/questions/11957595/mongodb-pymongo-query-with-datetime
    day = publish.strftime("%d") 
    month = publish.strftime("%m")
    year = publish.strftime("%Y")
    hour = publish.strftime("%H")
    minute = publish.strftime("%M")
    sec = publish.strftime("%S")
    milli = publish.strftime("%f")
    utc = publish.strftime("%z")
    stamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec), int(milli))
    # print(stamp, type(stamp), "stamppppp", utc)
    return stamp

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def getLinks(content):
    allLinks = []
    for div in content:
        alink = div.find_element_by_tag_name('a').get_attribute('href')
        atext = div.find_element_by_tag_name('a').text
        if atext :
            obj = {}
            # print(alink)
            # allLinks.append(alink)
            obj["link"] = alink
            obj["source"] = "Zacks"
            spanArr = div.find_elements_by_css_selector('div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > div > span:nth-child(1)')
            # if spanArr and re.search( "hours", spanArr.get_attribute('innerHTML')):
            if spanArr and spanArr[0].get_attribute('innerHTML'):
                print(spanArr[0].get_attribute('innerHTML'))
                obj["source"] = spanArr[0].get_attribute('innerHTML')

            allLinks.append(obj)

    return allLinks

def scrapFunction(linksArray, companycode):
    article_arr = []
    i=0
    for singleLink in linksArray:
        print("parsing article...")
        article = Article(singleLink["link"])
        article.download()
        article.parse()
        article.nlp()
        articleObject = {}
        articleObject["author"] = article.authors
        articleObject["text"] = article.text
        articleObject["summary"] = article.summary
        articleObject["title"] = article.title
        articleObject["keywords"] = article.keywords
        articleObject["company_code"] = companycode["code"]
        articleObject["company_name"] = companycode["name"]
        articleObject["source"] = singleLink["source"]
        articleObject["story_date"] = article.publish_date.strftime("%x")
        articleObject["story_time"] = article.publish_date.strftime("%X")
        articleObject["current_date"] = datetime.datetime.now().strftime("%x")
        articleObject["timestamp"] = datetime.datetime.utcnow()
        articleObject["storytimestamp"] = maketimeobject(article.publish_date)
        print("pushing to db...", article.publish_date)
        # db.intelli.update({"title": articleObject["title"]}, articleObject, upsert=True);
        # db.apple.insert_one(articleObject)
        del articleObject["timestamp"]
        del articleObject["storytimestamp"]
        # del articleObject["_id"]
        article_arr.append(articleObject)

    print(len(article_arr))
    json_object = json.dumps(article_arr, indent = 4)
    # f = open("article.json", "w")
    # f.write(json_object)
    # f.close()
    with open('article.json') as json_file: 
        data = json.load(json_file) 
        data = data + article_arr
    write_json(data, "article.json")

def scrollFunction(link, companycode):
    driver.get(link)
    # driver.get("https://in.finance.yahoo.com/quote/WFC?p=WFC&.tsrc=fin-srch")
    print(driver.title, link)
    # last_height = driver.execute_script("return document.body.scrollHeight")
    last_height= 0
    count = 0
    height = driver.execute_script("return document.body.scrollHeight")
    articleBlock = []
    while count<1:
        print(count)
        count = count+1
        new_height = height * count
        print(last_height, new_height)
        heightStr = "window.scrollTo({}, {});"
        driver.execute_script(heightStr.format(last_height, new_height))
        articleBlock = driver.find_elements_by_css_selector('li.js-stream-content')
        print("no.of articles", len(articleBlock))
        # if not getArticleDate(articleBlock[len(articleBlock)-1]):
        #     break;
        last_height = new_height
        # Wait to load the page.
        time.sleep(2)
    print(getLinks(articleBlock))
    scrapFunction(getLinks(articleBlock), companycode)


object = pd.read_pickle('./symbols.pickle')
company_code_arr = []
# 300
for i in range(300, 320):
    companyObj = {}
    companyObj["code"] = object.symbol[i]
    companyObj["name"] = object.company[i]
    print(companyObj)
    link = "https://in.finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch".format(object.symbol[i], object.symbol[i])
    scrollFunction(link, companyObj)
    print("breakkkk")



driver.quit() 
