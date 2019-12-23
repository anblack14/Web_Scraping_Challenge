from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
from flask import Flask, render_template 
import time 
import numpy as numpy
import json
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    
    # News
    browser = init_browser()

    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    time.sleep(2)

    html = browser.html 
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_="content_title").get_text()
    body = soup.find('div', class_="rollover_description_inner").get_text()

    # Images
    url_image =  "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    response = browser.html
    soup2 = BeautifulSoup(response, 'html.parser')
    images = soup2.find_all('a', class_="fancybox")
    pic_src = []
    for image in images:
        pic = image['data-fancybox-href']
        pic_src.append(pic)

    featured_image_url = "https://www.jpl.nasa.gov" + pic[2]

    # Weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    response = browser.html
    soup3 = BeautifulSoup(response, 'html.parser')
    posts = soup3.find_all('div', class_="js-tweet-text-container")
    weather = []
    for post in posts:
        tweet = post.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        weather.append(tweet)
    
    mars_weather = weather[8]

    # Facts

    url_facts = "https://space-facts.com/mars/"
    df = pd.read_html(url_facts)[0]
    df.columns = ["Facts", "Volume"]
    facts = df.set_index["Facts"]
    facts = facts.replace("\n", "")
    
    fact_table = facts

    # Hemispheres
    hemisphere_image_urls = []

    url_cerberus =  "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(url_cerberus)
    response_cerberus = browser.html
    soup4 = BeautifulSoup(response_cerberus, 'html.parser')
    cerberus_image = soup4.find_all('div', class_='wide-image-wrapper')

    # Cerberus
    for image in cerberus_image:
        cerberus = image.find('li')
        cerberus_full = cerberus.find('a')['href']
    cerberus_title = soup4.find_all('h2', class_='title').get_text()
    cerberus_hemisphere = {'Title': cerberus_title, 'url': cerberus_full}

    hemisphere_image_urls.append(cerberus_hemisphere)

    #Schiaparelli
    url_schiaparelli =  "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(url_schiaparelli)
    response_schiaparelli = browser.html
    soup4 = BeautifulSoup(response_schiaparelli, 'html.parser')
    schiaparelli_image = soup4.find_all('div', class_='wide-image-wrapper')

    for image in schiaparelli_image:
        schiaparelli = image.find('li')
        schiaparelli_full = schiaparelli.find('a')['href']
    schiaparelli_title = soup4.find_all('h2', class_='title').get_text()
    schiaparelli_hemisphere = {'Title': schiaparelli_title, 'url': schiaparelli_full}

    hemisphere_image_urls.append(schiaparelli_hemisphere)

    # Syrtis
    url_syrtis =  "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(url_syrtis)
    response_syrtis = browser.html
    soup4 = BeautifulSoup(response_syrtis, 'html.parser')
    syrtis_image = soup4.find_all('div', class_='wide-image-wrapper')

    for image in syrtis_image:
        syrtis = image.find('li')
        syrtis_full = syrtis.find('a')['href']
    syrtis_title = soup4.find_all('h2', class_='title').get_text()
    syrtis_hemisphere = {'Title': syrtis_title, 'url': syrtis_full}

    hemisphere_image_urls.append(syrtis_hemisphere)

    # Valles
    url_valles =  "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(url_valles)
    response_valles = browser.html
    soup4 = BeautifulSoup(response_valles, 'html.parser')
    valles_image = soup4.find_all('div', class_='wide-image-wrapper')

    for image in valles_image:
        valles = image.find('li')
        valles_full = valles.find('a')['href']
    valles_title = soup4.find_all('h2', class_='title').get_text()
    valles_hemisphere = {'Title': valles_title, 'url': valles_full}

    hemisphere_image_urls.append(valles_hemisphere)

    hemisphere_image = hemisphere_image_urls

    # Dictionary
    mars = {
        "title": title,
        "body": body,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_image": hemisphere_image
    }

    # Close Browswer
    browser.quit()

    # Results 
    return mars
