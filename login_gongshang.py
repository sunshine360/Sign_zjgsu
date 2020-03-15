#-*- coding:utf-8 -*-
# 方便延时加载

import time
from selenium import webdriver

#user = input("学号：")
#password = input("密码：")

# 进入浏览器设置修改hearder
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
#options.add_argument('--incognito')
#options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 9; zh-CN; HWI-AL00 Build/HUAWEIHWI-AL00;) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.8"')
browser = webdriver.Chrome(chrome_options=options)
#登录页面
url='https://nco.zjgsu.edu.cn/login'
browser.get(url)
#窗口最大化
browser.maximize_window()

# 找到输入框,发送要输入的用户名和密码,模拟登陆
browser.find_element_by_xpath(
    "//*[@id='name']").send_keys('1811060504')
browser.find_element_by_xpath(
    "//*[@id='psswd']").send_keys('194070')
# 在输入用户名和密码之后,模拟点击登陆按钮
browser.find_element_by_xpath("//*[@id='login-btn']").click()
time.sleep(2)#延时2s

#点击登陆后的页面中的签到,跳转到签到页面模拟点击签到
browser.find_element_by_xpath("/html/body/form/div[2]/button").click()
time.sleep(2)

print("签到成功")
#运行成功,退出浏览器
browser.quit()
