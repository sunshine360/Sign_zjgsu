# -*- coding:UTF-8 -*-
#!/use/bin/env python
# -*- coding:UTF-8 -*-
#@Time  : 2020/02/15 23:10
#@Author: sunshine
#@File  : demo_1.py
import urllib.request
import http.cookiejar
import time
import json
import win32con
import win32api
import os,sys
import random


Cookies = {}
Data = {}

exeName='sign_zjgsuv3'
run_path = sys.argv[0]
#print(run_path)

def addfile2autorun():#注册表的修改
    #global run_path
    runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_ALL_ACCESS)
    exe_path = sys.argv[0]
    #exe_path = run_path + '\\' + exeName  + '.exe'
    #print(exe_path)
    #读取键值
    try:

        value, key_type = win32api.RegQueryValueEx(hKey, exeName)

    except Exception as e:

        win32api.RegSetValueEx(hKey,exeName, 0, win32con.REG_SZ, exe_path)
        #log2(exe_path)
    #win32api.RegDeleteValue(hKey, exeName)
    win32api.RegCloseKey(hKey)


#访问主页，获取cookie
def get_index():

    url='https://nco.zjgsu.edu.cn'#访问的主页
    use = 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; HWI-AL00 Build/HUAWEIHWI-AL00;) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.8'
    header={}
    header['User-Agent'] = use
    request = urllib.request.Request(url, headers=header)
    '''
	获取Cookie，并保存到CookieJar()对象中
	'''
    #====================================
    #构建一个CookieJar对象实例来保存cookie
    cookiejar = http.cookiejar.CookieJar()
    #使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
    handler = urllib.request.HTTPCookieProcessor(cookiejar)
    #通过build_opener()来构建opener
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    #以get方法访问页面，访问之后会自动保存cookie到cookiejar中
    #opener.open("http://www.baidu.com")
    #可以按照标准格式将保存的Cookie打印出来
    #reponse = urllib.request.urlopen(request)


    try:
        reponse = urllib.request.urlopen(request)
        log2('Internet Ok\n')
    except urllib.error.URLError:
        log2('Internet Error\n')
        #print('Internet Error，请检查网络连接并重试')
        temp = input("按任意键退出......")
        return False
    #解析cookie
    cookieStr = ""
    for item in cookiejar:
        cookieStr = cookieStr + item.name + "=" +item.value + ";"

    cookieStr = cookieStr[:-1]
    list = reponse.readlines()
    uuid = ''
    for text in list:
        if text.decode('utf-8').find('var uuid') != -1:
            text= (text.decode('utf-8')).replace(" ","")
            text= text.replace("	","")
            #print(text)
            len=text.find('"') + 1
            text=text[len:]
            len=text.find('"')
            text=text[:len]
            #print(text)		
            Cookies['_ncov_uuid'] = text
    log2(Cookies)
    return cookieStr

#解析get数据，为进行post数据做准备
def formstr(html):

    global Data #初始化全局变量

    list_post = [
            'uuid',
                'currentResd',
            'fromHbToZjDate',
        'fromHbToZj',
            'fromWtToHzDate',
            'fromWtToHz',
            'meetDate',
            'meetCase',
            'travelDate',
            'travelCase',
            'medObsvReason',
            'medObsv',
            'belowCaseDesc',
            'belowCase',
            'temperature',
            'notApplyReason',
            'hzQRCode',
            'specialDesc'        
        ]  
    #print(html)
    #print(type(html))
    list1 = []
    list1.append(Cookies['_ncov_uuid'])
    for item in html:
        item = item.decode('utf-8')
        if (item.find('input') != -1) or (item.find('textarea') != -1) :
            item = item.replace("	","")
            if item.find('type="hidden"') != -1:
                continue
            #len = item.find('>')
            #item = item[:len]
            if item.find("input") != -1:
                if item.find('placeholder') != -1:
                    len = item.find('value')
                    item = item[len:]
                if item.find('type="date"') != -1 or item.find('type="number"') != -1:
                    len = item.find('value')
                    item = item[len:]
                if item.find ('type="radio"') != -1:
                    if item.find('checked') != -1:
                        len = item.find('value')
                        item = item[len:]
                    else:
                        continue
            if item.find('textarea') != -1:
                if item.find('/textarea')!= -1:
                    len = item.find('/textarea')
                    item = item[:len]
            #print(item)
            if item.find('value') != -1:
                len = item.find('"') + 1
                item = item[len:]
                if item.find('"') == 0:
                    item = ""
                else:
                    len = item.find('"')
                    item = item[:len]
            #print(item)
            if item.find('name=') != -1:
                len = item.find('name=')
                item = item[len:]
                len = item.find('>') + 1
                item = item[len:]
                if item.find('<') == 0:
                    item = ""
                else:
                    len = item.find('<')
                    item = item[:len]                
            list1.append(item)

    Data = dict(zip(list_post, list1))
    #print('Data:',Data)


