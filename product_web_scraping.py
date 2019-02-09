#scrape product websites
#https://www.youtube.com/watch?v=XQgXKtPSzUI&t=682s

import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#url i am loking for 
my_url = 'http://www.nfl.com/stats/categorystats?tabSeq=2&offensiveStatisticCategory=GAME_STATS&conference=ALL&role=TM&season=2018&seasonType=REG&d-447263-s=TOTAL_YARDS_GAME_AVG&d-447263-o=2&d-447263-n=1'

uClient = urlopen(my_url)

page_html = uClient.read()

uClient.close()

#html parsing
page_soup = soup(page_html, 'html.parser')

#turn data into csv
#<table id="result"
container = page_soup.findAll('table',{'id':'result'})
#len(container)

#th class 
#th class='thd2' are the headers

headers = page_soup.findAll('th', {'class':'thd2'})

container = container[0]
#get the first row
container.tbody.tr.td.a


