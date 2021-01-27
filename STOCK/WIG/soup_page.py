from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError,Timeout,RequestException
import requests
import time

class Soup:
    @classmethod
    def get_soup(cls,link,header,cookie,driver,get_driver):
        print("get soap")

        if get_driver is True:
            try:
                driver.get(link)
                driver.implicitly_wait(5)
                page = driver.page_source
                soup = BeautifulSoup(page, features="lxml")
                
                return soup
            except:
                return False

        else:

            try:

                page = requests.get(link,headers=header, cookies=cookie)
                encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
                soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")
                    
                if page.ok :
                    #return r_WIG
                    print("get driver ok")
                    time.sleep(2)
                    return soup

            except ConnectionError as e:
                print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                return False         
            except Timeout as e:
                print("OOPS!! Timeout Error") 
                return False

            except RequestException as e:
                print("OOPS!! General Error") 
                return False
