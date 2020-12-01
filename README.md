# docker-selenium-python
Docker base image to run python based scripts for selenium in one container. Compiled on top of base python image build on alpine. This method uses chromium in headless.


# Usage
Build docker-image from scratch. This may take a while, because numpy and pandas must be compiled from source. This is indeed a point, where improvements can begin.

Basic requirements are bs4, pandas, numpy and selenium. Simply change your requirements to your needs. 

- Create a python script to trigger selenium based events or crawl the web
- Copy your files to the specified locations
- Run ```docker run -it --rm docker-selenium-python:latest python main.py --args```

Intended usage is for crawling scheduled sites on AWS ECS and Azure ACR. Simply build your container as base and add your scripts to it.

## Example
```Python
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
```

# Advanced Usage
Trigger your script direct at the start of the container requires you to edit the Dockerfile like so:
```Dockerfile
...
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY examples/ ./

CMD ["python", "main.py", "args"]
```
Try using other python-alpine base scripts to utilize as base image to suit your needs.

This image was developed for [infologistix GmbH](https://infologistix.de)