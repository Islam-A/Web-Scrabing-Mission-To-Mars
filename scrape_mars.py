#########################################################################################
#  Convert Jupyter notebook from Step 1 into Python script with a function called scrape 
#  that will execute all scraping code and return one Python dictionary containing 
#  all of the scraped data.
#########################################################################################

# Import Dependencies 
from flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def scrape():
    ###################################################################################################################
    #  1. Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    #  2. Find the image url for the current Featured Mars Image and assign the url to a variable, featured_image_url.
    #  3. Visit the Mars Weather twitter page and scrape the latest Mars weather tweet from the page into mars_weather.
    #  4. Visit the Mars Facts webpage and use Pandas to scrape the facts table and convert into an html_table_str.
    #  5. Visit planetary.org to obtain high resolution images for each of Mar's hemispheres and make a dictionary.
    ###################################################################################################################
    
    # 1. Scrape HTML from NASA website
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    parsed = bs(response.text, 'html.parser')
    
    ## Find and save titles and description into lists
    news_title_list = []
    news_p_list = []

    for div in parsed.find_all('div', class_ = 'slide'):
        news_title = div.find('div', class_ = 'content_title').text.strip()
        news_p = div.find('div', class_ = 'rollover_description_inner').text.strip()
        news_title_list.append(news_title)
        news_p_list.append(news_p)

    # 2. Scrape HTML from JPL Mars Space Images
    jplmars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(jplmars_url)
    parsed_jplmars = bs(response.text, 'html.parser')

    ## Find and save featured image url
    ### (Splinter's Selenium's Geckodriver was denied on MacOS due to my security settings so I won't be using Splinter)
    for a in parsed_jplmars.find_all('a', class_ = 'button fancybox'):
        featured_image_url = 'https://www.jpl.nasa.gov' + a.get('data-fancybox-href')

    # 3. Scrape HTML from Mars Weather's Twitter Page
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)
    parsed_twitter = bs(response.text, 'html.parser')

    ## Scrape the latest Mars weather tweet from the page
    for p in parsed_twitter.find('p', class_ ="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        mars_weather = p

    # 4. Scrape table from Mars Facts using Pandas
    spacefacts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(spacefacts_url)
    df = tables[0]

    ## Use Pandas to convert the data to a HTML table string
    html_table_str = df.to_html()

    # 5. Scrape HTML from planetary.org
    hemispheres_url = 'http://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    response = requests.get(hemispheres_url)
    parsed_hemisphere = bs(response.text, 'html.parser')

    hemisphere_image_urls = []

    # Get img urls and save into a dictionary then append to a list.
    for img in parsed_hemisphere.find_all('img', class_ = 'img840'):
        
        hemisphere_title = img.get('alt')
        hemisphere_url = img.get('src')
        
        new_dict = {
            'title': hemisphere_title,
            'img_url': hemisphere_url
        }

        hemisphere_image_urls.append(new_dict)

    # Create a dictionary with all the scraped data to return
    dict_of_scraped = {
        "news_title_list": news_title_list,
        "news_p_list": news_p_list,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table_str": html_table_str,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return dict_of_scraped