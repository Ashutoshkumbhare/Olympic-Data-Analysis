import pandas as pd
import numpy as np

def preprocess(event,region):

    # merge with region datset
    event = event.merge(region,on='NOC',how='left')

    # dropping duplications
    event.drop_duplicates(inplace=True)

    # one-hot encoding on medels
    event = pd.concat([event,pd.get_dummies(event['Medal'])],axis=1)

    # filter for summer - winter olympics dataset
    summer_event = event[event['Season'] == 'Summer']
    winter_event = event[event['Season'] == 'Winter']

    return summer_event,winter_event

def country_year_list(data):

    Years = data['Year'].unique().tolist()
    Years.sort()
    Years.insert(0, 'Overall')

    Country = np.unique(data['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'Overall')

    return Years,Country