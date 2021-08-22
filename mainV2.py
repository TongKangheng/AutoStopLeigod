import requests
import json
from hashlib import md5
import warnings

warnings.filterwarnings('ignore')

def load_login_data(path:str='login_data.json'):
    with open(path,'r') as file:
        data=json.load(file)
        return data['phone_number'],data['password']

def get_account_token():
    phone_number, password = load_login_data()
    password=md5(password.encode('utf-8')).hexdigest()
    headers = {
        'Host': 'webapi.nn.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://jiasu.nn.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://jiasu.nn.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = '{"username":"'+str(phone_number)+'","password":"'+password+'","user_type":"0","src_channel":"guanwang","country_code":86,"lang":"zh_CN","region_code":1,"account_token":null}'
    response = requests.post('https://webapi.nn.com/api/auth/login',headers=headers, data=data,verify=False)
    data=response.content
    data=json.loads(data)
    return data['data']['login_info']['account_token']

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
    response = requests.post('https://webapi.nn.com/api/user/pause', headers=headers, data=data,verify=False) # 发送暂停时间请求

if __name__=='__main__':
    auto_stop_leigod()