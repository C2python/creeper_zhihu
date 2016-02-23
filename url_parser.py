#-*- coding:utf-8 -*- 
import requests
import re
import pickle
import os
from zhihu_login import headers_base
import json


def get_xsrf(url=None):
    global headers_base
    r = requests.get(url, headers=headers_base)        
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
    if xsrf == None:
        return ''
    else:
        return xsrf.group(0)
    
_xsrf = get_xsrf('http://www.zhihu.com')

#Author: ZhangWen
#Created in 15/01/2015
#Functions: Read the html from zhihu.txt. Parse the html, get the answer about each question
#Get the Picture. Input the directionary that imag stored, and image name.

number = 1

'''def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)'''
    
def get_img(img_url,path):
    global number
    list_url = img_url.split('/')
    my_file = list_url[-1]
    number = number+1
    img = requests.get(img_url,stream=True)
    
    if img.status_code == 200:
        with open(os.path.join(path,my_file),'wb') as f:
            for chunk in img.iter_content(1024):
                f.write(chunk)
        f.close()


def get_awimg(url=None):
    global _xsrf
    pagesize = 50
    offset = 0
    #cookies = load_cookies('cookies.txt')
    
    if url is None:
        return []
    url_list = url.split('/')
    url_token = url_list[-1]
    #print url_token

    url_content = requests.get(url).text
    answers = re.findall('h3 data-num="(.*?)"', url_content)
    num_anws = int(answers[0])
    img_set = []
    
    for offset in range(0,num_anws+1,pagesize):        
        post_url = 'https://www.zhihu.com/node/QuestionAnswerListV2'
        params = json.dumps({
            'url_token':int(url_token),
            'pagesize':pagesize,
            'offset':offset
            })
        data = {
            '_xsrf':_xsrf,
            'method':'next',
            'params':params
            }
        contents = requests.post(post_url,data=data,headers=headers_base)
        #print contents.status_code
        jsondata = json.loads(contents.content)
        answer_list = jsondata["msg"]
        #img_list = re.findall('img .*?src="(.*?_b.*?)" ', ''.join(answer_list))
        img_list = re.findall(r'(?<=data-actualsrc=")[^"]*(?=">)', ''.join(answer_list))
        img_set.extend(img_list)
    return img_set

def parse_myurl(url,path):

    img_set = get_awimg(url)
    for img_url in img_set:
        print img_url
        get_img(img_url,path)

def get_url(text):
    base_url = 'https://www.zhihu.com'
    result = []
    items = re.findall(r'(?<=<div class="title"><a target="_blank" href=")[^"]*(?=" class="question-link">)',text)
    for item in items:
        absolute_url = base_url+item
        #print absolute_url
        result.append(absolute_url)
    return result

def save_img(text):
    
    print 'Please input the directionary'
    dir_file = raw_input('>')
    path = 'E:\python\pic\\'+dir_file
    if not os.path.isdir(path):
        os.mkdir(path)

    #print 'Please input the img name'
    #filename = raw_input('>')
        
    result = get_url(text)
    for url_question in result:
        #print url_question
        parse_myurl(url_question,path)


if __name__=='__main__':
    f_html = open('zhihu.txt','r+')
    text = f_html.read()
    save_img(text)
    f_html.close()



