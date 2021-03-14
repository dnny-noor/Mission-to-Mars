# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
browser.visit(url)

html = browser.html
hemisphere_soup = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

links = hemisphere_soup.find_all("div", class_="item")

for link in links:
    hemispheres = {}
    
    title = link.find("h3").text
    
    hemisphere_link = link.find("a", class_="product-item").get("href")
    hemisphere_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{hemisphere_link}'
    
    browser.visit(hemisphere_url)
    
    pic_html = browser.html
    pic_soup = soup(pic_html, 'html.parser')
        
    pic_search = pic_soup.find("div", class_="downloads")
    pic_link = pic_search.find("a", target="_blank").get('href')
    pic_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{pic_link}'

    hemispheres["title"] = title
    hemispheres["img_url"] = pic_url
        
    hemisphere_image_urls.append(hemispheres)
    
    # Navigate Backwards
    #browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
