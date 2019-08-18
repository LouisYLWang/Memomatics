import pandas as pd
import sqlite3

db_file = r'resource\wechat_log\decrypted_database.db'
with sqlite3.connect(db_file) as conn:
    df = pd.read_sql_query("SELECT * FROM message", con=conn)

#df['content'][200:400]