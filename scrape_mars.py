#!/usr/bin/env python
# coding: utf-8

# In[99]:


#Import Packages
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
#get_ipython().system('which chromedriver')
mars_coll ={}


def init_browser():
	executable_path = {'executable_path': 'chromedriver'}
	return Browser ('chrome', **executable_path, headless=False)

def mars_news():

	#Browser
	browser = init_browser()

	#Obtain  Nasa news
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)

	# In[102]:
	html = browser.html
	sp = bs(html, "html.parser")
	# In[103]:
	# Obtain site title, news title and news_paragraph
	
	news_title = sp.find_all('div', class_='bottom_gradient')
	news_paragraph = sp.find_all('div', class_='rollover_description_inner')

	# News info
	ttl = []
	par = []
	# News Title
	for news_ttl in news_title:
		ttl.append(str(news_ttl.text))
	# News Paragraph 
	for news_par in news_paragraph:
		par.append(str(news_par.text))
    
	#zfasdfsadfadsfds
	if len(ttl) > 0: mars_coll["news_title"] = ttl[0]
	else: mars_coll["news_title"] = "I couldn't find the title"

#	if len(par) > 0: mars_coll["news_paragraph"] = news_paragraph[6]
	#item['content'] = item['content'].encode('utf-8', 'strict')
	if len(par) > 0: mars_coll["news_paragraph"] = par[6]
	else: mars_coll["news_paragraph"] = "I couldn't find the News"	

	# Exit Browser
	browser.quit()

	return mars_coll


# In[104]:

def mars_image():

	#Browser
	browser = init_browser()

	#Visit Mars Space Images
	image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url)
	# In[105]:
	# HTML Object 
	html_image = browser.html
	soup = bs(html_image, 'html.parser')
	# In[106]:
	# Obtain background-image 
	background_url  = soup.find('article')['style']
	start = background_url.find("url('")
	end = background_url.find("');")
	url = background_url[start+len("url('"):end]
	#URL
	featured_image_url = 'https://www.jpl.nasa.gov' + url
	mars_coll['featured_image_url'] = str(featured_image_url)
	# Exit Browser
	browser.quit()

	return mars_coll

# In[107]:

def mars_weather():

	#Browser
	browser = init_browser()
	#Access Mars Weather in Twitter
	twitter_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(twitter_url)
	# In[108]:
	#HTML Twitter Object 
	html_weather = browser.html
	sp = bs(html_weather, 'html.parser')
	# In[109]:
	# find first tweet (April, 26 2020) and clean it
	mars_weather=""
	for info in sp.find_all('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'):
	    if "(2020-05-01)" in info.text:
                mars_weather = info.text
	mars_coll['weather_tweet'] = str(mars_weather)
	browser.quit()
	
	return mars_coll

# In[110]:

def mars_facts():
	
	#Facts url 
	facts_url = 'http://space-facts.com/mars/'

	# Read Html and find the mars data
	mars_df = pd.read_html(facts_url)[0]
	# In[111]:
	#Columns
	mars_df.columns = ['Description','Value']
	# Save HTML
	final_data = mars_df.to_html()
	mars_coll['mars_facts'] = final_data
	
	return mars_coll

# In[112]:

def mars_hemispheres():
	#Browser
	browser = init_browser()
	#Hemispheres Page
	hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemispheres_url)


	# In[113]:


	html_hemispheres = browser.html
	sp = bs(html_hemispheres, 'html.parser')


	# In[114]:


	# Obtain mars hemisphere data
	items = sp.find_all('div', class_='item')

	hemispheres = []

	#	 For Loop
	for item in items:         
	    # title
		title = item.find('h3').text
    	# Image link
		link_url = item.find('a', class_='itemLink product-item')['href']
		browser.visit('https://astrogeology.usgs.gov'  + link_url)
            
    	# HTML object to parse the link
		link_url_html = browser.html
		sp = bs(link_url_html, 'html.parser')           
    	# Full image
		final_image_url = 'https://astrogeology.usgs.gov' + sp.find('img', class_='wide-image')['src']
            
    	# Append to list
		hemispheres.append({"title" : title,"final_image_url" : final_image_url})
		mars_coll['hemispheres'] = hemispheres
		browser.quit()
		return mars_coll
