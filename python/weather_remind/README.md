# 天气提醒脚本

我讨厌下雨天，尤其是出门却没带伞的下雨天。每到这个时候，就特羡慕大头儿子，“人家有伞，我有大头”。。。既然没有大头儿子的天赋异禀，就只能老老实实地带伞了。

蛋，总是忘了带肿么破！！！

在多次被北京的大雨拍在路上之后，我痛定思痛，决定要想个法子解决忘带伞这一世纪难题。。。

其实这个问题很好解决嘛，早晨出门前看下天气预报不就行了。对于像我这种每天能够早早起床、舒展一会儿身体、做一顿营养早餐、看一个小时书、在上班路上欣赏北京美景的人来说so easy。

才怪。

每天睡的比猪晚、起的比猪早，早晨急忙爬起来刷个牙洗个脸，连个饭都吃不上就要去挤地铁，这还天天迟到呢！哪还能想起来去看天气预报啊！！！

主动去看天气预报这个方案对我来基本无解。。。

那，就被动好了，让基友在我需要带伞的时候，主动提醒我一下吧。

好，祭出基友之友--Python！！！

我想让python做以下事情：

![流程图](流程图.png)

所以，要实现以下三部分：

1. 爬取天气数据
2. 判断是否有雨
3. 发送提醒

嗯，开搞。

#### 爬天气预报数据
先找个靠谱的天气预报网站，看了一圈，感觉这个[中国天气预报](http://www.weather.com.cn/weather/101010100.shtml)挺靠谱的，毕竟敢用“中国”命名呢。下图就是目标数据了：

![天气数据](天气数据.png)

打开浏览器控制台，找到数据在html中的位置：

![html1](html1.png)

可以看到，7天的天气数据位于 id="7d"的div标签 -> ul标签 -> li标签 中。

再看看li中的具体结构：

![html2](html2.png)


* 日期位于 li标签 -> h1标签 中；
* 天气位于 li标签 -> class="wea"的p标签 中；
* 最高温度位于 li标签 -> class="tem"的p标签 -> span标签 中；
* 最低温度位于 li标签 -> class="tem"的p标签 -> i标签 中。

数据找好了，开始爬数据出来。鉴于爬数据的逻辑简单，直接用urllib2和Beautifulsoup来做。

```
# 爬取7天内的天气数据
from bs4 import BeautifulSoup
import urllib2
def fetch_weather_datas():
    # 请求页面数据
    response = urllib2.urlopen(url='http://www.weather.com.cn/weather/101010100.shtml') 
    body = response.read()

    # 用BeautifulSoup解析，取出7天的天气数据
    soup = BeautifulSoup(body)
    tags = soup.select('#7d > ul > li')

    return ['%s\t%s\t%s\t%s' %  # 对七天的数据分别解析，将解析后的每天的数据拼接成“日期+天气+最高气温+最低气温”的字符串，\t分隔
        (
            tag.select('h1')[0].string, # 取时间数据
            tag.select('.wea')[0]['title'],  # 取天气数据
            tag.select('.tem > span')[0].string, # 取最高气温
            tag.select('.tem > i')[0].string # 取最低气温
        ) 
        for tag in tags] # 返回结果为List
```

#### 今天是否有雨？
拿到天气数据之后，要看下今天的天气如何，是否需要提醒我带伞。

```
# 传入爬到的天气数据,判断今天是否是雨天
def is_rainy_day(weather_datas):
    return '雨' in weather_datas[0] # weather_datas[0]为今天的数据
```

#### 发送提醒
因为我手机上的邮件客户端始终在后台开启，选择用邮件的方式来做提醒比较合适，所以使用了Python自带的邮件发送工具：smtplib。
需要有一个发送提醒邮件的邮箱账号，我用的是新浪的邮箱。

```
# 发送邮件
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def send_mail(receivers, datas):
    mail_host = 'smtp.sina.com'  # 设置服务器，不同的邮箱对应的smtp服务器地址不同
    mail_user = 'username'  # 用户名，发送邮件的邮箱账号的用户名
    mail_pass = 'password'  # 密码，发送邮件的邮箱密码

	# 定义邮件内容
    message = MIMEText('\n'.join(datas), 'plain', 'utf-8') # 邮件内容为爬取到的近7天天气数据
    message['From'] = Header(mail_user) # 邮件的发送方
    message['To'] = Header(','.join(receivers), 'utf-8') # 邮件的接受方，逗号分隔
    message['Subject'] = Header('天气提醒', 'utf-8') # 邮件主题

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 连接服务器， 25 为新浪邮箱 SMTP 端口号
        log('连接服务器成功..')
        smtpObj.login(mail_user, mail_pass) # 登录服务器
        log('登录邮箱服务器成功..')
        smtpObj.sendmail(from_addr=mail_user, to_addrs=receivers, msg=message.as_string()) # 发送邮件
        log('邮件发送成功..')
    except smtplib.SMTPException as e:
        log('无法发送邮件...' + e.message)


# 日志打印
import time
def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print '[%s] %s' % (timestamp, msg)
```

#### 整合
将上边编写完成的方法按下边的方式整合到一起，就是一个能够发送天气提醒的脚本了：

```
try:
    weather_datas = fetch_weather_datas() # 爬取天气数据
    if is_rainy_day(weather_datas):	# 今天是否是雨天
        send_mail('xxxx@sina.com', weather_datas) # 发送天气数据到目标邮箱
    else:
        log('今天天气良好..')
except:
    log('出错..')
```

#### 定时执行
写完脚本后，我希望这个脚本能在每天早晨6点30分执行，这样我就能在醒来的第一时间就能看到提醒邮件并带上雨伞了。

首先需要一个能联网的服务器，将脚本放在服务器中。

然后，用crontab来做定时的任务（linux环境）。执行：

`crontab -e`

此时会进入进入vim界面，进入编辑模式，输入：

`30 6 * * * /usr/bin/python xxxx/weather.py >> run.log`

保存，此时定时任务就跑起来了，日志记录在run.log文件中。

> 具体的cron表达式语法在网上有很多教程，就不细说了。

#### 完成
不必再羡慕大头儿子了！虽然他有大头，但是我有伞啊~