def login(cook):
    url = 'https://nco.zjgsu.edu.cn/login'
    #登录信息处理
    data_keys = ['name','psswd']
    data_values = []
    with open(run_path + 'login.txt', 'r') as fp:
        login_data = fp.readlines()
    for i in login_data:
        len = i.find(':') + 1
        i = i[len:]
        i = i.replace('\n','')
        data_values.append(i)
    #print(data_values)
    data = dict(zip(data_keys,data_values))
    log2(data)
    postdata = urllib.parse.urlencode(data).encode('utf8')
        #模拟头文件
    use = 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; HWI-AL00 Build/HUAWEIHWI-AL00;) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.8'
    cookie = cook
    header={}
    header['User-Agent'] = use
    header['Cookie'] = cookie
    log2(header)
    log2(postdata)
    request = urllib.request.Request(url, postdata, headers=header)
    reponse = urllib.request.urlopen(request)
    html = reponse.readlines()
    #print(temp.decode('UTF-8'))
    log2(html)
    bSignOK = False
    #检测是否当天已经签到成功
    for item in html:
        item = item.decode('utf-8')
        if item.find('<h3 class="text-red">') != -1:
            if item.find('当天') != -1 :
                bSignOK = True
            else:
                break	

    if bSignOK: 
        #print(item)
        logout(header)
    else:
        Cookies['_ncov_username'] = data['name']
        len = cook.find('=') + 1
        Cookies['zjgsusessionsid'] = cook[len:]
        formstr(html)

    return bSignOK

#登录主页
def sign():


    postData = urllib.parse.urlencode(Data).encode('utf8')
    log2('postData:')
    log2(postData)
    url = 'https://nco.zjgsu.edu.cn/'

    use = 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; HWI-AL00 Build/HUAWEIHWI-AL00;) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.8'
    log2(Cookies)
    cookieStr =""
    for item,var in Cookies.items():
        cookieStr = cookieStr + ' {v}={k};'.format(v = item, k = var)
        #test=item.key()
        #print(item,var)
    cookieStr = cookieStr[:-1]
    log2(cookieStr)

    header={}
    header['User-Agent'] = use
    header['Cookie'] = cookieStr
    header['Origin'] = 'https://nco.zjgsu.edu.cn'
    header['Referer'] = 'https://nco.zjgsu.edu.cn/'
    log2(header)

    request = urllib.request.Request(url, postData,headers=header)
    reponse = urllib.request.urlopen(request)
    temp = reponse.readlines()
    log2(temp)

def log():
    with open(run_path + 'log_times.txt','a+') as fp:

        #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) #2020-02-17 22:55:18
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        fp.write('签到成功\n')

#把必要的过程文件写下来方便后期进行bug修复

def log2(logvar):
    #print(logvar)
    with open(run_path + 'log.txt','a+') as fp:
        #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) #2020-02-17 22:55:18
        fp.write(time.strftime('\n%Y-%m-%d %H:%M:%S ',time.localtime(time.time())))
        if(type(logvar) is list):
            fp.write("list:\n")
            for val in logvar:
                temp = val.decode('utf-8')
                fp.write(temp)
        elif (type(logvar) is dict):
            fp.write("dict:\n")
            jsObj = json.dumps(logvar)
            fp.write(jsObj) 
        elif (type(logvar) is bytes):
            temp = logvar.decode('utf-8')
            fp.write(temp)
        else:
            fp.write(logvar) 
            
#每天只提交一次，防止被服务器拒收
def logout(header):
    url = 'https://nco.zjgsu.edu.cn/logout?'
    request = urllib.request.Request(url, headers=header)
    reponse = urllib.request.urlopen(request)
    log2('logout')
    #print('logout')

def check_sign_time(rant):

    #签到时间，0:00 - 10:00
    timer1 = '00:02:00'
    timer2 = '10:00:00'
    now_time_int = time.time()
    now_rant_time_str = time.strftime('%H:%M:%S', time.localtime(now_time_int - rant))
    if now_rant_time_str < timer2:
        #print('rant:', rant)	
        #print('now time:', time.strftime('%H:%M:%S', time.localtime(now_time_int)))
        #print('rant time:',now_rant_time_str)
        return True
    return False


if __name__ == "__main__":

    rant = random.randint(1,600)

    while check_sign_time(rant) is False:
        #print('not sign time')
        time.sleep(100)

    #print('can sign time')
    addfile2autorun()

    time.sleep(5) #等待开机网络初始化
    print(run_path)
    run_path = run_path.replace('\\','/')
    run_path = run_path[:run_path.rfind('/')+1]

    #print(run_path + '/log.txt')
    #exit()
    with open(run_path + 'log.txt','w') as fp:
        fp.write('')

    ret = get_index()
    if (ret is not False ) and Cookies != {} :
        needSign =login(ret)
        if needSign is False:
            #print("start sign")
            sign()
            log()
            #print("ok")

