#scrape tables
#https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
import requests
import lxml.html as lh
import pandas as pd

year = 2018

while year >= 2010:
    #target url
    url = 'http://www.nfl.com/stats/categorystats?tabSeq=2&offensiveStatisticCategory=GAME_STATS&conference=ALL&role=TM&season='+ str(year) + '&seasonType=REG&d-447263-s=TOTAL_YARDS_GAME_AVG&d-447263-o=2&d-447263-n=1'
    
    #get the html contents
    page = requests.get(url)
    
    #store the contents
    doc = lh.fromstring(page.content)
    
    #parse the data in the tr (rows)
    tr_rows = doc.xpath('//tr')
    
    # check the lenght of the rows
    [len(T) for T in tr_rows[:10]]# picked the firt 10 rows
    
    tr_elements = doc.xpath('//tr')
    
    #create an empty list
    col = []
    i = 0
    
    #pull out each header and an empty list
    for t in tr_elements[0]:
        i+=1
        name = t.text_content()
        print('%d:"%s"'%(i,name))
        col.append((name,[]))
        
    #start adding data at the second row
    for j in range(1, len(tr_elements)):
        #T = tje j'th row
        T = tr_elements[j]
        
        #if the row isnt 21 digits long its not part of the row
        if len(T)!=21:
            break
        
        i = 0
        
        #iterate through all the row elements
        for t in T.iterchildren():
            data = t.text_content()
            #check if the row is empty
            if i > 0:
                #convert any numerical to integer
                try:
                    data = int(data)
                except:
                    pass
            #append the data to an empty list of the i'th column
            col[i][1].append(data)
            #move i to the next column
            i+=1
    
    [len(C) for (title,C) in col]
    
    my_dict = {title:column for (title,column) in col}
    df = pd.DataFrame(my_dict)
    
    year-=1