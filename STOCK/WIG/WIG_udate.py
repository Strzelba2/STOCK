import requests
from bs4 import BeautifulSoup
import sys
from django.conf import settings  
import pandas as pd
from .models import CompanyData , Quotes , Index,IndexData,Wares,WaresData,Currency,CurrencyData,Quotes_last,Currency_Last,Index_Last,Wares_Last
from django.utils import timezone
import pytz
from django.shortcuts import get_object_or_404
import datetime
from django.utils.dateparse import parse_datetime,parse_date
from django.http import HttpResponse
import datetime
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

class UPDATE_SCRAP:

    def __init__(self, **kwargs):
        print("init")
        self.month = {"sty":1,"lut ":2 ,"mar":3,"kwi":4,"maj":5,"cze":6,"lip":7,"sie":8,"wrz":9,"paź":10,"lis" :11,"gru":12}
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
        wait = WebDriverWait(driver, 5)
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

    def dates_bwn_twodates(self,start_date, end_date):
        print("datas_bwn")
        list_data = []
        date_to_check = start_date + datetime.timedelta(days=1) 

        while date_to_check <= end_date:
            days = date_to_check.strftime("%A")
            if days == "Sunday" or days == "Saturday":
                date_to_check += datetime.timedelta(days=1) 
            else:
                list_data.append(date_to_check)
                date_to_check += datetime.timedelta(days=1) 
                
        return list_data

    def day_before(self,last_time):
        print("Day before")

        day_bf = last_time - datetime.timedelta(days=1) 

        if day_bf.strftime("%A") == "Saturday":
            day = day_bf - datetime.timedelta(days=1)   
        elif day_bf.strftime("%A") == "Sunday":
            day = day_bf - datetime.timedelta(days=2)
        else:
            day = day_bf

        return day


    def get_row_archiwum_last(self,name,genre):
        print("52 get_row_archiwum_last")
        cj = browser_cookie3.chrome()

        header_INDEX = self.headers['Index']

        time.sleep(randint(1,4))
        while True:
            print("while")
            soup = Soup.get_soup(f"https://{settings.QUOTE}/q/d/?s={name}",header_INDEX, cj,self.driver,self.get_driver)

            if soup is not False:
                print("soap not fales")
                table = soup.find('table', {'id': 'fth1'})
                
                if table:
                    print("table ok")
                    td = table.find_all('tr')[1].find_all('td')[1].get_text().split(' ')
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

        td_Opening_price = table.find_all('tr')[1].find_all('td')[2].get_text()
        td_Highest_price = table.find_all('tr')[1].find_all('td')[3].get_text()
        td_Lowest_price = table.find_all('tr')[1].find_all('td')[4].get_text()
        td_Closing_price = table.find_all('tr')[1].find_all('td')[5].get_text()
        time_to =f"{td[2]}-{self.month[td[1]]}-{td[0]}"

        last_time =  datetime.datetime.strptime(time_to, "%Y-%m-%d").date()
        if genre == "Currency":
            list_td = [last_time,td_Opening_price,td_Highest_price,td_Lowest_price,td_Closing_price]
        else:
            Volume =  table.find_all('tr')[1].find_all('td')[8].get_text()
            list_td = [last_time,td_Opening_price,td_Highest_price,td_Lowest_price,td_Closing_price,Volume.replace(',', '')]
        print("get_row_archiwum_last",list_td)
        return list_td , soup


    def get_row_archiwum(self,name,genre,list_time , soup):
        print("75","get_row_archiwum")
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']
        data = {}
 
        reversed_dictionary = dict(map(reversed, self.month.items()))

        
        table = soup.find('table', {'id': 'fth1'})
        for date in list_time:
            list_date = f"{date.day} {date.month} {date.year}".split(' ')
            string_date = f"{list_date[0]} {reversed_dictionary[int(list_date[1])]} {list_date[2]}"
            print("214",string_date)
            row_find = table.find('td',text=string_date)
            if row_find:
                row = row_find.parent
            else:
                continue
            td = row.find_all('td')
            Opening_price = td[2].get_text()
            Highest_price = td[3].get_text()
            Lowest_price  = td[4].get_text()
            Closing_price = td[5].get_text()

            if genre != "Currency":
                Volume = td[8].get_text()
                data[date] = [Opening_price,Highest_price,Lowest_price ,Closing_price,Volume.replace(',', '')]
            else:

                data[date] = [Opening_price,Highest_price,Lowest_price ,Closing_price]

        return data

    def get_row_current(self,name):
        print("106 get_row_current")
        cj = browser_cookie3.chrome()
        header_INDEX = self.headers['Index']

        time.sleep(randint(1,4))

        while True:
            soup = Soup.get_soup(f"https://{settings.QUOTE}/q/?s={name}",header_INDEX, cj,self.driver,self.get_driver)
            if soup is not False:
                table = soup.find('table', {'id': 't1'})
                if table:
                    td = table.find_all('td',{'id':'f13'})
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

        Closing_price = td[0].span.get_text()
        time_current = ' '.join([item.get_text() for item in td[1].find_all('span')])
        naive = parse_datetime(time_current)

        if [item for item in td[4]][0] == "Max/min":
            Highest_price = [item.get_text() for item in td[4].find_all('span')][0]
            Lowest_price = [item.get_text() for item in td[4].find_all('span')][1]
            Opening_price = td[7].span.get_text()
        else:
            Highest_price = [item.get_text() for item in td[3].find_all('span')][0]
            Lowest_price = [item.get_text() for item in td[3].find_all('span')][1]
            Opening_price = td[6].span.get_text()


        list_td = [naive,Opening_price,Highest_price,Lowest_price,Closing_price]


        return list_td

    def get_WIG_Soup(self):
        print("get_wig_Soup")
        cj = browser_cookie3.chrome()
        header_WIG = self.headers['WIG']
        while True:
            print("While")
            soup = Soup.get_soup(f"https://{settings.FINANCIAL}/gielda/akcje_gpw",header_WIG, cj,self.driver,self.get_driver)
            if soup is not False:
                    return soup
            else:
                self.reset_wifi()
                if self.get_driver is True:
                    self.get_driver = False
                else:
                    self.get_driver = True

    def check_exist(self,objects,soup):
        print("check_exist")
        for name in objects:
            table = soup.find('table', {'class': 'qTableFull'})
            row= table.find_all('tr')
            print(name.Symbol)
            try:
                x = table.find('a',class_=lambda c: f's_tt s_tt_sname_{name.Symbol}' in c).parent.parent
            except:
                print(f"firma nie istnieje : {name.Symbol}") 
                name.delete()

    def update_WIG(self,name,soup):
        print("wig_update")

        table = soup.find('table', {'class': 'qTableFull'})
        row= table.find_all('tr')

        x = table.find('a',class_=lambda c: f's_tt s_tt_sname_{name.Symbol}' in c).parent.parent
        time= x.find('time')
        td_Opening_price = x.find('span',{'class':'q_ch_open'}).get_text()
        td_Highest_price = x.find('span',{'class':'q_ch_max'}).get_text()
        td_Lowest_price = x.find('span',{'class':'q_ch_min'}).get_text()
        td_Closing_price = x.find('span',{'class':'q_ch_act'}).get_text()
        td_Volume = x.find('span',{'class':'q_ch_vol'}).get_text()

        naive = parse_datetime(time['datetime'].replace('T',' ').split('+')[0])
        aware = pytz.timezone(settings.TIME_ZONE).localize(naive, is_dst=None)

        Company = Quotes_last.objects.filter(Name = name)

        if Company.exists():

            obj = get_object_or_404(Company)
            obj.Day_trading = aware
            obj.Opening_price = td_Opening_price
            obj.Highest_price = td_Highest_price
            obj.Lowest_price = td_Lowest_price
            obj.Closing_price = td_Closing_price
            obj.Volume = td_Volume.replace(' ','')
            obj.save()
   
        else: 
            quotes = Quotes_last.objects.create(Name=name,Day_trading = naive,Opening_price = td_Opening_price,Highest_price = td_Highest_price,
                Lowest_price = td_Lowest_price,Closing_price = td_Closing_price,Volume =td_Volume.replace(' ',''))
    @classmethod
    def update_Rsi(cls):
        print("upds")
        period = 14
        today = datetime.date.today()
        self=cls
        Company = CompanyData.objects.all()
        for name in Company:
            print(name)
            count_query = Quotes.objects.filter(Name=name).count()
            if count_query < 15:
                continue

            Quotes_data = Quotes.objects.filter(Name=name,RSI__isnull=True).order_by('Day_trading')
            if Quotes_data :
                print("if Quotes_data")
                for data in Quotes_data:
                    print(data.Day_trading)

                    day_bef  = self.day_before( self,data.Day_trading)
                    range_min = day_bef - datetime.timedelta(days=14)
                    data_day_bef = Quotes.objects.filter(Name=name,Day_trading= day_bef).last()
                    if not data_day_bef:
                        print("brakdanych")
                        data_day_bef = Quotes.objects.filter(Name=name,Day_trading__range=(range_min,day_bef)).order_by('Day_trading').last()

                    if not data_day_bef.av_gain and not data_day_bef.av_loss:
                        print("data to update")
                        break
                    
                    if data.Closing_price > data_day_bef.Closing_price:
                        av_gain = (data_day_bef.av_gain*(period-1)+(data.Closing_price - data_day_bef.Closing_price))/period
                        av_loss = (data_day_bef.av_loss*(period-1))/period

                        if av_gain == 0:
                            av_gain = 0.0001
                        if av_loss == 0:
                            av_loss = 0.0001

                    else:
                        print("else")
                        av_gain = (data_day_bef.av_gain*(period-1))/period
                        av_loss = (data_day_bef.av_loss*(period-1)+(data_day_bef.Closing_price-data.Closing_price))/period

                        if av_gain == 0:
                                av_gain = 0.0001
                        if av_loss == 0:
                            av_loss = 0.0001

                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))
                    data.av_gain = av_gain
                    data.av_loss = av_loss
                    data.RSI = RSI
                    data.save()
                    if data.Day_trading == today:
                        print("is today")
                        last_data = Quotes_last.objects.filter(Name = name , Day_trading = data.Day_trading)
                        if last_data:
                            print("data exist")
                            obj = get_object_or_404(last_data)
                            obj.RSI = RSI
                            obj.save()
                    print(RSI)

            else:
                print("is None")
                last_archiwum = Quotes.objects.filter(Name=name).order_by('Day_trading').last()
                last_Quates = Quotes_last.objects.filter(Name = name,Day_trading__contains=today).first()

                if last_Quates:
                    print("last_archiwum",last_archiwum.RSI)

                    if last_Quates.Closing_price > last_archiwum.Closing_price:
                                av_gain = (last_archiwum.av_gain*(period-1)+(last_Quates.Closing_price - last_archiwum.Closing_price))/period
                                av_loss = (last_archiwum.av_loss*(period-1))/period

                                if av_gain == 0:
                                    av_gain = 0.0001
                                if av_loss == 0:
                                    av_loss = 0.0001

                    else:

                        av_gain = (last_archiwum.av_gain*(period-1))/period
                        av_loss = (last_archiwum.av_loss*(period-1)+(last_archiwum.Closing_price-last_Quates.Closing_price))/period

                        if av_gain == 0:
                                av_gain = 0.0001
                        if av_loss == 0:
                            av_loss = 0.0001


                    RSI = 100 - (100 / (1 + (av_gain / av_loss)))
                    last_Quates.RSI = RSI
                    last_Quates.save()
                    print(RSI)




                

    @classmethod
    def update_Currency(cls):
        print("WALUTY")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = CurrencyData.objects.all()
        return self.update(objects,"Currency")

    @classmethod
    def update_Index(cls):
        print("INDEX")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = IndexData.objects.all()

        return self.update(objects,"Index")

    @classmethod
    def update_Wares(cls):
        print("WARES")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = WaresData.objects.all()
        return self.update(objects,"Wares")

    @classmethod
    def update_Company(cls):
        print("WIG")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = CompanyData.objects.all()
        #objects = CompanyData.objects.filter(Name = "06MAGNA")
        return self.update(objects,"Company")
    @classmethod
    def fast_update_Company(cls):
        self = cls()
        objects = CompanyData.objects.all()
        soup_WIG = self.get_WIG_Soup()
        self.check_exist(objects,soup_WIG)
        for name in objects:
            print(name)
            self.update_WIG(name,soup_WIG)

            quates_last = Quotes_last.objects.get(Name = name)
            day_befor  = self.day_before( quates_last.Day_trading)
            range_min = day_befor - datetime.timedelta(days=14)
            last_archiwum = Quotes.objects.filter(Name=name,Day_trading__range=(range_min,day_befor)).order_by('Day_trading').last()

            if last_archiwum is None:
                last_archiwum = Quotes.objects.filter(Name=name).order_by('Day_trading').last()
            price = round(( quates_last.Closing_price - last_archiwum.Closing_price)/last_archiwum.Closing_price*100,2)
            print(price)
            quates_last.Change_price = price
            quates_last.save()

        self.driver.quit()

        


    @classmethod
    def change_price(cls):
        self = cls
        print("działa")

        Company = CompanyData.objects.all()

        for name in Company:
            print(name)
            quates_last = Quotes_last.objects.get(Name = name)
            day_befor  = self.day_before(quates_last.Day_trading)
            range_min = day_befor - datetime.timedelta(days=14)
            last_archiwum = Quotes.objects.filter(Name=name,Day_trading__range=(range_min,day_befor)).order_by('Day_trading').last()

            if last_archiwum is None:
                last_archiwum = Quotes.objects.filter(Name=name).order_by('Day_trading').last()
            price = round(( quates_last.Closing_price - last_archiwum.Closing_price)/last_archiwum.Closing_price*100,2)
            print(price)
            quates_last.Change_price = price
            quates_last.save()

        Index_change = IndexData.objects.all()
        for name in Index_change:
            print(name)
            quates_last = Index_Last.objects.get(Name=name)
            day_befor  = self.day_before( self,quates_last.Day_trading)
            range_min = day_befor - datetime.timedelta(days=14)
            last_archiwum = Index.objects.filter(Name=name,Day_trading__range=(range_min,day_befor)).order_by('Day_trading').last()
            if last_archiwum is None:
                last_archiwum = Index.objects.filter(Name=name).order_by('Day_trading').last()
            price = round(( quates_last.Closing_price - last_archiwum.Closing_price)/last_archiwum.Closing_price*100,2)
            print(price)
            quates_last.Change_price = price
            quates_last.save()
        Wares_change = WaresData.objects.all()
        for name in Wares_change:
            print(name)
            quates_last = Wares_Last.objects.get(Name=name)
            day_befor  = self.day_before( self,quates_last.Day_trading)
            range_min = day_befor - datetime.timedelta(days=14)
            last_archiwum = Wares.objects.filter(Name=name,Day_trading__range=(range_min,day_befor)).order_by('Day_trading').last()
            if last_archiwum is None:
                last_archiwum = Wares.objects.filter(Name=name).order_by('Day_trading').last()
            price = round(( quates_last.Closing_price - last_archiwum.Closing_price)/last_archiwum.Closing_price*100,2)
            print(price)
            quates_last.Change_price = price
            quates_last.save()


        Currency_change = CurrencyData.objects.all()
        for name in Currency_change:
            print(name)
            quates_last = Currency_Last.objects.get(Name=name)
            day_befor  = self.day_before( self,quates_last.Day_trading)
            range_min = day_befor - datetime.timedelta(days=14)
            last_archiwum = Currency.objects.filter(Name=name,Day_trading__range=(range_min,day_befor)).order_by('Day_trading').last()
            if last_archiwum is None:
                last_archiwum = Currency.objects.filter(Name=name).order_by('Day_trading').last()
            price = round(( quates_last.Closing_price - last_archiwum.Closing_price)/last_archiwum.Closing_price*100,2)
            print(price)
            quates_last.Change_price = price
            quates_last.save()


        
    def update (self,objects,genre):
        print("update")
        if genre =="Company":
            soup_WIG = self.get_WIG_Soup()
            self.check_exist(objects,soup_WIG)

        for name in objects:

            print(name.Symbol.lower())
            if genre == "Currency": 
                last_archiwum = Currency.objects.filter(Name=name).last()
            elif genre =="Index":
                last_archiwum = Index.objects.filter(Name=name).last() 
            elif genre =="Company":
                last_archiwum = Quotes.objects.filter(Name=name).last()
            elif genre =="Wares":
                last_archiwum = Wares.objects.filter(Name=name).last()
            print(last_archiwum)
            td , last_soup = self.get_row_archiwum_last(name.Symbol.lower(),genre)
            if not genre =="Company":
                td_current = self.get_row_current(name.Symbol.lower())

            last_time =  td[0]
            print(last_time)
            list_dates = self.dates_bwn_twodates(last_archiwum.Day_trading,last_time)
            last_time_before = self.day_before(datetime.date.today())

            if last_archiwum == last_time_before:
                print("current")
                if genre == "Currency": 
                    obj_current =  Currency_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj_current =  Index_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj_current =  Wares_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])

            elif last_archiwum.Day_trading == self.day_before(last_time):
                print("one day before current")
                if genre == "Currency": 
                    obj = Currency.objects.create(Name=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4])
                    obj_current =  Currency_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj = Index.objects.create(Name=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    obj_current =  Index_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    obj = Quotes.objects.create(Name=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj = Wares.objects.create(Name=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    obj_current =  Wares_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                
            else:

                data = self.get_row_archiwum(name.Symbol.lower(),genre,list_dates,last_soup)

                for key,value in data.items():
                    print(key,value)

                    if genre == "Currency": 
                        obj = Currency.objects.create(Name=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3])
                    elif genre =="Index":
                        obj = Index.objects.create(Name=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])
                    elif genre =="Company":
                        obj = Quotes.objects.create(Name=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])
                    elif genre =="Wares":
                        obj = Wares.objects.create(Name=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])

                if genre == "Currency": 
                    obj_current =  Currency_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj_current =  Index_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj_current =  Wares_Last.objects.filter(Name=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])

        self.driver.quit()
        

