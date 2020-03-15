## **sign_zjgsu-program**

**浙江工商大学云战役平台自动签到系统：**

​	**安装依赖库**：

		import urllib.request
		import http.cookiejar
		import time
		import json
		import win32con
		import win32api
		import os,sys
		import random
**实现逻辑**：

​	经过前期测试，该网页端必须通过手机端才能进入，所以电脑用fiddle抓包时则必须通过手机实现，然后通过电脑模拟头文件使用电脑访问主页，再通过对cookie和post数据的解析，完成网页自动签到的程序。

![image-20200315155552209](C:\Users\starscq\AppData\Roaming\Typora\typora-user-images\image-20200315155552209.png)

**程序主体编写** ：

1、访问主页：    

​	按照签到顺序先进主页然后转到登录页面，签到页面输入用户名密码post数据上去返回主页内容，主页点击提交，post所填数据到服务器端返回报送成功页面。整个过程中的cookie应该一直为访问登录也免得cookie，所以必须先访问主页得到此时的cookie以及userid，cookie在每次post数据到服务器端的时候都必须带着，不然会被服务器拒绝访问而登录失败。     注意：访问过程中的User-Agent必须是Android设备，电脑设备会被拒绝访问，需要通过fiddle抓包把手机访问时的user-agent保存下来作为访问签到过程中的头文件

2、登录主页：    

​	主页登录过程中需要学生用户名和密码作为post数据，并且带着访问主页的cookie通过post方式给服务器，此时服务器会返回签到页面，里面有自己的签到信息，通过fiddle可以很清楚看到提交到服务器的数据是怎么选择出来的，此时则需要对返回的主页数据进行分析整理，找出post到服务器端的主要数据通过观察每个post的value通过数据处理，整理得到所需要的提交的数据。

 3、提交数据：     

​	分析get到的数据包通过程序处理得到签到提交信息，通过encode编码post到服务器端，返回签到成功页面。

**程序功能增加**  

​	1、开机自启动（修改注册表）  

​	2、开机启动时间延缓（防止网络加载过慢），定点随机时间签到  

​	3、打包exe  

​	4、log文件进行远程调试



**程序bug修改**  

​	1、双击启动正常，开机自启动异常 

​	2、goto语句导致程序出现bug以及程序的不正常退出  

​	3、函数命名不够规范