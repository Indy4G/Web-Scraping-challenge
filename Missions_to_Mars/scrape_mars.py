from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome", **path, headless=True, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36')

def scrape():
    browser = init_browser()

    ### Create Dictionary For All Mars Data To Be Stored
    mars_data = {}

    ##NASA Mars News
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_news = soup.find('div', class_='image_and_description_container')
    news_title = mars_news.find('div', class_='content_title').text
    news_text = mars_news.find('div', class_='article_teaser_body').text
    
    
    ###Add Mars News To Mars Data Dictionary
    mars_data['news_title']=news_title
    mars_data['news_text']=news_text


    ##JPL Mars Space Images - Featured Image
    mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_images_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_mars_image = soup.find('div', class_='image_and_description_container')
    featured_mars_image = featured_mars_image.find('div', class_='img')
    featured_mars_image = featured_mars_image.find('img')['src']

    featured_image_url = 'https://www.jpl.nasa.gov' + featured_mars_image

    ###Add Featured Mars Image URL To Mars Data Dictionary
    mars_data['featured_image_url']=featured_image_url


    ##Mars Weather
    mars_weatherTwitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weatherTwitter_url)
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('article')
    mars_weather = mars_weather.find_all('span')[4].text

    ###Add Mars Weather To Mars Data Dictionary
    mars_data['mars_weather']=mars_weather


    ##Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df = mars_facts_df.rename(columns = {0:'Mars Facts',1:''})
    mars_facts_df = mars_facts_df.set_index('Mars Facts', drop=True)
    mars_facts_df.to_html('mars_facts.html')
    
    ###Add Mars Weather To Mars Data Dictionary
    mars_data['mars_facts']=mars_facts_df.to_html(justify='left')

    
    ##Mars Hemispheres
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_names = []
    hemisphere_images = []
    for i in range(4):
        browser.visit(mars_hemispheres_url)
        time.sleep(2)
        browser.find_by_css('img[class="thumb"]')[i].click()
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h2', class_="title").text
        name = name.rsplit(' ', 1)[0]
        hemisphere_names.append(name)
        image = soup.find('img', class_='wide-image')['src']
        hemisphere_images.append(f'https://astrogeology.usgs.gov{image}')    

    hemisphere_image_urls = []
    for j in range(4):
        hemisphere_image_urls.append({'title':hemisphere_names[j], 'img_url':hemisphere_images[j]})

    ###Add Mars Hemisphere Images URLs To Mars Data Dictionary
    mars_data['hemisphere_image_urls']=hemisphere_image_urls

    return mars_data