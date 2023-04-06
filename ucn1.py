import re
from undetected_chromedriver import Chrome
import time


driver = Chrome()
try:
    driver.get("https://teluguflix.shop/category/recently-added-movies/")
    
    # Scroll the page down to load dynamic content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Get the final page source
    page_source = driver.page_source
  
    links = re.findall('<a\s+(?!.*category|quality)[^>]*?href="([^"]*(1080p|720p|576p|x264)[^"]*)"', page_source)
    for link in links:
        driver.get(link[0])  # Visit the page
        page_source = driver.page_source
        # Find all href links using regex
        tiny = re.findall('<h4><a href="([^"]*tinyfy[^"]*)"[^>]*>', page_source)
        print(tiny)
except Exception as e:
    print(e)

finally:
    driver.quit()
