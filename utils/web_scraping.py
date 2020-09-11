# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:37:26 2020

@author: misha
"""
from bs4 import BeautifulSoup
from selenium import webdriver


class WebScraper:
    
    @staticmethod
    def get_chrome_driver(**kwargs):
        """Fetch the driver for the Google Chrome browser"""
        path_to_driver = kwargs['path_to_driver']
        driver = webdriver.Chrome(path_to_driver)
        return driver
    
    @staticmethod
    def get_page_content_soup(**kwargs):
        """Extract page content for the URL passed"""
        driver = kwargs['driver']
        url = kwargs['url']
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        return soup
