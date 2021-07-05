'''This example scrapes `infologistix <https://infologistix.de>`_. Intended usage is crawling company consulting services from the webpage.

Utilizes infologistix/docker-python-selenium:alpine as image to run of.

'''
from typing import Literal
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import pymsteams

class InfologistixCrawler():
    '''Example Crawler for infologistix homepage.
    Crawles services of the webpage and returns them. 

    Parameters
    ----------
    url : str
        the url to scrape
    headless : bool, default: True
        set to true when running in headless environment

    Examples
    --------
    >>> crawler = InfologistixCrawler(url="https://infologistix.de", headless=False)
    >>> print(crawler.run())
    '''
    def __init__(self, url: str, headless: bool=True) -> None:
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1280,720")
        if headless:
            options.add_argument("--headless")
        self.__driver = Chrome(options=options)
        self.__driver.get(url)

    def getServices(self) -> list:
        '''Scrapes the services of the webpage from infologistix GmbH

        Returns
        -------
        list
            unsorted list of dict-like service structures
        '''
        results = list()
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, "Leistungen")))
        services: WebElement = self.__driver.find_element_by_id("Leistungen")
        service: WebElement
        for service in services.find_elements_by_tag_name("section"):
            results.append(self.__extract(service.find_element_by_class_name("elementor-image-box-content")))
        return results

    def __extract(self, service: WebElement) -> dict:
        '''Extracts the services from each section element.
        Contains URI, title and description for each service.

        Parameters
        ----------
        service : WebElement
            a services WebElement to scrape information

        Returns
        -------
        dict
            information on dict-like basis
        '''
        return {
            "URI" : service.find_element_by_tag_name("a").get_attribute("href"),
            "Title": service.find_element_by_tag_name("a").text,
            "Description": service.find_element_by_tag_name("p").text
        }

    def makeFrame(self, services: list) -> pd.DataFrame:
        '''Converts the list into a human readable table format.

        Parameters
        ----------
        services : list
            unsorted list of services

        Returns
        -------
        pd.DataFrame
            table friendly services
        '''
        return pd.DataFrame(services)

    def run(self) -> pd.DataFrame:
        '''Runs the Crawler and performs actions in the right order.

        Returns
        -------
        pd.DataFrame
            table friendly services
        '''
        services = self.getServices()
        self.close()
        return self.makeFrame(services)

    def close(self) -> None:
        '''Closes the driver.
        '''
        self.__driver.close()



def sendMSTeams(webhook : str, message : str, title : str) -> Literal[True]:
    '''Send a message to a Teams channel. 
    Needs a configured webhook for MS Teams.

    Parameters
    ----------
    webhook : str
        webhook URI to connect to
    message : str
        a message. Can be Text, Markdown or HTML
    title : str
        the messages title

    Returns
    -------
    Literal[True]
        message was sent
    '''
    channel = pymsteams.connectorcard(webhook)
    channel.title(title)
    channel.text(message)
    return channel.send()


if __name__ == "__main__":
    services = InfologistixCrawler(url="https://infologistix.de").run()
    print(services)
    # make a html table 
    message = services.to_html()
    title = "Dienstleistungen Infologistix GmbH"
    # comment out if you have a webhook.
    #sendMSTeams("webhook", message=message, title=title)