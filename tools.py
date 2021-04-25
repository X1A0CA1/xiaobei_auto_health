import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random

def server(sckey, msg):
    if sckey is not None:
        uri = 'https://sc.ftqq.com/{}.send?text={}'.format(sckey, msg)
        requests.get(uri)
        pass
    else:
        print('SCKEY 为空，跳过推送')
        
        
def mail(my_sender, my_pass, my_user, msg):
    if my_sender is not None:
        my_sender = my_sender  # 发件人账号
        my_pass = my_pass  # 发件人邮箱授权码
        my_user = my_user  # 输入收件人账号
        content = msg  # 邮件内容
        mail_from = 'XJun'  # input('输入发件人名称:')
        mail_to = 'XJun'  # input('输入收件人名称:')
        mail_subject = '这是一封由XJun编写的Python程序自动发送的邮件'  # input('输入邮箱标题:')
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([mail_from, my_sender])
        msg['To'] = formataddr([mail_to, my_user])
        msg['Subject'] = mail_subject
        server = smtplib.SMTP_SSL("smtp.163.com", 994)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    else:
        print('邮箱为空，跳过推送')

login_url = "https://xiaobei.yinghuaonline.com/prod-api/login"
health_url = "https://xiaobei.yinghuaonline.com/prod-api/student/health"
captcha_url='https://xiaobei.yinghuaonline.com/prod-api/captchaImage'
# 请求头
headers = {
    "user-agent": "iPhone10,3(iOS/14.4) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
    "accept": "*/*",
    "accept-language": "zh-cn",
    "accept-encoding": "gzip, deflate, br"
}

random_tem_x=random.randint(3, 8)
random_tem_y=random.randint(35,36)
random_tem=random_tem_y+random_tem_x*0.1   #体温随机

location_x=113.59
location_y=23.53
random_x=random.randint(530128570557,641635986328)
random_y=random.randint(6901126798316,9222456559607)
location_x=str(location_x)+str(random_x)
location_y=str(location_y)+str(random_y)     #地址随机            

#  写自己学校的位置
health_parameter = {
    "temperature": "%s" %random_tem,                #体温为35.3~36.8的随机数
    "coordinates": "中国-广东省-广州市-从化区",
    "location": "%s,%s" %(location_x,location_y),   #地址也为范围内的随机数
    "healthState": "1",
    "dangerousRegion": "2",
    "dangerousRegionRemark": "",
    "contactSituation": "2",
    "goOut": "1",
    "goOutRemark": "",
    "remark": "无",
    "familySituation": "1"
}
