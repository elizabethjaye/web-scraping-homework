#!/usr/bin/env python
# coding: utf-8

# # Step 0: Import Dependencies & Executable Paths

# In[18]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser


# In[19]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#Define Function
def scrape ():
	# # Step 1: Scraping

	# #### NASA Mars News

	# In[14]:


	#Set up url
	url = 'https://mars.nasa.gov/news/'

	#Retrieve page
	response = requests.get(url)

	#Beautiful Soup object, parsing with html.parser
	soup = BeautifulSoup(response.text, 'html.parser')

	#Examine Results
	print(soup.prettify())


	# In[15]:


	#Pull results
	news_title = soup.find('div', class_="content_title").text
	news_p = soup.find('div', class_="rollover_description_inner").text

	#Print variable values
	print(news_title)
	print(news_p)


	# #### JPL Mars Space Images - Featured Image

	# In[20]:


	#Set up url
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

	#Retrieve page
	browser.visit(url)

	#HTML Object
	html = browser.html

	#Beautiful Soup object, parsing with html.parser
	soup = BeautifulSoup(html, 'html.parser')

	#Examine Results
	print(soup.prettify())


	# In[21]:


	#Pull initial results
	totalIMGPull = str(soup.find("a", class_="button fancybox"))

	#Set search to grab image identifier 
	start = '/spaceimages/details.php?id='
	end = '\" data-title'

	#Pull substring
	suffixIMG = totalIMGPull.partition(start)[2].partition(end)[0]

	#Assigning url
	featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/"+suffixIMG+"_hires.jpg"
	featured_image_url


	# #### Mars Weather

	# In[22]:


	#Set up url
	url = 'https://twitter.com/marswxreport?lang=en'

	#Retrieve page
	response = requests.get(url)

	#Beautiful Soup object, parsing with html.parser
	soup = BeautifulSoup(response.text, 'html.parser')

	#Examine Results
	print(soup.prettify())


	# In[23]:


	#Pull initial set of tweets
	twitterPull = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

	#Check for weather data vs other tweets
	for t in twitterPull:
	    current = t.text
	    if current[:7] == "InSight":
	        marsTweet = current
	        break

	#Clean up text
	marsTweet = marsTweet.partition("InSight ")[2].partition("pic.twitter.com")[0]
	mars_weather = marsTweet.replace("\n", " ")
	mars_weather


	# #### Mars Facts

	# In[24]:


	#Set up url
	url = 'https://space-facts.com/mars/'

	#Read html w/ pandas
	tables = pd.read_html(url)

	#Turn into df
	df_mars = tables[0]

	df_mars.set_index(0, inplace=True)
	df_mars.columns = ["Values"]
	del df_mars.index.name
	df_mars


	# In[25]:


	#Turn into html table
	html_table = df_mars.to_html()

	#Clean Table
	html_table = html_table.replace('\n', '')

	html_table


	# #### Mars Hemispheres

	# In[26]:


	#Manual assigning to dictionary
	hemisphere_image_urls = [
	    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
	    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
	    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
	    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
	]

	# #### Assigning to dictionary
	scrape_dict = {}
	scrape_dict["news_title"] = news_title
	scrape_dict["news_p"] = news_p
	scrape_dict["featured_image_url"] = featured_image_url
	scrape_dict["mars_weather"] = mars_weather
	scrape_dict["html_table"] = html_table
	scrape_dict["hemisphere_image_urls"] = hemisphere_image_urls

	
	return scrape_dict
