import hashlib
import time
import random
import string
from urllib.parse import quote
import requests
import pandas as pd
import numpy as np

def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    return m.hexdigest().upper()
 
def get_params(plus_item):
    global params
    t = time.time()
    time_stamp=str(int(t))
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    app_id='2120885599'
    app_key='v6A4fHWnCeiOLDzh'
    params = {'app_id':app_id,
              'text':plus_item,
              'time_stamp':time_stamp,
              'nonce_str':nonce_str,
             }
    sign_before = ''
    for key in sorted(params):
        sign_before += '{}={}&'.format(key,quote(params[key], safe=''))
    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def get_sentiments(comments):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"
    comments = comments.encode('utf-8')
    payload = get_params(comments)
    r = requests.post(url,data=payload)
    return r.json()

if __name__ == '__main__':
    # test
    get_sentiments('啥时候丢的？')
df_h = pd.read_csv('wordcloud\h_finished.csv')
df_z = pd.read_csv('wordcloud\z_finished.csv')

def emotion_res(df):
    len_emo = max(len(df['emotion']),1)
    len_pos = max(len(df[df['emotion']>0]), 1)
    len_neg = max(len(df[df['emotion']<0]), 1)
    return (
        {
        'avg emotion': np.sum(df['emotion'])/len_emo,
        'avg positive emotion': np.sum(df[df['emotion']>0]['emotion'])/len_pos,
        'avg negative emotion': np.sum(df[df['emotion']<0]['emotion'])/len_neg,
        'pos share': len(df[df['emotion']>0])/len_emo,
        'neg share': len(df[df['emotion']<0])/len_emo
        }
        )

emotion_res(df_z)

def get_by_year(year, df):
    t1 = time.mktime(time.strptime(year + '-01-01', '%Y-%m-%d')) * 1000
    t2 = time.mktime(time.strptime(year + '-12-31', '%Y-%m-%d')) * 1000
    return df[df['createTime'] < t2][df['createTime'] > t1]

def get_by_month(year, month, df):

    t1 = time.mktime(time.strptime(str(year) + "-%02i"%month + '-01', '%Y-%m-%d')) * 1000
    if month != 12:
        t2 = time.mktime(time.strptime(str(year) + "-%02i"%(month+1) + '-01', '%Y-%m-%d')) * 1000
    else:
        t2 = time.mktime(time.strptime(str(year+1) + '-01-01', '%Y-%m-%d')) * 1000

    return df[df['createTime'] < t2][df['createTime'] > t1]



timeData = list()
data_h = list()
data_z = list()
for year in [2015, 2016, 2017, 2018, 2019]:
    for month in range(1,13):
        timeData.append('%i/%i' %(year,month))
        data_z.append(emotion_res(get_by_month(year, month, df_z))['avg emotion'])
        data_h.append(emotion_res(get_by_month(year, month, df_h))['avg emotion'])


