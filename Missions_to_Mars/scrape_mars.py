from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from pprint import pprint
from time import sleep
import aux_func as aux

def scrape():
    browser = Browser("chrome", executable_path="C:/Users/Drew's Surface/AppData/Local/chromedriver", headless=True)
    mars = {
        "title": mars_news1(browser),
        "paragraph": mars_news2(browser),
        "image_URL": jpl_image(browser),
        "weather": mars_weather_tweet(browser),
        "facts": mars_facts(browser),
        "hemisphere": mars_hs(browser),
    }
    return mars

def mars_news1(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    webpage = aux.getParsedWebpage(browser, url)

    # pull the most recent headlines + info from the website
    headlines_grouped = soup.find_all(webpage, 'h3', class_=None)

    # Scrape the first article title and teaser paragraph text; return them
    first_title = aux.getParsedTextList(headlines_grouped)[0]
    return first_title


def mars_news2(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    webpage = aux.getParsedWebpage(browser, url)

    # pull the most recent headlines + info from the website
    text_grouped = soup.find_all(webpage, 'div', class_='article_teaser_body')

    # Scrape the first article title and teaser paragraph text; return them
    first_paragraph = aux.getParsedTextList(text_grouped)[0]
    return first_paragraph

def jpl_image(browser):
    # Scrape the URL and return
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    webpage = aux.getParsedWebpage(browser, url)

    # get and construct url for largest size of featured image available
    featured_url = soup.find(webpage, 'a', class_='button fancybox').get('data-fancybox-href')
    featured_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA11591_hires.jpg"
    return featured_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    webpage = aux.getParsedWebpage(browser, url)

    std_tweet_class = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'


    # pull text of most recent tweet about the weather
    first_tweet = soup.find_all(webpage, 'p', class_= std_tweet_class)[0].get_text()
    return first_tweet
    
def mars_facts(browser):
    url = 'https://space-facts.com/mars/'
    webpage = aux.getParsedWebpage(browser, url)

    # create dict to hold facts
    fact_dict = {}

    # get all rows in the facts table and parse into dict
    facts_all = soup.find(webpage, 
                        'table', 
                        class_='tablepress tablepress-id-p-mars').find_all('tr')

    for fact in facts_all:
        fact_dict[soup.find(fact, 'strong').get_text()] = (soup.find(fact, class_='column-2').get_text())

    # convert to Dataframe and to HTML table
    fact_df = pd.DataFrame.from_dict(fact_dict, orient='index')
    fact_df.rename(columns={0:'Facts about Mars'}, inplace=True)
    fact_html = pd.DataFrame.to_html(fact_df)
    return fact_html
    
def mars_hs(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    webpage = aux.getParsedWebpage(browser, url)

    # get all unique links to the photo pages first
    page_links_list = []
    page_links = soup.find_all(webpage, 'a', class_='itemLink product-item')
    [page_links_list.append(page.get('href')) for page in page_links]
    page_links_list = list(set(page_links_list))

    image_list = []

    # iterate through links and pull URL for full size images
    for link in page_links_list:
        url = f'https://astrogeology.usgs.gov{link}'
        webpage = aux.getParsedWebpage(browser, url)
        
        # get image title
        title = soup.find(webpage, 'h2', class_='title').get_text()
        
        # get full size image link
        downloads_section = soup.find(webpage, 'div', class_='downloads')
        image_link = soup.find(downloads_section, 'a').get('href')
        
        # add title and full-size image url to dict
        image_list.append({'title':title, 'image_url':image_link})
        return image_list