
# coding: utf-8

# In[1]:

import pandas as pd
from pymongo import MongoClient, GEO2D
import pymongo
import json
import datetime
from bson.son import SON
import folium 
import math
import numpy as np
from IPython.display import display


# In[2]:

df_20150817 = pd.read_csv('/home/kathrin/Doctorado/bus_rio/Datos_Omnibus/morte_motoqueiro_20150817/20150817.txt', delimiter = ('\t'))


#Create a link to MongoDB using MongoClient(The name of new database will be morte_motoquiro_event)
db = MongoClient().morte_motoquiro_event

# In[7]:

db.dados20150817.create_index([("latlon", GEO2D)])

clean_df_20150817 = df_20150817[df_20150817['line'].notnull() & df_20150817['latitude'].notnull() & df_20150817['longitude'].notnull()]

for row in clean_df_20150817.iterrows():
    #The 'latitude' and 'longitude' names correspond to column names in the original cceats dataframe
    df_20150817_file = [{"timestamp": row[1]['timestamp'],
                         "bus_id":row[1]['bus_id'],
                         "line":row[1]['line'],
                         "latitude": row[1]['latitude'],
                         "longitude": row [1]['longitude'], 
                         "speed" : row[1]['speed'],
                         "latlon": [row[1]['longitude'], row[1]['latitude']]
                        }]
    db.dados20150817.insert_many(df_20150817_file)

