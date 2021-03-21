import requests
from bs4 import BeautifulSoup
import sys
from django.conf import settings  
import pandas as pd
from .models import CompanyData , Quotes , Index,IndexData,Wares,WaresData,Currency,CurrencyData,NCData,NC_Quotes
from django.shortcuts import get_object_or_404
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests.exceptions import ConnectionError,Timeout,RequestException
import time
import browser_cookie3
from random import sample ,randint
from .soup_page import Soup

wifi = settings.WIFI_PASSWORD
link = settings.INDEX_HOST

class SCRAP:
    def __init__(self, *args, **kwargs):
        self.WIG = {}
        self.headers = {"WIG":{
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "pl-PL,pl;q=0.9",
                        "Connection": "keep-alive",
                        "Host":settings.WIG_HOST,
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",},      
                        "Index":{
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Host":settings.INDEX_HOST,
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", },    
                        }
        self.User_Agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"]
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.get_driver = False


    def reset_wifi(self):
        print("reset wifi")
        
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        driver.get("http://192.168.0.1/login.asp")
        driver.implicitly_wait(2)

        admin = driver.find_element_by_xpath("//*[@id='getfocus']")
        admin.send_keys("admin")

        password = driver.find_element_by_xpath("//*[@name='loginPassword']")
        password.send_keys(wifi)

        button = driver.find_element_by_xpath("//*[@id='td_buttonlogin']")

        time.sleep(2)
        button.click()
        time.sleep(2)
        page_source = driver.page_source

        wait = WebDriverWait(driver, 2)
        wait.until(EC.frame_to_be_available_and_switch_to_it(("header")))



        driver.implicitly_wait(2)
        time.sleep(5)
        page_source = driver.page_source

        settings =WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,"//*[@id='menu3']"))) 

        settings.click()
        driver.switch_to.default_content()
        wait = WebDriverWait(driver, 2)
        wait.until(EC.frame_to_be_available_and_switch_to_it(("webbody")))
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"bodysetting_content")))
        reset = driver.find_element_by_xpath("//*[@id='setmanRebootkey']")
        reset.click()
        alert = driver.switch_to_alert()
        alert.accept()
        time.sleep(2)

        driver.implicitly_wait(2)
        driver.quit()
        time.sleep(15)
        header_WIG = self.headers["WIG"]
        header_WIG["User-Agent"] = next(iter(sample(self.User_Agent,1)))
        header_Index = self.headers["Index"]
        header_Index["User-Agent"] = next(iter(sample(self.User_Agent,1)))
        cj = browser_cookie3.chrome()

        header_INDEX = self.headers['Index']

        while True:
            try:
                r_WIG = requests.get(f"https://{link}/",headers=header_INDEX, cookies=cj,timeout=5)
                
                if r_WIG.ok :
                    #return r_WIG
                    print(" print seset wifi ok")
                    time.sleep(5)
                break
            except ConnectionError as e:
                print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                print(str(e)) 
                time.sleep(5)          
                continue
            except Timeout as e:
                print("OOPS!! Timeout Error") 
                print(str(e))
                time.sleep(5)
                continue
            except RequestException as e:
                print("OOPS!! General Error") 
                print(str(e))
                time.sleep(5)
                continue


    def get_link_financial(self):
        cj = browser_cookie3.chrome()
        header_WIG = self.headers['WIG']

        while True:
            soup = Soup.get_soup(f"https://{settings.FINANCIAL}/gielda/akcje_gpw",header_WIG, cj,self.driver,self.get_driver)
            if soup is not False:
                table = soup.find('table', {'class': 'qTableFull'})
                if table:
                    rows = table.findAll('tr')
                    break
                else:
                    self.reset_wifi()
                    if self.get_driver is True:
                        self.get_driver = False
                    else:
                        self.get_driver = True

            else:
                self.reset_wifi()
                if self.get_driver is True:
                    self.get_driver = False
                else:
                    self.get_driver = True


        for tr in rows:
            a = tr.find('a')
            if a:
                text = a.text
                text_to = text.split()

                link = a['href']
                link_to =link.split("/")

                Company = CompanyData.objects.filter(Symbol = text_to[0])
                if Company.exists():
                    self.WIG[text_to[0]] = link_to[2]

        return self.WIG

    def get_link_quote(self,link):
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']

        while True:
            soup = Soup.get_soup(f"https://{settings.QUOTE}/t/{link}",header_INDEX, cj,self.driver,self.get_driver)
            if soup is not False:
                table = soup.find('table', {'id': 'fth1'})
                if table:
                    rows = table.findAll('tr')
                    break
                else:
                    self.reset_wifi()
                    if self.get_driver is True:
                        self.get_driver = False
                    else:
                        self.get_driver = True

            else:
                self.reset_wifi()
                if self.get_driver is True:
                    self.get_driver = False
                else:
                    self.get_driver = True

        for tr in rows:
            name = tr.find('td',{'id':'f10'})
            if name is not None:
                text = name.get_text() 
            link = tr.find('td',{'id':'f13'})
            if link is not None:
                link_value = link.a['href']  
                             
                get_link =  link_value.split('=')
                self.WIG[text] = get_link[1]

        return self.WIG

    def merge_dicts(self,a,*args):
        z = a.copy()
        for x in args:
            z.update(x)
        print(z)
        return z

   
    def down_index(self):
        WIG = self.get_link_quote('?i=510')
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']
        for name ,link in WIG.items():
            print(name)
            Index_obj = IndexData.objects.filter(Name=name)
            if not Index_obj.exists():

                Index_obj = IndexData(Name=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                while True:
                    page = requests.get(f"https://{settings.QUOTE}/{href}",headers=header_INDEX, cookies=cj)
                    if page.content:
                        url_data = settings.DATA_ROOT 
                        with open(f'{url_data}{link}.csv', 'wb') as f:
                            f.write(page.content)

                        break
                    else:
                        self.reset_wifi()

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)

                    quotes = Index.objects.create(Name=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])
                    try:
                        numer_volume = int(row[5])
                        if type(numer_volume) is int:
                            quotes.Volume = numer_volume
                            quotes.save()
                    except:
                        continue

            else:
                continue
            

        self.driver.quit()  

    def down_wares(self):
        print("downwares")
        WIG = self.get_link_quote('?i=512')
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']

        print(WIG)
        for name ,link in WIG.items():
            print(name)
            Wares_obj = WaresData.objects.filter(Name=name)
            if not Wares_obj.exists():
                Index_obj = WaresData(Name=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                while True:
                    page = requests.get(f"https://{settings.QUOTE}/{href}",headers=header_INDEX, cookies=cj)

                    if page.content:
                        url_data = settings.DATA_ROOT 
                        with open(f'{url_data}{link}.csv', 'wb') as f:
                            f.write(page.content)
                        break
                    else:
                        self.reset_wifi()

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):

                    quotes = Wares.objects.create(Name=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])
                    print(row[5])
                    
                    try:
                        numer_volume = int(row[5])
                        if type(numer_volume) is int:
                            print("volume int")
                            quotes.Volume = numer_volume
                            quotes.save()
                    
                    except:
                        continue
 
            else:
                continue

        self.driver.quit()

    def down_currency(self):
        WIG = self.get_link_quote('?i=60')
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']
        print(WIG)
        for name ,link in WIG.items():
            Currency_obj = CurrencyData.objects.filter(Name=name)
            if not Currency_obj.exists():
                Index_obj = CurrencyData(Name=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                while True:
                    page = requests.get(f"https://{settings.QUOTE}/{href}",headers=header_INDEX, cookies=cj)
                    if page.content:
                        url_data = settings.DATA_ROOT 
                        with open(f'{url_data}{link}.csv', 'wb') as f:
                            f.write(page.content)
                        break
                    else:
                        self.reset_wifi()

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)


                    quotes = Currency.objects.create(Name=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])

            else:
                continue
            
        self.driver.quit()

    def down_company_quote(self):
        print("down company")

        WIG_0=self.get_link_quote('?i=513')
        WIG_1=self.get_link_quote('?i=513&v=0&l=2')
        WIG_2=self.get_link_quote('?i=513&v=0&l=3')
        WIG_3=self.get_link_quote('?i=513&v=0&l=4')
        WIG_4=self.get_link_quote('?i=513&v=0&l=5')
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']

        WIG = self.merge_dicts(WIG_0,WIG_1,WIG_2,WIG_3,WIG_4)

        for name ,link in WIG.items():

            Company = CompanyData.objects.filter(Name=name)
            if not Company.exists():
                Company = CompanyData(Name=name, Symbol =link.upper())
                Company.save()
        

                href=f"q/d/l/?s={link}&i=d"
                while True:
                    page = requests.get(f"https://{settings.QUOTE}/{href}",headers=header_INDEX, cookies=cj)
                    if page.content:
                        url_data = settings.DATA_ROOT 

                        with open(f'{url_data}{link}.csv', 'wb') as f:
                            f.write(page.content)
                        break
                    else:
                        self.reset_wifi()


                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)

                    quotes = Quotes.objects.create(Name=Company,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])

                    try:
                        numer_volume = int(row[5])
                        if type(numer_volume) is int:
                            print("volumen",numer_volume)
                            quotes.Volume = numer_volume
                            quotes.save()
                    except:
                        continue

            else:
                continue
        
        self.driver.quit()

    def down_NC_quote(self):
        print("down company")

        WIG_0=self.get_link_quote('?i=514')
        WIG_1=self.get_link_quote('?i=514&v=0&l=2')
        WIG_2=self.get_link_quote('?i=514&v=0&l=3')
        WIG_3=self.get_link_quote('?i=514&v=0&l=4')

        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']

        WIG = self.merge_dicts(WIG_0,WIG_1,WIG_2,WIG_3)

        for name ,link in WIG.items():

            Company = NCData.objects.filter(Name=name)
            if not Company.exists():
                Company = NCData(Name=name, Symbol =link.upper())
                Company.save()
        

                href=f"q/d/l/?s={link}&i=d"
                while True:
                    page = requests.get(f"https://{settings.QUOTE}/{href}",headers=header_INDEX, cookies=cj)
                    if page.content:
                        url_data = settings.DATA_ROOT 
                        print(link)
                        try:
                            with open(f'{url_data}{link}.csv', 'wb') as f:
                                f.write(page.content)
                        except:
                            with open(f'{url_data}{link}_d.csv', 'wb') as f:
                                f.write(page.content)
                        break
                    else:
                        self.reset_wifi()

                try:
                    data=pd.read_csv(f'{url_data}{link}.csv') 
                except:
                    data=pd.read_csv(f'{url_data}{link}_d.csv') 
                for row in data.itertuples(index=False):
                    print(row)

                    quotes = NC_Quotes.objects.create(Name=Company,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])

                    try:
                        numer_volume = int(row[5])
                        if type(numer_volume) is int:
                            print("volumen",numer_volume)
                            quotes.Volume = numer_volume
                            quotes.save()
                    except:
                        continue

            else:
                continue
        
        self.driver.quit()
    @classmethod
    def down_RSI(cls,) :

        period = 14
        '''
        Company = CompanyData.objects.all()
        for name in Company:
            print(name)
            av_up = []
            av_down = []
            av_gain = 0
            av_loss = 0
            Quotes_data = Quotes.objects.filter(Name=name).order_by('Day_trading')
            for i, item in enumerate(Quotes_data):

                if i == 0 :
                    av_up.append(0)
                    av_down.append(0)
                    obj = get_object_or_404(Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()
                elif i < period:
                    if item.Closing_price > Quotes_data[i-1].Closing_price:

                        av_up.append(item.Closing_price-Quotes_data[i-1].Closing_price)
                    else:
                        av_down.append(Quotes_data[i-1].Closing_price-item.Closing_price)

                    obj = get_object_or_404(Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()

                    av_gain = sum(av_up)/period
                    av_loss = sum(av_down)/period

                else:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:
                        av_gain = (av_gain*(period-1)+(item.Closing_price - Quotes_data[i-1].Closing_price))/period
                        av_loss = (av_loss*(period-1))/period
                        if av_gain == 0:
                            av_gain = 0.0001

                        if av_loss == 0:
                            av_loss = 0.0001


                    else:

                        av_gain = (av_gain*(period-1))/period
                        av_loss = (av_loss*(period-1)+(Quotes_data[i-1].Closing_price-item.Closing_price))/period
                        if av_gain == 0:
                            av_gain = 0.0001

                        if av_loss == 0:
                            av_loss = 0.0001


                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))

                    obj = get_object_or_404(Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))
                    obj.av_gain = av_gain
                    obj.av_loss = av_loss
                    obj.RSI = RSI
                    obj.save()
     
        Index_data = IndexData.objects.all()
        for name in Index_data:
            print(name)
            av_up = []
            av_down = []
            av_gain = 0
            av_loss = 0

            Quotes_data = Index.objects.filter(Name=name).order_by('Day_trading')
            for i, item in enumerate(Quotes_data):


                if i == 0 :

                    av_up.append(0)
                    av_down.append(0)
                    obj = get_object_or_404(Index.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()
                elif i < period:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:

                        av_up.append(item.Closing_price-Quotes_data[i-1].Closing_price)
                    else:
                        av_down.append(Quotes_data[i-1].Closing_price-item.Closing_price)

                    obj = get_object_or_404(Index.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()

                    av_gain = sum(av_up)/period
                    av_loss = sum(av_down)/period


                else:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:
                            av_gain = (av_gain*(period-1)+(item.Closing_price - Quotes_data[i-1].Closing_price))/period
                            if av_gain == 0:
                                av_gain = 0.0001

                            av_loss = (av_loss*(period-1))/period
                            if av_loss == 0:
                                av_loss = 0.0001


                    else:
                        av_gain = (av_gain*(period-1))/period
                        av_loss = (av_loss*(period-1)+(Quotes_data[i-1].Closing_price-item.Closing_price))/period

                        if av_gain == 0:
                            av_gain = 0.0001

                        if av_loss == 0:
                            av_loss = 0.0001


                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))


                    obj = get_object_or_404(Index.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = RSI
                    obj.av_gain = av_gain
                    obj.av_loss = av_loss
                    obj.save()
        
        Wares_data = WaresData.objects.all()
        for name in Wares_data:
            print(name)
            av_up = []
            av_down = []
            av_gain = 0
            av_loss = 0
            Quotes_data = Wares.objects.filter(Name=name).order_by('Day_trading')
            for i, item in enumerate(Quotes_data):

                if i == 0 :
                    av_up.append(0)
                    av_down.append(0)
                    obj = get_object_or_404(Wares.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()
                elif i < period:
                    if item.Closing_price > Quotes_data[i-1].Closing_price:

                        av_up.append(item.Closing_price-Quotes_data[i-1].Closing_price)
                    else:
                        av_down.append(Quotes_data[i-1].Closing_price-item.Closing_price)

                    obj = get_object_or_404(Wares.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()

                    av_gain = sum(av_up)/period
                    av_loss = sum(av_down)/period

                else:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:
                            av_gain = (av_gain*(period-1)+(item.Closing_price - Quotes_data[i-1].Closing_price))/period
                            av_loss = (av_loss*(period-1))/period
                            if av_gain == 0:
                                av_gain = 0.0001
                            if av_loss == 0:
                                av_loss = 0.0001

                    else:

                        av_gain = (av_gain*(period-1))/period
                        av_loss = (av_loss*(period-1)+(Quotes_data[i-1].Closing_price-item.Closing_price))/period
                        if av_gain == 0:
                                av_gain = 0.0001
                        if av_loss == 0:
                            av_loss = 0.0001

                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))

                    obj = get_object_or_404(Wares.objects.filter(Name=name , Day_trading = item.Day_trading))
                    obj.av_gain = av_gain
                    obj.av_loss = av_loss
                    obj.RSI = RSI
                    obj.save()
        
        Currency_data = CurrencyData.objects.all()
        for name in Currency_data:
            print(name)
            av_up = []
            av_down = []
            av_gain = 0
            av_loss = 0
            Quotes_data = Currency.objects.filter(Name=name).order_by('Day_trading')
            for i, item in enumerate(Quotes_data):

                if i == 0 :
                    av_up.append(0)
                    av_down.append(0)
                    obj = get_object_or_404(Currency.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()
                elif i < period:
                    if item.Closing_price > Quotes_data[i-1].Closing_price:

                        av_up.append(item.Closing_price-Quotes_data[i-1].Closing_price)
                    else:
                        av_down.append(Quotes_data[i-1].Closing_price-item.Closing_price)

                    obj = get_object_or_404(Currency.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()

                    av_gain = sum(av_up)/period
                    av_loss = sum(av_down)/period

                else:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:
                            av_gain = (av_gain*(period-1)+(item.Closing_price - Quotes_data[i-1].Closing_price))/period
                            av_loss = (av_loss*(period-1))/period

                            if av_gain == 0:
                                av_gain = 0.0001
                            if av_loss == 0:
                                av_loss = 0.0001

                    else:

                        av_gain = (av_gain*(period-1))/period
                        av_loss = (av_loss*(period-1)+(Quotes_data[i-1].Closing_price-item.Closing_price))/period

                        if av_gain == 0:
                                av_gain = 0.0001
                        if av_loss == 0:
                            av_loss = 0.0001

                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))

                    obj = get_object_or_404(Currency.objects.filter(Name=name , Day_trading = item.Day_trading))
                    obj.av_gain = av_gain
                    obj.av_loss = av_loss
                    obj.RSI = RSI
                    obj.save()

        '''
        #Company = NCData.objects.all()
        Company = NCData.objects.filter(Symbol = "PRN")
        for name in Company:
            print(name)
            av_up = []
            av_down = []
            av_gain = 0
            av_loss = 0
            Quotes_data = NC_Quotes.objects.filter(Name=name).order_by('Day_trading')
            for i, item in enumerate(Quotes_data):

                if i == 0 :
                    av_up.append(0)
                    av_down.append(0)
                    obj = get_object_or_404(NC_Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()
                elif i < period:
                    if item.Closing_price > Quotes_data[i-1].Closing_price:

                        av_up.append(item.Closing_price-Quotes_data[i-1].Closing_price)
                    else:
                        av_down.append(Quotes_data[i-1].Closing_price-item.Closing_price)

                    obj = get_object_or_404(NC_Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))

                    obj.RSI = 0
                    obj.save()

                    av_gain = sum(av_up)/period
                    av_loss = sum(av_down)/period

                else:

                    if item.Closing_price > Quotes_data[i-1].Closing_price:
                        av_gain = (av_gain*(period-1)+(item.Closing_price - Quotes_data[i-1].Closing_price))/period
                        av_loss = (av_loss*(period-1))/period
                        if av_gain == 0:
                            av_gain = 0.0001

                        if av_loss == 0:
                            av_loss = 0.0001


                    else:

                        av_gain = (av_gain*(period-1))/period
                        av_loss = (av_loss*(period-1)+(Quotes_data[i-1].Closing_price-item.Closing_price))/period
                        if av_gain == 0:
                            av_gain = 0.0001

                        if av_loss == 0:
                            av_loss = 0.0001


                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))

                    obj = get_object_or_404(NC_Quotes.objects.filter(Name=name , Day_trading = item.Day_trading))
                    obj.av_gain = av_gain
                    obj.av_loss = av_loss
                    obj.RSI = RSI
                    obj.save()

        
    '''
    @classmethod
    def down_company_financial(cls):


        WIG=self.get_link_financial(driver)


        for name ,link in WIG.items():

            page = requests.get(f"https://{settings.FINANCIAL}/{settings.RAPORTY}/{link}")
            encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
            soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

            table = soup.find('table', {'class': 'report-table'})


            year=[c.get_text().split()[0] for c in table.find('tr').find_all('th',{'class':['thq h','thq h newest']})]
            income=[c.find('span',{'class':'pv'}).get_text() for c in table.find('tr',{'data-field':'IncomeRevenues'}).find_all('td',{'class':'h'})]
            incom_net = [c.find('span',{'class':'pv'}).get_text() for c in table.find('tr',{'data-field':'IncomeNetProfit'}).find_all('td',{'class':'h'})]
            EBITDA = [c.find('span',{'class':'pv'}).get_text() for c in table.find('tr',{'data-field':'IncomeShareholderNetProfit'}).find_all('td',{'class':'h'})]
            print(year)
            print(income)
            print(incom_net)
            print(EBITDA)

            
            for tr in rows:
                for col in tr:
                    
                    print( "to jest rząd")
                    print(col)
                    print("koniec")

                    label = tr.find('th',{'class':'thq h'})
                    if label:
                        text = label.text.split()
                        text_to = text[0]
                        print(text_to)
                    data_fields = tr.find('tr',{'data-field':'IncomeRevenues'})
                    print(data_fields)

                break
                
                
'''

            


        


    








