#-*- coding:utf-8 -*-

#Author:  @zhangwen
#Created in 15/01/2016
#Functions: Search the questions about the query word that you input\
#Write the html into the zhuhu.txt.

import requests
import re
import pickle
import json
import sys
from zhihu_login import headers_base
'''def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
cookies = load_cookies('cookies.txt')'''

def zhihu_search():
    f = open('zhihu.txt','w+')
    s = requests.session()
    
    print 'Please Input The Keywords'
    query = raw_input('>').decode(sys.stdin.encoding)#解码成unicode

    '''per_url = 'https://www.zhihu.com/r/search?q=%E5%B1%81%E8%82%A1&range=&type=question&offset=10'
    per_html = s.get(per_url,cookies=cookies)
    jsondata = json.loads(per_html.content)
    keylist = jsondata.keys()
    for key in keylist:
        print key'''
    search_url = 'https://www.zhihu.com/r/search?q='+query+'&range=&type=question&offset='
    for offset in range(0,31,10):
        per_url = search_url+str(offset)
        per_html = s.get(per_url,headers=headers_base)
        if per_html.status_code==200:
            jsondata = json.loads(per_html.content)#jsondata is dict
            text = jsondata['htmls']#text is list
            for key in text:
                f.write(key)
    f.close()

if __name__ == '__main__':
    zhihu_search()
