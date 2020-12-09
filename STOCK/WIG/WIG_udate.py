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
from .Random_proxy import Random


class UPDATE_SCRAP():

    def __init__(self, **kwargs):

        self.month = {"sty":1,"lut ":2 ,"mar":3,"kwi":4,"maj":5,"cze":6,"lip":7,"sie":8,"wrz":9,"paź":10,"lis" :11,"gru":12}

    def dates_bwn_twodates(self,start_date, end_date):
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

        day_bf = last_time - datetime.timedelta(days=1) 

        if day_bf.strftime("%A") == "Saturday":
            day = day_bf - datetime.timedelta(days=1)   
        elif day_bf.strftime("%A") == "Sunday":
            day = day_bf - datetime.timedelta(days=2)
        else:
            day = day_bf

        return day


    def get_row_archiwum_last(self,name,genre,driver):
        print("52 get_row_archiwum_last")
        page = Random().soup_proxy(f"https://{settings.QUOTE}/q/d/?s={name}","Index",driver)
        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

        table = soup.find('table', {'id': 'fth1'})
        td = table.find_all('tr')[1].find_all('td')[1].get_text().split(' ')
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
        print("71",list_td)
        return list_td

    def get_row_archiwum(self,name,genre,list_time,driver):
        print("75","get_row_archiwum")
        data = {}
        page = Random().soup_proxy(f"https://{settings.QUOTE}/q/d/?s={name}","Index",driver)
        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")
        #reversed_dictionary = dict(map(reversed, self.month.items()))
        reversed_dictionary = dict(map(reversed, self.month.items()))

        table = soup.find('table', {'id': 'fth1'})
        for date in list_time:
            list_date = f"{date.day} {date.month} {date.year}".split(' ')
            string_date = f"{list_date[0]} {reversed_dictionary[int(list_date[1])]} {list_date[2]}"

            row = table.find('td',text=string_date).parent
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

        print(data)
        return data

    def get_row_current(self,name,driver):
        print("106 get_row_current")

        page = Random().soup_proxy(f"https://{settings.QUOTE}/q/?s={name}","Index",driver)
        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

        table = soup.find('table', {'id': 't1'})
        
        td = table.find_all('td',{'id':'f13'})
        for row in td:
            print( "to jest TD numer :   ",row)

        Closing_price = td[8].span.get_text()
        print(Closing_price)
        time = ' '.join([item.get_text() for item in td[10].find_all('span')])
        print(time)
        naive = parse_datetime(time)
        Highest_price = [item.get_text() for item in td[14].find_all('span')][0]
        print(Highest_price)
        Lowest_price = [item.get_text() for item in td[14].find_all('span')][1]
        print(Lowest_price)
        Opening_price = td[20].span.get_text()
        print(Opening_price)

        list_td = [naive,Opening_price,Highest_price,Lowest_price,Closing_price]
        print(list_td)
        return list_td

    def get_WIG_Soup(self,driver):
        page = Random().soup_proxy(f"https://{settings.FINANCIAL}/gielda/akcje_gpw","WIG",driver)
        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")
        return soup

    
    def update_WIG(self,name,soup):
        print("wig_update")

        table = soup.find('table', {'class': 'qTableFull'})
        row= table.find_all('tr')

        x = table.find('a',class_=lambda c: f's_tt s_tt_sname_{name.Symbol}' in c).parent.parent
        time= x.find('time')
        print(x)
        td_Opening_price = x.find('span',{'class':'q_ch_open'}).get_text()
        td_Highest_price = x.find('span',{'class':'q_ch_max'}).get_text()
        td_Lowest_price = x.find('span',{'class':'q_ch_min'}).get_text()
        td_Closing_price = x.find('span',{'class':'q_ch_act'}).get_text()
        td_Volume = x.find('span',{'class':'q_ch_vol'}).get_text()

        naive = parse_datetime(time['datetime'].replace('T',' ').split('+')[0])
        aware = pytz.timezone(settings.TIME_ZONE).localize(naive, is_dst=None)

        Company = Quotes_last.objects.filter(Name_company = name)

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
            quotes = Quotes_last.objects.create(Name_company=name,Day_trading = naive,Opening_price = td_Opening_price,Highest_price = td_Highest_price,
                Lowest_price = td_Lowest_price,Closing_price = td_Closing_price,Volume =td_Volume.replace(' ',''))


    @classmethod
    def update_Currency(cls,driver):
        print("WALUTY")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = CurrencyData.objects.all()
        return self.update(objects,"Currency",driver)

    @classmethod
    def update_Index(cls,driver):
        print("INDEX")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = IndexData.objects.all()
        return self.update(objects,"Index",driver)

    @classmethod
    def update_Wares(cls,driver):
        print("WARES")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = WaresData.objects.all()
        return self.update(objects,"Wares",driver)

    @classmethod
    def update_Company(cls,driver):
        print("WIG")

        self = cls()
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        now = timezone.localtime(timezone.now())
        print(now)

        if now.strftime("%A") == "Sunday" or now.strftime("%A") == "Saturday":
            return HttpResponse("weekend")

        objects = CompanyData.objects.all()
        return self.update(objects,"Company",driver)


    def update (self,objects,genre,driver):
        print("update")
        if genre =="Company":
            soup_WIG = self.get_WIG_Soup(driver)
 
        for name in objects:

            print(name.Symbol.lower())
            if genre == "Currency": 
                last_archiwum = Currency.objects.filter(Name_Currency=name).last()
            elif genre =="Index":
                last_archiwum = Index.objects.filter(Name_Index=name).last() 
            elif genre =="Company":
                last_archiwum = Quotes.objects.filter(Name_company=name).last()
            elif genre =="Wares":
                last_archiwum = Wares.objects.filter(Name_ware=name).last()
            print(last_archiwum)
            td = self.get_row_archiwum_last(name.Symbol.lower(),genre,driver)
            if not genre =="Company":
                td_current = self.get_row_current(name.Symbol.lower(),driver)

            last_time =  td[0]
            print(last_time)
            list_dates = self.dates_bwn_twodates(last_archiwum.Day_trading,last_time)
            last_time_before = self.day_before(datetime.date.today())

            if last_archiwum == last_time_before:
                print("current")
                if genre == "Currency": 
                    obj_current =  Currency_Last.objects.filter(Name_Currency=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name_Currency=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj_current =  Index_Last.objects.filter(Name_Index=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name_Index=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj_current =  Wares_Last.objects.filter(Name_ware=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name_ware=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])

            elif last_archiwum.Day_trading == self.day_before(last_time):
                print("one day before current")
                if genre == "Currency": 
                    obj = Currency.objects.create(Name_Currency=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4])
                    obj_current =  Currency_Last.objects.filter(Name_Currency=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name_Currency=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj = Index.objects.create(Name_Index=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    obj_current =  Index_Last.objects.filter(Name_Index=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name_Index=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    obj = Quotes.objects.create(Name_company=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj = Wares.objects.create(Name_ware=name,Day_trading=td[0],Opening_price=td[1],
                    Highest_price=td[2],Lowest_price=td[3],Closing_price=td[4],Volume = td[5])
                    obj_current =  Wares_Last.objects.filter(Name_ware=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name_ware=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                
            else:

                data = self.get_row_archiwum(name.Symbol.lower(),genre,list_dates,driver)

                for key,value in data.items():
                    print(key,value)

                    if genre == "Currency": 
                        obj = Currency.objects.create(Name_Currency=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3])
                    elif genre =="Index":
                        obj = Index.objects.create(Name_Index=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])
                    elif genre =="Company":
                        obj = Quotes.objects.create(Name_company=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])
                    elif genre =="Wares":
                        obj = Wares.objects.create(Name_ware=name,Day_trading=key,Opening_price=value[0],
                        Highest_price=value[1],Lowest_price=value[2],Closing_price=value[3],Volume = value[4])

                if genre == "Currency": 
                    obj_current =  Currency_Last.objects.filter(Name_Currency=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Currency_Last.objects.create(Name_Currency=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Index":
                    obj_current =  Index_Last.objects.filter(Name_Index=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Index_Last.objects.create(Name_Index=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])
                elif genre =="Company":
                    self.update_WIG(name,soup_WIG)
                elif genre =="Wares":
                    obj_current =  Wares_Last.objects.filter(Name_ware=name)
                    if obj_current.exists():
                        obj_c = get_object_or_404(obj_current)
                        obj_c.Day_trading = pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None)
                        obj_c.Opening_price = td_current[1]
                        obj_c.Highest_price = td_current[2]
                        obj_c.Lowest_price = td_current[3]
                        obj_c.Closing_price = td_current[4]
                        obj_c.save()
                    else:
                        obj_c = Wares_Last.objects.create(Name_ware=name,Day_trading=pytz.timezone(settings.TIME_ZONE).localize(td_current[0], is_dst=None),Opening_price=td_current[1],
                                Highest_price=td_current[2],Lowest_price=td_current[3],Closing_price=td_current[4])

        

