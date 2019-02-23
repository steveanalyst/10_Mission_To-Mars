# Dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver

    
    #Windows Users
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # return browser = Browser('chrome', **executable_path, headless=False)
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

    
# Create Mars dictionary for importing into Mongo
mars_data = {}

# NASA Mars News
def mars_news_scrape():
    

    # Initialize browser 
    browser = init_browser()

    # Use splinter to visit Mars news website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get news title and paragraph
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    # Store data in a dictionary
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    return print(mars_data)

    

# JPL Mars Space Images - Featured Image
def mars_feature_image_scrape():


    # Initialize browser 
    browser = init_browser()

    # use splinter to visit image website
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    
    # Create HTML object 
    image_html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(image_html, 'html.parser')

    # Click button or link to reach the full resolution image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')

    # Create HTML object 
    fullsize_html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(fullsize_html, 'html.parser')

    # Get full size picture url
    featured_img_url = soup.find('img').get('src')


    # Store data in a dictionary
    mars_data['featured_image_url'] = featured_image_url 
        
    return mars_data

    
        

# Mars Weather 
def mars_weather_scrape():

    

    # Initialize browser 
    browser = init_browser()


    # use splinter to visit weather website beautifulsoup to parse html
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    soup = bs(weather_html, 'lxml')

    # Get text for weather
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    
    # Store data in a dictionary
    mars_data['mars_weather'] = mars_weather
        
    return mars_data

    

# Mars Facts
def mars_facts_scrape():

    facts_url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(facts_url)[0]
    facts_df = facts_df.rename(columns={0:'Mars Planet Profile', 1:''})
    facts_table = facts_df.to_html(classes = 'table table-striped')


    # Store data in a dictionary
    mars_data['mars_facts'] = facts_table

    return mars_data


# Mars Hemispheres
def mars_hemispheres_scrape():

    

    # Initialize browser 
    browser = init_browser()

    # use splinter to visit Mars hemispheres website
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    # Use beautifulsoup to parse HTML
    soup = bs(hemispheres_html, 'lxml')

    # Get all items related with Mars hemispheres
    items = soup.find_all('div', class_='item')

    # Create empty list to save hemisphere urls 
    hemisphere_image_urls = []

    # base url 
    base_url = 'https://astrogeology.usgs.gov'


    # Loop through all items
    for item in items: 
        title = item.find('h3').text

        # save all full image href
        partial_url = item.find('a', class_='itemLink product-item')['href']


        browser.visit(base_url + partial_url)
        partial_html = browser.html
        soup = bs( partial_html, 'html.parser')

        # combine to get full image link
        hemisphere_image_urls = base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : hemisphere_image_urls})


    # Store data in a dictionary
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls


    return mars_data
    