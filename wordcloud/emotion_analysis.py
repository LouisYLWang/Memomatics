import hashlib
import time
import random
import string
from urllib.parse import quote
import requests
 
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
