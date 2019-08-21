import pandas as pd
import sqlite3
import time
import jieba
from collections import Counter
from emotion_analysis import *


db_file = r'resource\wechat_log\decrypted_database.db'

with sqlite3.connect(db_file) as conn:
    # messages from chatroom 
    df_cr = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='902' and type=1", con=conn)
    # hong's message from chatroom 
    # df_cr[df_cr['content'].str.startswith("pdd003:\n")]
    df_h_1 = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='902' and type=1 and status = 4", con=conn)
    df_h_1['content'] = df_h_1['content'].str.replace(r'pdd003:\n', "")
    # zhuang's message from chatroom 
    # df_cr[-df_cr['content'].str.startswith("pdd003:\n")]
    df_z_1 = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='902' and type=1 and status = 2", con=conn)
    # chatroom name
    df_name = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='902' and type=10000", con=conn)
    # messages from private chat 
    df_pc = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='618' and type=1", con=conn)    
    # hong's message from private chat 
    df_h_2 = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='618' and type=1 and status = 4", con=conn)
    # zhuang's message from private chat 
    df_z_2 = pd.read_sql_query("SELECT content, createTime FROM message WHERE talkerId='618' and type=1 and status = 2", con=conn)




df_z = df_z_1.append(df_z_2)
df_h = df_h_1.append(df_h_2)
df_all = df_cr.append(df_pc)


'''
df_z.to_csv('z.csv')
df_h.to_csv('h.csv')
'''

'''
count_z = 0
for m in df_z['content']:
    count_z += len(m)
print(count_z)

count_h = 0
for m in df_h['content']:
    count_h += len(m)
print(count_h)

len(df_z)
len(df_h)
'''

def get_message_time(df_):
    time_map = [dict() for i in range(8)]
    for t in df_['createTime']:
        h = time.strftime('%H', time.gmtime(t//1000))
        w = int(time.strftime('%w', time.gmtime(t//1000)))
        # notice: time.strftime has a shift of 8, probably because of time zone
        key = (int(h) + 8)%24

        if key not in time_map[w]:
            time_map[w][key] = 0
        time_map[w][key] += 1
    
    ret = list()
    for w_ in range(7):
        ret += [[w_,h_,time_map[w_][h_]] for h_ in range(24)]
    return ret
    

#get_message_time(df_h)
#get_message_time(df_z)

# word cloud
def word_cloud(df, quantity):
    
    wordfilter = list("abcdefghijklmnopqrstquvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    text_ls = list(df['content'])
    res = list()
    for t in text_ls:
        for wf in wordfilter:
            t = t.replace(wf, "")
        if t:
            res.append(t)
    text = ''.join(res)
    print("finished parsing text message")
    seg_list = jieba.cut(text, cut_all=False)
    print("finished text segmentation")
    c = Counter()
    for x in seg_list:
        c[x] += 1

    punc = list(r'.。（）()?？:：！![]"‘’“”+=-*$#@~《》< ，,/\\～…\|¯_\'')
    for p in punc:
        if p in c:
            del c[p]

    keys = list(c.keys())
    for key in keys:
        if len(key) == 1:
            del c[key]
    print("finished disposing puctuation and stopwords")
    return dict(c.most_common(quantity))

#word_cloud(df_z, 200)


def get_content_freq(df, quantity):
    punc = list(r'.。（）()?？:：！![]"‘’“”+=-*$#@~《》< ，,/\\～…\|¯_\'')
    text_count = Counter()
    for txt in df['content']:
        for p in punc:
            txt = txt.replace(p, "")
        text_count[txt] += 1
    return dict(text_count.most_common(quantity))

#get_content_freq(df_h, 200)
#get_content_freq(df_z, 100)


def get_emotion_score(df):
    punc = list(r'.。（）()?？:：！![]"‘’“”+=-*$#@~《》< ，,/\\～…\|¯_\'')
    text_count = Counter()
    for txt in df['content']:
        for p in punc:
            txt = txt.replace(p, "")
        text_count[txt] += 1

    emotion_score_h = 0
    count = 0
    for text in text_count.keys():
        temp_res = get_sentiments(text)
        if temp_res['ret'] == 0:
            emotion_score_h += temp_res['data']['polar'] * temp_res['data']['confd'] * text_count[text] 
        count += 1
    return emotion_score_h, count

def add_emotion_score_to_df(df):
    count = 0
    n = len(df['content'])
    progress = 1
    df['emotion'] = 0

    for i in range(n + 1):
        if count == n // 1000 * progress:
            print("finished " + str(progress/10) + " %!")
            progress += 1
        text = df.iloc[i,0]
        temp_res = get_sentiments(text)
        if temp_res['ret'] == 0:
            df.iloc[i,2] = temp_res['data']['polar'] * temp_res['data']['confd']
        count += 1

add_emotion_score_to_df(df_h)
add_emotion_score_to_df(df_z)