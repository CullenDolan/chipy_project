
# coding: utf-8

# In[ ]:

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#import the csv file
df = pd.read_csv('nfl_betting.csv')


# In[ ]:

#remove the weather detail column because it is unstructred free text
#remove the schedule date because i have separate columns with year and week of the season as seperate columns
#remove gameid
#remove games that did not have a betting line and have not occured
new_df = df.drop(['weather_detail','schedule_date','game_id'], axis = 1).dropna(subset = ['over_under_line', 
                                                                                          'score_home'])


# In[ ]:

#replace text w/ numbers for the week 
new_df = new_df.replace(['Wildcard', 'WildCard','Division', 'Conference', 'Superbowl','SuperBowl'],[18,18,19,20,21,21])
#find what the column type is (convert everything to float>> new_df.dtypes


# In[ ]:

#convert 'schedule_week' from object to float
new_df['schedule_week'] = new_df.schedule_week.astype(float)


# In[ ]:

#convert the over underline from object to float
new_df.over_under_line = pd.to_numeric(new_df.over_under_line, errors = 'coerce')


# In[ ]:

#change humidity to a float and if there are erros change to NaN
new_df.weather_humidity = pd.to_numeric(new_df.weather_humidity, errors = 'coerce')
#replace NaN with a value 45
#The NaN cells were when games were played inside, so I took an average indoor humidity
new_df.weather_humidity.fillna(45, inplace = True)


# In[ ]:

#split the columns into independent and dependent variables then recombine
#dependent variable is in the middle of independent variables
x1 = new_df.iloc[:,0:11]
x2 = new_df.iloc[:,13:15]
x = pd.merge(x1, x2, left_index = True, right_index = True).values


# In[ ]:

#encode categorical variables to numerical values
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_x = LabelEncoder()
#home team
x[:,2] = labelencoder_x.fit_transform(x[:,2])
#away team
x[:,3] = labelencoder_x.fit_transform(x[:,3])
#stadium
x[:,4] = labelencoder_x.fit_transform(x[:,4])
#team favorite
x[:,5] = labelencoder_x.fit_transform(x[:,5])
#neutral stadium? (True = neutral)
x[:,11] = labelencoder_x.fit_transform(x[:,11])
#playoff game?(True = playoff game)
x[:,12] = labelencoder_x.fit_transform(x[:,12])


# In[ ]:

#create the over under line as the dependent variable
actual_score = new_df['score_home'] + new_df['score_away']


# I have been wresting with what the endependent variable should look like and thanks to my mentor, here is how I plan to get the y value

# In[ ]:


df2 = pd.DataFrame({'game': [1,2,3], 'vegas_line': [28, 36, 40], 'real_score': [32, 30, 39]})
# Create binary dependent variable. 1 if real_score is greater than vegas_line, 0 if otherwise
df2['over_vegas_line'] = df2.apply(lambda row: 1 if row.real_score > row.vegas_line else 0, axis=1)
df2

