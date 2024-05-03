'''
cookie管理器
主要调用get_cookies()
'''

import json  
import os  
import tkinter as tk  
from tkinter import simpledialog  
from utils import m_paths  
from utils.print_if import print_if
 

cookie_json_path=m_paths.cookie_json_path
cookie_txt_path=m_paths.cookie_txt_path
saved_cookies={}

def split_cookie_and_save(cookieStr):  
    global saved_cookies
    cookie_dict = {}  
    for line in cookieStr.splitlines():  
        if line.strip():  # 检查这一行是否为空
            lineSplit=line.split('\t')
            key, value = lineSplit[0].strip(), lineSplit[1].strip()  # 使用制表符（tab）作为分隔符，并取出第一、二个元素作为key和value，同时去除空格  
            if('nga' in lineSplit[2] or '178' in lineSplit[2]):
                cookie_dict[key] = value  
      
    #settings = cookieDict  
    saved_cookies=cookie_dict
 
    with open(cookie_json_path, 'w', encoding='utf-8') as f:  
        json.dump(cookie_dict, f)  
        print_if(f'Cookie已成功保存！\n{cookie_dict}',3) 
        return cookie_dict  # 成功保存后返回cookie_dict  
  
def user_input_cookie():  

    cookie_str = simpledialog.askstring("Cookie Input", "请输入你的cookie:")  
    print_if(cookie_str)
    if len(cookie_str) > 100: 
        cookie_dict= split_cookie_and_save(cookie_str)  # 如果cookieStr长度大于10，则调用SplitCookieAndSave方法并返回其结果  
        print_if(f'cookie_dict\n{cookie_dict}')
        return cookie_dict
    else:  
        print_if("Cookie字符串太短，请重新输入！",2)  # 如果cookieStr长度小于等于10，则输出提示信息并返回None表示调用失败  
        return user_input_cookie()  # 递归再次调用
  

def get_cookies():
    '''获取Cookie'''
    
    #如果存在savedCookies，则直接返回
    global saved_cookies
    if len(saved_cookies)>100:
        return saved_cookies

    #否则， 读取文件

    need_reinput=False
    # 检查文件是否存在  
    if os.path.exists(cookie_json_path) and os.path.getsize(cookie_json_path) > 100:  
        with open(cookie_json_path, 'r', encoding='utf-8') as f: 
            cookies_dict = json.load(f)  
            if len(cookies_dict)<3:
                need_reinput=True
            else:
                saved_cookies=cookies_dict
                #print(f"GetCookies Success")

            #f.seek(0)
            #print(f'f.read()\n{f.read()}')
    else:  
        need_reinput=True

    if need_reinput:
        print_if(f"File {cookie_json_path} does not exist or is empty.",1)  
        saved_cookies = user_input_cookie()

    return saved_cookies
 


# 在开始运行时自动调用GetCookie方法，这里使用的是懒加载的方式，也可以在程序初始化时调用GetCookie方法。  
print_if(get_cookies())

#UserInputCookie()