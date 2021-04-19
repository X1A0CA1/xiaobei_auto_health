import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

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

#  写自己学校的位置
health_parameter = {
    "temperature": "35.8",
    "coordinates": "undefined-广东省-广州市-从化区",
    "location": "113.59641635986328,23.539222456559607",
    "healthState": "1",
    "dangerousRegion": "2",
    "dangerousRegionRemark": "",
    "contactSituation": "2",
    "goOut": "1",
    "goOutRemark": "",
    "remark": "无",
    "familySituation": "1"
}
