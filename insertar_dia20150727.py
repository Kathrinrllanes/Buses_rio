
# coding: utf-8

# In[1]:

import pandas as pd
from pymongo import MongoClient, GEO2D
import json


# In[2]:

#Create a link to MongoDB using MongoClient(The name of new database will be aniv_cidade_event)
db = MongoClient().morte_motoquiro_event


# In[3]:

# Create the collection "dados20150208_line_438" with an geolocation index "latlon"
db.dados20150727.create_index([("latlon", GEO2D)])


# In[4]:

#Insert in MongoDb gps data of bus line
df_20150727 = pd.read_csv('/media/noel/7EE1-9608/morte_motoqueiro_20150817/20150727.txt', delimiter = ('\t'))


# In[5]:

df_20150727_file = []
for row in df_20150727.iterrows():
    #The 'latitude' and 'longitude' names correspond to column names in the original cceats dataframe
    df_20150727_file = [{"timestamp": row[1]['timestamp'],
                         "bus_id":row[1]['bus_id'],
                         "line":row[1]['line'],
                         "latitude": row[1]['latitude'],
                         "longitude": row [1]['longitude'],
                         "speed" : row[1]['speed'],
                         "latlon": [ row[1]['longitude'], row[1]['latitude'] ]
                         }]
    db.dados20150727.insert_many(df_20150727_file)


