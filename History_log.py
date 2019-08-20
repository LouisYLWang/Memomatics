import pandas as pd
import sqlite3
import time
import jieba
from collections import Counter


'''
talker = "pdd003"
with sqlite3.connect(db_file) as conn:
    c = conn.cursor()
    stmt = "SELECT content FROM message WHERE talker='{}'".format(talker)
    msg = []
    for row in c.execute(stmt):
        if not row or not row[0] or row[0].find('xml') != -1:
            continue
        msg.append(row[0])
    msg = "\n".join(msg)
    wordfilter = list("abcdefghijklmnopqrstquvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ哈")
    for wf in wordfilter:
        msg = msg.replace(wf, "")
    data = " ".join(jieba.cut(msg, cut_all=True))
'''

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

df_z.to_csv('z.csv')
df_h.to_csv('h.csv')

df_all = df_cr.append(df_pc)


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
    

get_message_time(df_h)

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

word_cloud(df_z, 200)






'''
seg_list = jieba.cut(txt)
c = Counter()
for x in seg_list:
    c[x] += 1
print('常用词频度统计结果')
print(c.most_common(100))
#for (k,v) in c.most_common(100):
#    print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/3), v))
return c.most_common(100)

'''




'''
list(map(str, range(25)))
#df['content'][200:400]
df['content'][119]
df['createTime'][0]
a = df['createTime'][119]
a





from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import sqlite3


def wechat_wordcloud(talker):
    font_path = "Miui-Regular.ttf"
    data = wechat_record(talker)
    img = WordCloud(font_path=font_path, width=1400, height=1400,
                    margin=2, collocations=False).generate(data)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    img.to_file("{}.png".format(talker))


def wechat_record(talker):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    stmt = "SELECT content FROM message WHERE talker='{}'".format(talker)
    msg = []
    for row in c.execute(stmt):
        if not row or not row[0] or row[0].find('xml') != -1:
            continue
        msg.append(row[0])
    msg = "\n".join(msg)
    wordfilter = list("abcdefghijklmnopqrstquvwxyz0123456789哈")
    for wf in wordfilter:
        msg = msg.replace(wf, "")
    data = " ".join(jieba.cut(msg, cut_all=True))
    conn.close()
    return data


if __name__ == '__main__':
    talker = "wyl400421"
    wechat_wordcloud(talker)
    '''