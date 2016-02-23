
#-*- coding:utf-8 -*- 
import requests
import re
import pickle
#from bs4 import BeautifulSoup


headers_base = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 
    'Referer': 'http://www.zhihu.com/',
}

def get_users(content=None):
    print content
    users = re.search(r'<a title="*>', content)
    print users.group(0)

def save_cookies(requests_cookiejar,filename):
    with open(filename,'wb') as f:
        pickle.dump(requests_cookiejar,f)
    f.close()

def get_captcha(s,captcha_url):
    captcha = s.get(captcha_url, stream=True)
    print captcha
    f = open('captcha.jpg', 'wb')
    for line in captcha.iter_content(10):
        f.write(line)
    f.close()
   
    print u'输入验证码:' 
    captcha_str = raw_input()
    return captcha_str

def get_xsrf(s,url=None):
    global headers_base
    r = s.get(url, headers=headers_base)        
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
    if xsrf == None:
        return ''
    else:
        return xsrf.group(0)
    
def login(email,passwd):
    global headers_base
    url = 'http://www.zhihu.com'
    login_url = 'http://www.zhihu.com/login/email'
    captcha_url = 'http://www.zhihu.com/captcha.gif'#验证码url
    #email = email.encode('utf-8')
    #passwd = passwd.encode('utf-8')
    login_data = {
        'email': email,
        'password': passwd,
        'rememberme': 'true',
    }

    s = requests.session()
    xsrf = get_xsrf(s,url)
    print xsrf
    login_data['_xsrf'] = xsrf.encode('utf-8')

    captcha_str = get_captcha(s,captcha_url) 
    login_data['captcha'] = captcha_str

    res = s.post(login_url, headers=headers_base, data=login_data)
    print res.status_code

    m_cookies = res.cookies
    #print m_cookies
    save_cookies(m_cookies,'cookies.txt')
    
    test_url = 'https://www.zhihu.com'
    res = s.get(test_url, headers=headers_base) 

    get_users(res.text)
    

if __name__=='__main__':
    login('1206885945@qq.com','19910118vhw')
