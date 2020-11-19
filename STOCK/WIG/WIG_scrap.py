import requests
from bs4 import BeautifulSoup
import sys
from django.conf import settings  
import os
import pandas as pd
from .models import CompanyData , Quotes


class WIG_STOOP:
    def __init__(self, *args, **kwargs):
        self.WIG = {}


    def get_link(self):
        page = requests.get("https://stooq.pl/t/?i=513")

        encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(page.content, from_encoding=encoding, features="lxml")

        table = soup.find('table', {'id': 'fth1'})
        rows = table.findAll('tr')

        for td in rows:
            name = td.find('td',{'id':'f10'})
            if name is not None:
                text = name.get_text() 
            link = td.find('td',{'id':'f13'})
            if link is not None:
                link_value = link.a['href']
                self.WIG[text] = link_value

        return self.WIG


    @classmethod
    def down_company_data(cls,link,name):
        '''
        Company = CompanyDat.objects.filter(Name_company=name)
        if not Company.exists():
            Company = CompanyDat(Name_company=name,Link_to_Search =link)
        '''
        print(link)
        print(name)
        val= link[-3:]
        href=f"q/d/l/?s={val}&i=d"
        page = requests.get(f"https://stooq.pl/{href}")
        url_data = settings.DATA_ROOT 

        with open(f'{url_data}{val}.csv', 'wb') as f:
            f.write(page.content)

        data=pd.read_csv(f'{url_data}{val}.csv') 
        for row in data.itertuples(index=False):
            print(row[0])
            break
        


    








