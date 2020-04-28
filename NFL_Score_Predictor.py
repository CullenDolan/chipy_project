# import libraries
import pandas as pd

# import the csv file
df = pd.read_csv('nfl_data.csv')
# remove the weather detail column because it is unstructred free text
# remove the schedule date because i have separate columns with year and week of the season as seperate columns
# remove gameid
# remove games that did not have a betting line and have not occured
new_df = df.drop(['weather_detail', 'schedule_date', 'game_id'], axis=1).dropna(subset=['over_under_line',
                                                                                        'score_home'])
# replace text w/ numbers for the week
new_df = new_df.replace(['Wildcard', 'WildCard', 'Division', 'Conference', 'Superbowl', 'SuperBowl'],
                        [18, 18, 19, 20, 21, 21])
# find what the column type is (convert everything to float>> new_df.dtypes
# convert 'schedule_week' from object to float
new_df['schedule_week'] = new_df.schedule_week.astype(float)
# convert the over underline from object to float
new_df.over_under_line = pd.to_numeric(new_df.over_under_line, errors='coerce')
# change humidity to a float and if there are erros change to NaN
new_df.weather_humidity = pd.to_numeric(new_df.weather_humidity, errors='coerce')
# replace NaN with a value 45
# The NaN cells were when games were played inside, so I took an average indoor humidity
new_df.weather_humidity.fillna(45, inplace=True)
new_df.head()
# overundre line; weathertemp; weather wind mph need zeros
# split the columns into independent and dependent variables then recombine
# dependent variable is in the middle of independent variables
x1 = new_df.iloc[:, 0:11]
x2 = new_df.iloc[:, 13:15]
x = pd.merge(x1, x2, left_index=True, right_index=True).values
# encode categorical variables to numerical values
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder_x = LabelEncoder()
# home team
x[:, 2] = labelencoder_x.fit_transform(x[:, 2])
# away team
x[:, 3] = labelencoder_x.fit_transform(x[:, 3])
# stadium
x[:, 4] = labelencoder_x.fit_transform(x[:, 4])
# team favorite
x[:, 5] = labelencoder_x.fit_transform(x[:, 5])
# neutral stadium? (True = neutral)
x[:, 11] = labelencoder_x.fit_transform(x[:, 11])
# playoff game?(True = playoff game)
x[:, 12] = labelencoder_x.fit_transform(x[:, 12])
x
# create over under line as independent variable
new_df['actual_score'] = new_df.score_home + new_df.score_away
# use lambda function to create the boolean to state if the score was over or under
new_df['over_line'] = new_df.apply(lambda row: 1 if row.actual_score > row.over_under_line else 0, axis=1)
# Create the dependent variabel
y = new_df.iloc[:, 16].values
