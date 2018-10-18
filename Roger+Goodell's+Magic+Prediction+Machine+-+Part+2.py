
# coding: utf-8

# # Roger Goodell's Magic Prediction Machine - Part 2
# Here is the second installment of my Chipy project. In general, I am not as far along as I hoped but I have learned so much in this short time. I have also been able to sustain interest and am making progress every time I work on the project. I have a decent size data set of historical outcomes for NFL games. I was trying to combine historical outcomes with a different data set of teams stats but was struggling.
# 
# Think back to my original objective, I am refocusing on getting the code to work and then can go back and optimize the variable and inputs for the model. 

# In[121]:

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#import the csv file
df = pd.read_csv('nfl_betting.csv')


# # Data Cleaning 
# The csv file had several types of data sources so i wanted to try to get everything to a float. i also wanted to remove any rows that did not have an over under line.

# In[122]:

#remove the weather detail column because it is unstructred free text
#remove the schedule date because i have separate columns with year and week of the season as seperate columns
#remove gameid
#remove games that did not have a betting line and have not occured
new_df = df.drop(['weather_detail','schedule_date','game_id'], axis = 1).dropna(subset = ['over_under_line', 
                                                                                          'score_home'])


# In[123]:

#replace text w/ numbers for the week 
new_df = new_df.replace(['Wildcard', 'WildCard','Division', 'Conference', 'Superbowl','SuperBowl'],[18,18,19,20,21,21])
#find what the column type is (convert everything to float>> new_df.dtypes


# In[124]:

#convert 'schedule_week' from object to float
new_df['schedule_week'] = new_df.schedule_week.astype(float)


# In[125]:

#convert the over underline from object to float
new_df.over_under_line = pd.to_numeric(new_df.over_under_line, errors = 'coerce')


# In[126]:

#change humidity to a float and if there are erros change to NaN
new_df.weather_humidity = pd.to_numeric(new_df.weather_humidity, errors = 'coerce')
#replace NaN with a value 45
#The NaN cells were when games were played inside, so I took an average indoor humidity
new_df.weather_humidity.fillna(45, inplace = True)


# In[127]:

#split the columns into independent and dependent variables then recombine
#dependent variable is in the middle of independent variables
x1 = new_df.iloc[:,0:11]
x2 = new_df.iloc[:,13:15]
x = pd.merge(x1, x2, left_index = True, right_index = True).values


# In[129]:

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


# In[136]:

#create the over under line as the dependent variable
actual_score = new_df['score_home'] + new_df['score_away']


# I have been wresting with what the endependent variable should look like and thanks to my mentor, here is how I plan to get the y value

# In[135]:


df2 = pd.DataFrame({'game': [1,2,3], 'vegas_line': [28, 36, 40], 'real_score': [32, 30, 39]})
# Create binary dependent variable. 1 if real_score is greater than vegas_line, 0 if otherwise
df2['over_vegas_line'] = df2.apply(lambda row: 1 if row.real_score > row.vegas_line else 0, axis=1)
df2

