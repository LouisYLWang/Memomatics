import pandas as pd
import sqlite3
import time


with sqlite3.connect(db_file) as conn:
    df = pd.read_sql_query("SELECT * FROM message", con=conn)


"SELECT content FROM message WHERE talker='{}'".format("1132909349@chatroom")

talker = "1132909349@chatroom"
db_file = r'resource\wechat_log\decrypted_database.db'
with sqlite3.connect(db_file) as conn:
    c = conn.cursor()
    stmt = "SELECT content FROM message WHERE talker='{}'".format(talker)
    msg = []
    for row in c.execute(stmt):
        if not row or not row[0] or row[0].find('xml') != -1:
            continue
        msg.append(row[0])
    msg = "\n".join(msg)
    wordfilter = list("abcdefghijklmnopqrstquvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for wf in wordfilter:
        msg = msg.replace(wf, "")
    data = " ".join(jieba.cut(msg, cut_all=True))



#df['content'][200:400]
df['content'][119]
df['createTime'][0]
a = df['createTime'][119]
a
time.ctime(1463055892)
df['content'][df['content'].str.contains('~SEMI_XML~')]


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
    wordfilter = list("abcdefghijklmnopqrstquvwxyz0123456789")
    for wf in wordfilter:
        msg = msg.replace(wf, "")
    data = " ".join(jieba.cut(msg, cut_all=True))
    conn.close()
    return data


if __name__ == '__main__':
    talker = "wyl400421"
    wechat_wordcloud(talker)