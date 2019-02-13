#https://stackoverflow.com/questions/51785640/scraping-nfl-com-fantasy-football-projections-using-python

import requests
import pandas as pd
from bs4 import BeautifulSoup 

#function to put the scraped data in a list
def get_weekly_players(res):
    res_list = list() 
    week = url.split('statWeek=')[1]
    player_rows = res.find_all('tr')
    for row in player_rows:
        #pick out the important rows
        name = row.find('a', 'playerCard')
        p_yds = row.find('td', 'stat_5')
        p_tds = row.find('td', 'stat_6')
        r_yds = row.find('td', 'stat_14')
        r_tds = row.find('td', 'stat_15')
        
        #append the player data to the list
        if name and p_yds and p_tds and r_yds and r_tds:
            res_list.append((int(week), name.text, str(p_yds.text), str(p_tds.text), str(r_yds.text), str(r_tds.text)))
    return res_list  

#creates a blank list to add the scraped info    
all_res = list()

#loops through all the weeks of the season
for week in range(0, 25):
    url = 'http://fantasy.nfl.com/research/projections?position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=weekProjectedStats&statWeek={}'.format(week)
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    res = get_weekly_players(soup)
    all_res.extend(res)
    
#create the dataframe
player_df = pd.DataFrame(all_res, columns=['week','player', 'pass yards','pass tds', 'rush yards','rush tds'])

#replace the dash with zero and convert to float
player_df = player_df.replace('-',value = '0')
player_df['pass yards'] = player_df['pass yards'].astype(float)
player_df['pass tds'] = player_df['pass tds'].astype(float)
player_df['rush yards'] = player_df['rush yards'].astype(float)
player_df['rush tds'] = player_df['rush tds'].astype(float)
player_df['total yards'] = player_df['rush yards'] + player_df['pass yards']
player_df['total tds'] = player_df['rush tds'] + player_df['pass tds']

#save the data as a csv
export_csv = player_df.to_csv(r'C:\Users\Cullen\Documents\Python Scripts\player_stat_test.csv', index = None, header = True)