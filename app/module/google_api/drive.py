import pandas as pd
import requests

def getinitdatasheet():

    url = requests.get('https://docs.google.com/spreadsheets/d/1-nn5MJl2p1HoM1JoGxJgM_9lETW9CXP-zbK05Av1FG0/edit?usp=sharing')
    sheet_id = '1-nn5MJl2p1HoM1JoGxJgM_9lETW9CXP-zbK05Av1FG0'
    sheet_name = 'channel'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)

    return df

