from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys

def crawl(url):
	options = ChromeOptions()
    options.add_arguments("--headless")
    options.add_arguments("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

# crawl python.org
d = crawl("https://python.org")
assert "Python" in d.title
elem = d.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in d.page_source
d.close()
