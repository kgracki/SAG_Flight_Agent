'''
Created on 16 kwi 2018

@author: Kacper Gracki
'''
#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import asyncio


async def check_flights_azair(min_day, max_day):
    # url address with specific flight information
    url = ("http://www.azair.com/azfin.php?tp=0&"
           "searchtype=flexi&srcAirport=Warsaw+%"
           "5BWAW%5D+%28%2BWMI%29&srcTypedText="
           "war&srcFreeTypedText=&srcMC=WAR_ALL&"
           "srcap0=WMI&srcFreeAirport=&dstAirport="
           "Spain+%5BFUE%5D+%28%2BACE%2CLPA%2CTFN%"
           "2CTFS%2CGMZ%2CVDE%2CSPC%2CALC%2CLEI%2COVD"
           "%2CBIO%2CBCN%2CLCG%2CGRO%2CGRX%2CIBZ%2CXRY%"
           "2CMJV%2CMAD%2CAGP%2CMAH%2CREU%2CEAS%2CSCQ%2CVLC"
           "%2CVLL%2CVIT%2CVGO%2CSDR%2CZAZ%2CSVQ%2CPMI%2"
           "CCDT%29&dstTypedText=spai&dstFreeTypedText=&"
           "dstMC=ES&adults=1&children=0&infants=0&minHourStay="
           "0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00"
           "&maxHourOutbound=24%3A00&minHourInbound=0%3A00&"
           "maxHourInbound=24%3A00&dstap0=ACE&dstap2=LPA&dstap3"
           "=TFN&dstap4=TFS&dstap5=GMZ&dstap6=VDE&dstap7=SPC&dstap8"
           "=ALC&dstap9=LEI&dstap10=OVD&dstap11=BIO&dstap12=BCN&dstap13"
           "=LCG&dstap14=GRO&dstap15=GRX&dstap16=IBZ&dstap17=XRY&dstap18"
           "=MJV&dstap19=MAD&dstap20=AGP&dstap21=MAH&dstap22=REU&dstap23"
           "=EAS&dstap24=SCQ&dstap25=VLC&dstap26=VLL&dstap27=VIT&dstap28"
           "=VGO&dstap29=SDR&dstap30=ZAZ&dstap31=SVQ&dstap32=PMI&dstap33"
           "=CDT&dstFreeAirport=&depdate=1.1.2018&arrdate=28.2.2018&"
           "minDaysStay={0}&maxDaysStay={1}&nextday=0&autoprice=true&currency=PLN"
           "&wizzxclub=false&supervolotea=false&schengen=false&transfer=false"
           "&samedep=true&samearr=true&dep0=true&dep1=true&dep2=true&"
           "dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true"
           "&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&maxChng=0"
           "&isOneway=return&resultSubmit=Search".format(min_day, max_day))
    
    url2 = ("http://www.azair.eu/azfin.php?searchtype=flexi&tp="
           "0&isOneway=return&srcAirport=Warsaw+%5BWAW%5D+%28%2"
           "BWMI%29&srcap0=WMI&srcap3=LUZ&srcap4=BZG&srcap5=KTW&"
           "srcFreeAirport=&srcTypedText=war&srcFreeTypedText=&src"
           "MC=WAR_ALL&dstAirport=Malaga+%5BAGP%5D&dstFreeAirport=&"
           "dstTypedText=malag&dstFreeTypedText=&dstMC=&depmonth=20180"
           "4&depdate=2018-04-18&aid=0&arrmonth=201903&arrdate=2019-03-30"
           "&minDaysStay={0}&maxDaysStay={1}&dep0=true&dep1=true&dep2=true&dep3"
           "=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=tru"
           "e&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=tru"
           "e&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&max"
           "HourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&"
           "autoprice=true&adults=1&children=0&infants=0&maxChng=1&currency=PLN&indexSubmit=Search".format(min_day, max_day))
    
    url3 = ("http://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway=return&srcAirport="
            "Warsaw+%5BWAW%5D+%28%2BWMI%29&srcFreeAirport=&srcTypedText=warsaw&srcFreeTypedText"
            "=&srcMC=WAR_ALL&dstAirport=Anywhere+%5BXXX%5D&anywhere=true&dstap0=BRU&dstap2=CRL&dstap4"
            "=LGG&dstap6=OST&dstFreeAirport=&dstTypedText=anywhere&dstFreeTypedText=&dstMC=&depmonth="
            "201806&depdate=2018-06-04&aid=0&arrmonth=201806&arrdate=2018-06-30&minDaysStay={0}&maxDaysStay={1}"
            "&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2"
            "=true&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=true&minHourStay=0%3A45&maxHourStay=23"
            "%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00"
            "&autoprice=true&adults=1&children=0&infants=0&maxChng=1&currency=PLN&indexSubmit=Search".format(min_day, max_day))

    # get request from website
    page = requests.get(url3)
    print(page)

    # parse specific html page
    soup = BeautifulSoup(page.content, 'html.parser')
    # find results by using CSS selector
    # and collect arrays of data
    g_list = soup.findAll("div", {"class": "result"})
    date_g_list = soup.findAll("span", {"class": "date"}) 
    price_g_list = soup.findAll("span", {"class": "tp"})

    best_price = price_g_list[0].text

    from_g_list = soup.findAll("span", {"class": "from"})
    to_g_list = soup.findAll("span", {"class": "to"})

    # print data
    for element in range(len(g_list)):
        print (date_g_list[element * 2].text)           
        print ("\t",from_g_list[(element * 4)].text)
        print ("\t",to_g_list[(element * 4)].text)
        print (date_g_list[(element * 2) + 1].text)
        print ("\t",from_g_list[(element * 4) + 2].text)
        print ("\t",to_g_list[(element * 4) + 2].text)
        print (price_g_list[element].text)
#         if (best_price > price_g_list[element].text):
#             best_price = price_g_list[element].text
#             print ("Best price...", best_price)
        print ("\r\n\r\n")
        
#     print(best_price)
    pattern = best_price.split(" ")
    return int(pattern[0])

async def check_promotion_fru():
    
    url = "https://www.fru.pl/bilety-lotnicze/promocje"
        # get request from website
    page = requests.get(url)
    print(page)

    # parse specific html page
    soup = BeautifulSoup(page.content, 'html.parser')
    g_list = soup.findAll("div", {"class": "direction ellipsis col-xs-7 col-sm-7 col-md-7 col-lg-7 pull-left"})
    direction_g_list = soup.findAll("span", {"class": "content content no-padding no-margin"})
    price_g_list = soup.findAll("div", {"class": "price text-right col-xs-5 col-sm-5 col-md-5 col-lg-5 pull-right"})
    
    price_list = soup.findAll("span", {"class": "value"})
    print(direction_g_list)
    print(price_list)
    
    direction = []
    price = []
    for i in range(12):
        direction.append(direction_g_list[i].text)
        price.append(price_g_list[i].text)
        
        print(direction[i])
        print(price[i])
        
    return price[0]


# check_flights_azair(2, 6)
    