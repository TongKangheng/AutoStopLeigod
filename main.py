from selenium import webdriver
import time
import requests
import json

# 从json文件读入雷神的账号密码
def load_login_data(path:str='login_data.json'):
    with open(path,'r') as file:
        data=json.load(file)
        return data['phone_number'],data['password']

# 运行时是否打开浏览器窗口，默认不打开，完全后台运行。
def get_chrome_options(open_window:bool=False)->webdriver.ChromeOptions:
    option=webdriver.ChromeOptions();
    if open_window==False:
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        option.add_argument('window-size=1920x3000')    # 如果没有这句话，程序在不打开浏览器窗口时运行报错
    return option

# 通过模拟操作登录雷神加速器官网网页，获取对应的account_token
def get_account_token(url:str='https://vip-jiasu.nn.com/login.html?region_code=1&language=zh_CN'):
    phone_number,password=load_login_data()
    option=get_chrome_options()
    browser=webdriver.Chrome(options=option)
    browser.get(url=url)
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/ul[1]/li[1]/input').clear()
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/ul[1]/li[1]/input').send_keys(phone_number)   # 输入账号
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/ul[1]/li[2]/input').clear()
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/ul[1]/li[2]/input').send_keys(password) # 输入密码
    time.sleep(1) # 输入完成后不能立即点击登录，否则会报错“账号不存在”
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/a').click()
    time.sleep(1) # 等待页面跳转加载完成
    data = browser.execute_script('return localStorage.getItem("account_token");')
    data=eval(data)
    account_token=data['account_token']
    return account_token

def auto_stop_leigod():
    account_token=get_account_token()

    # 用charles抓包，一句抓到的request构造请求头
    headers = {
        'Host': 'webapi.nn.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://vip-jiasu.nn.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://vip-jiasu.nn.com/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    data = '{"account_token":"' + account_token + '","lang":"zh_CN"}' # 根据charles抓包的数据构造请求数据
    response = requests.post('https://webapi.nn.com/api/user/pause', headers=headers, data=data) # 发送暂停时间请求

if __name__=='__main__':
    auto_stop_leigod()