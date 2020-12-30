from random import sample 
import pandas as pd
import requests
import browser_cookie3
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from django.conf import settings  
import os
import json
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
import time
import datetime


class Random ():

    def __init__(self):
        self.headers = {"WIG":{
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Connection": "keep-alive",
        "Host":"www.biznesradar.pl",
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
        "Host":"stooq.pl",
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
    def random_headers(self,genre):
        print("random_header")
        
        header = self.headers[genre]
        header["User-Agent"] = next(iter(sample(self.User_Agent,1)))

        return header
    def get_Driver(self):
        print("driver_get")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.get(settings.PROXY)
        driver.find_element_by_xpath("//select[@class='form-control input-sm']/option[@value='80']").click()
        driver.find_element_by_xpath("//th[@class='hx']/select/option[@value='yes']").click()
        return driver

    def driver_refresh(self,driver):
        print("refresh")
        driver.refresh()
        driver.find_element_by_xpath("//select[@class='form-control input-sm']/option[@value='80']").click()
        driver.find_element_by_xpath("//th[@class='hx']/select/option[@value='yes']").click()
        return driver

    def save_browser(self,proxy,header,genre):
        print("save proxy")
        path = Path(__file__).parent
        filename = os.path.join(path,'Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)
            print(proxy)
            print("befor save",len(my_lis))
        if not proxy in my_lis:
            my_lis[proxy] = [header,0,genre]
            print(my_lis[proxy])
            print("ilość after save",len(my_lis))
            with open(filename, 'w') as outfile:
                outfile.write(json.dumps(my_lis))
                outfile.close()

    def wrong_connect(self,proxy):
        print("wrong conect")
        path = Path(__file__).parent
        filename = os.path.join(path,'Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)

        my_lis[proxy][1] +=1 
        with open(filename, 'w') as outfile:
                outfile.write(json.dumps(my_lis))
                outfile.close()

    def check_proxy_list(self):
        print("chec list")
        path = Path(__file__).parent
        filename = os.path.join(path,'Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)

        [my_lis.pop(i, None) for i in list(my_lis) if my_lis[i][1] >= 3]

        with open(filename, 'w') as outfile:
                outfile.write(json.dumps(my_lis))
                outfile.close()
    def check_wrong_proxy(self,proxy):
        print("chec wrong")
        check = False
        path = Path(__file__).parent
        filename = os.path.join(path,'Wrong_Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)
        today = datetime.date.today()
        print(today.strftime('%m/%d/%Y'))
        if today.strftime('%m/%d/%Y') in my_lis:
            print("if")
            list_todey = my_lis[today.strftime('%m/%d/%Y')]
            if proxy in list_todey:
                check = True

        print(check)
        return check
    def check_all_proxy(self,all_proxy):
        print("check all")
        check = False
        list_proxy = all_proxy
        path = Path(__file__).parent
        filename = os.path.join(path,'Wrong_Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)
        today = datetime.date.today()
        print(today.strftime('%m/%d/%Y'))
        if today.strftime('%m/%d/%Y') in my_lis:
            print("if")
            list_todey = my_lis[today.strftime('%m/%d/%Y')]
            proxy_list = []
            for row in list_proxy.itertuples(index=False):
                    proxy = f'{row[0]}:{int(row[1])}'
                    print(proxy)
                    proxy_list.append(proxy)
            check = all(item in list_todey for item in proxy_list )
            print(check)
            return check


    def add_wrong_proxy(self,proxy):
        print("wrong proxy")
        path = Path(__file__).parent
        filename = os.path.join(path,'Wrong_Proxy.json')
        with open(filename) as file:
            my_lis=json.load(file)
        today = datetime.date.today()
        print(today.strftime('%m/%d/%Y'))
        if today.strftime('%m/%d/%Y') in my_lis:
            print("if")
            list_todey = my_lis[today.strftime('%m/%d/%Y')]
            if not proxy in list_todey:
                print(list_todey)
                list_todey.append(proxy)
                with open(filename, 'w') as outfile:
                    outfile.write(json.dumps(my_lis))
                    outfile.close()
        else:
            print("else")
            my_lis = {}
            my_lis[today.strftime('%m/%d/%Y')] = [proxy]
            with open(filename, 'w') as outfile:
                outfile.write(json.dumps(my_lis))
                outfile.close()


            



    def soup_proxy(self,link,genre,driver):
        print("link:",link)
        cj = browser_cookie3.chrome()
        path = Path(__file__).parent
        filename = os.path.join(path,'Proxy.json')
        

        while True:
            print("while")
            self.check_proxy_list()
            with open(filename) as file:
                my_lis=json.load(file)
            page = 2
            WIG_Proxy = dict((k, v) for k, v in my_lis.items() if v[2] == "WIG")

            print("ilość wig dic",len(WIG_Proxy))
            Index_Proxy = dict((k, v) for k, v in my_lis.items() if v[2] == "Index")
            print(Index_Proxy)
            print("ilość Index dic",len(Index_Proxy))
            

            if len(Index_Proxy) <= 5 and len(WIG_Proxy) <=3:

                page_source = driver.page_source
                df = pd.read_html(page_source , flavor='bs4')[0]
                select = df.loc[df['Https'] == 'yes']
                print(len(df.index))
                print(select)
                if select.empty:
                    print("if select empty")
                    try:
                        page_proxy = driver.find_element_by_xpath(f"//li[@class='paginate_button ']/a[contains(text(), '{page}')]")
                        page_proxy.click()
                        page_source = driver.page_source
                        df = pd.read_html(page_source , flavor='bs4')[0]
                        
                        select = df.loc[df['Https'] == 'yes']
                        print(select)
                    except NoSuchElementException as e:
                        print("except")
                        time.sleep(300)
                        self.driver_refresh(driver)
                        self.soup_proxy(link,genre,driver)


                for row in select.itertuples(index=False):
                    print("for loop")

                    proxy = f'{row[0]}:{int(row[1])}'
                    if self.check_wrong_proxy(proxy):
                        if self.check_all_proxy(select):
                            if genre == "WIG":
                                print("if wig")
                                header_WIG = self.headers['WIG']
                                print("time slep")
                                try:
                                    r_WIG = requests.get(link, headers=header_WIG, cookies=cj)

                                    if r_WIG.ok :
                                        return r_WIG

                                    break
                                except requests.ConnectionError as e:
                                    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                                    print(str(e))           
                                    continue
                                except requests.Timeout as e:
                                    print("OOPS!! Timeout Error") 
                                    print(str(e))
                                    continue
                                except requests.RequestException as e:
                                    print("OOPS!! General Error") 
                                    print(str(e))
                                    continue
                            elif genre == "Index":
                                print("if index")
                                header_Index =  self.headers['Index']
                                print(header_Index)
                        
                                try:
                                    r_Index = requests.get(link, headers=header_Index, cookies=cj)

                                    
                                    if r_Index.ok :
                                        self.save_browser(proxy,header_Index,"Index")
                                        print(r_Index.status_code)
                                        print("proxy sucesses", proxy)
                                        return r_Index
                                        
                                    break
                                except requests.ConnectionError as e:
                                    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                                    print(str(e))            
                                    continue
                                except requests.Timeout as e:
                                    print("OOPS!! Timeout Error")
                                    print(str(e))
                                    continue
                                except requests.RequestException as e:
                                    print("OOPS!! General Error")
                                    print(str(e))
                                    continue

                        else:
                            continue

                    if genre == "WIG":
                        print("if wig")
                        header_WIG = self.random_headers("WIG")
                        print(header_WIG)
                        try:
                            r_WIG = requests.get(link,proxies={"https": f"https://{proxy}"} , headers=header_WIG, cookies=cj,timeout=3)
                            
                            if r_WIG.ok :
                                self.save_browser(proxy,header_WIG,"WIG")
                                print(r_WIG.status_code)
                                print("proxy sucesses", proxy)
                                return r_WIG
                                
                            break
                        except requests.ConnectionError as e:
                            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                            print(str(e))
                            self.add_wrong_proxy(proxy)            
                            continue
                        except requests.Timeout as e:
                            print("OOPS!! Timeout Error")
                            self.add_wrong_proxy(proxy)  
                            print(str(e))
                            continue
                        except requests.RequestException as e:
                            print("OOPS!! General Error")
                            self.add_wrong_proxy(proxy)  
                            print(str(e))
                            continue

                    elif genre == "Index":
                        print("if index")
                        header_Index = self.random_headers("Index")
                        print(header_Index)
                
                        try:
                            r_Index = requests.get(link,proxies={"https": f"https://{proxy}"} , headers=header_Index, cookies=cj,timeout=3)

                            
                            if r_Index.ok :
                                self.save_browser(proxy,header_Index,"Index")
                                print(r_Index.status_code)
                                print("proxy sucesses", proxy)
                                return r_Index
                                
                            break
                        except requests.ConnectionError as e:
                            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                            self.add_wrong_proxy(proxy)  
                            print(str(e))            
                            continue
                        except requests.Timeout as e:
                            print("OOPS!! Timeout Error")
                            self.add_wrong_proxy(proxy)  
                            print(str(e))
                            continue
                        except requests.RequestException as e:
                            print("OOPS!! General Error")
                            self.add_wrong_proxy(proxy)  
                            print(str(e))
                            continue


            else:
                print("else")
                
                if genre == "WIG":
                        sample_proxy = sample(list(WIG_Proxy),1)
                        proxy = sample_proxy[0]
                        header_WIG = my_lis.get(sample_proxy[0])[0]
                        print(proxy)
                        print(header_WIG)
                        try:
                            r_WIG = requests.get(link,proxies={"https": f"https://{proxy}"} , headers=header_WIG, cookies=cj,timeout=3)
                            
                            if r_WIG.ok :
                                print(r_WIG.status_code)
                                print("proxy sucesses", proxy)
                                return r_WIG
                                
                            break
                        except requests.ConnectionError as e:
                            self.wrong_connect(proxy)
                            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                            print(str(e))            
                            continue
                        except requests.Timeout as e:
                            self.wrong_connect(proxy)
                            print("OOPS!! Timeout Error")
                            print(str(e))
                            continue
                        except requests.RequestException as e:
                            self.wrong_connect(proxy)
                            print("OOPS!! General Error")
                            print(str(e))
                            continue

                elif genre == "Index":

                    sample_proxy = sample(list(Index_Proxy),1)
                    proxy = sample_proxy[0]
                    header_Index = my_lis.get(sample_proxy[0])[0]
                    print(header_Index)
                    print(proxy)
            
                    try:
                        r_Index = requests.get(link,proxies={"https": f"https://{proxy}"} , headers=header_Index, cookies=cj,timeout=3)

                        if r_Index.ok :
                            print(r_Index.status_code)
                            print("proxy sucesses", proxy)
                            return r_Index
                            
                        break
                    except requests.ConnectionError as e:
                        self.wrong_connect(proxy)
                        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                        print(str(e))            
                        continue
                    except requests.Timeout as e:
                        self.wrong_connect(proxy)
                        print("OOPS!! Timeout Error")
                        print(str(e))
                        continue
                    except requests.RequestException as e:
                        self.wrong_connect(proxy)
                        print("OOPS!! General Error")
                        print(str(e))
                        continue

                

