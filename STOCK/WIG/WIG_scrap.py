import requests
from bs4 import BeautifulSoup
import sys
from django.conf import settings  
import pandas as pd
from .models import CompanyData , Quotes , Index,IndexData,Wares,WaresData,Currency,CurrencyData



class SCRAP:
    def __init__(self, *args, **kwargs):
        self.WIG = {}

    def get_link_financial(self):
        page = requests.get(f"https://{settings.FINANCIAL}/gielda/akcje_gpw")
        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

        table = soup.find('table', {'class': 'qTableFull'})
        rows = table.findAll('tr')

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
        page = requests.get(f"https://{settings.QUOTE}/t/{link}")

        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

        table = soup.find('table', {'id': 'fth1'})
        rows = table.findAll('tr')

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

    def merge_dicts(self,a, b,c,d,e):
        z = a.copy()
        z.update(b)
        z.update(c)
        z.update(d)
        z.update(e)
        return z

    @classmethod
    def down_index(cls):
        WIG = SCRAP().get_link_quote('?i=510')
        for name ,link in WIG.items():
            print(name)
            Index_obj = IndexData.objects.filter(Name_Index=name)
            if not Index_obj.exists():

                Index_obj = IndexData(Name_Index=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                page = requests.get(f"https://{settings.QUOTE}/{href}")
                url_data = settings.DATA_ROOT 
                with open(f'{url_data}{link}.csv', 'wb') as f:
                    f.write(page.content)

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)

                    quotes = Index.objects.create(Name_Index=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])
                    try:
                        if row[5] is int:
                            quotes.Volume = row[5]
                            quotes.save()
                    except:
                        continue

                
            else:
                continue
            break

            
    @classmethod
    def down_wares(cls):
        WIG = SCRAP().get_link_quote('?i=512')
        print(WIG)
        for name ,link in WIG.items():
            Wares_obj = WaresData.objects.filter(Name_ware=name)
            if not Wares_obj.exists():
                Index_obj = WaresData(Name_ware=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                page = requests.get(f"https://{settings.QUOTE}/{href}")
                url_data = settings.DATA_ROOT 
                with open(f'{url_data}{link}.csv', 'wb') as f:
                    f.write(page.content)

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)


                    quotes = Wares.objects.create(Name_ware=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])
                    try:
                        if row[5] is int:
                            quotes.Volume = row[5]
                            quotes.save()

                    except:
                        continue

            else:
                continue
            break

    @classmethod
    def down_currency(cls):
        WIG = SCRAP().get_link_quote('?i=60')
        print(WIG)
        for name ,link in WIG.items():
            Currency_obj = CurrencyData.objects.filter(Name_Currency=name)
            if not Currency_obj.exists():
                Index_obj = CurrencyData(Name_Currency=name, Symbol =link.upper())
                Index_obj.save()
                href=f"q/d/l/?s={link}&i=d&o=1111111"
                page = requests.get(f"https://{settings.QUOTE}/{href}")
                url_data = settings.DATA_ROOT 
                with open(f'{url_data}{link}.csv', 'wb') as f:
                    f.write(page.content)

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)


                    quotes = Currency.objects.create(Name_Currency=Index_obj,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])

            else:
                continue
            break

  
    @classmethod
    def down_company_quote(cls):

        WIG_0=SCRAP().get_link_quote('?i=513')
        WIG_1=SCRAP().get_link_quote('?i=513&v=0&l=2')
        WIG_2=SCRAP().get_link_quote('?i=513&v=0&l=3')
        WIG_3=SCRAP().get_link_quote('?i=513&v=0&l=4')
        WIG_4=SCRAP().get_link_quote('?i=513&v=0&l=5')

        WIG = SCRAP().merge_dicts(WIG_0,WIG_1,WIG_2,WIG_3,WIG_4)

        for name ,link in WIG.items():

            Company = CompanyData.objects.filter(Name_company=name)
            if not Company.exists():
                Company = CompanyData(Name_company=name, Symbol =link.upper())
                Company.save()
        

                href=f"q/d/l/?s={link}&i=d"
                page = requests.get(f"https://{settings.QUOTE}/{href}")
                url_data = settings.DATA_ROOT 

                with open(f'{url_data}{link}.csv', 'wb') as f:
                    f.write(page.content)

                data=pd.read_csv(f'{url_data}{link}.csv') 
                for row in data.itertuples(index=False):
                    print(row)

                    quotes = Quotes.objects.create(Name_company=Company,Day_trading = row[0],Opening_price = row[1],Highest_price = row[2],
                    Lowest_price = row[3],Closing_price = row[4])
                    try:
                        if row[5] is int:
                            quotes.Volume = row[5]
                            quotes.save()
                    except:
                        continue

            else:
                continue
            break

        

    @classmethod
    def down_company_financial(cls):


        WIG=SCRAP().get_link_financial()


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

            '''
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
                


            


        


    








