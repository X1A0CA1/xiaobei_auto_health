import requests
import tools
import json
import base64
import os

username = os.environ.get('IDCODE')
password = os.environ.get('PASSWORD')
sckey = os.environ.get('SCKEY')
my_sender = os.environ.get('MYSENDER')
my_pass = os.environ.get('MYPASS')
my_user = os.environ.get('MYUSER')
print(sckey,my_sender,my_pass,my_user)
if username == None or password == None:
    # 引入 config 文件
    import config
    username = config.username
    base64_password = str(base64.b64encode(bytes(config.password, encoding="utf-8")), encoding="utf-8")
else:
    base64_password = str(base64.b64encode(bytes(password, encoding="utf-8")), encoding="utf-8")


# 抓个话动滑动验证的包
captcha = requests.get(tools.captcha_url, headers=tools.headers)
captcha = json.loads(captcha.text)
# {'msg': '操作成功', 'img': 'xxxxxx', 'code': 200, 'showCode': '2YG2', 'uuid': '25c897f5c0ca4e79bbce43318900266b'}
# 抓出来的值像上面这样


code = captcha['showCode']
uuid = captcha['uuid']
# 登录时需要 post 的信息
login_parameter={
    "username": username,
    "password": base64_password,
    "code": code,
    "uuid": uuid
}

if __name__ == '__main__':
    # 发送请求
    login_r = requests.post(tools.login_url, headers=tools.headers, json=login_parameter)

    # 格式化为 json
    json_login_r = json.loads(login_r.text)
    login_status = json_login_r["msg"]
    if login_status == "用户不存在/密码错误":
        print("用户不存在或密码错误")
        tools.server(sckey, "用户不存在或密码错误")
        tools.mail(my_sender, my_pass, my_user, "用户不存在或密码错误")
    elif login_status != "操作成功":
        print("我也不知道发生啥了，自己手动北温打吧？")
        print("返回的登录结果是：  " + login_status)
        tools.server(sckey, "北温打失败，请手动北温打")
        tools.mail(my_sender, my_pass, my_user, "北温打失败，请手动北温打")
    else:
        # 拿到 token
        login_token = json_login_r["token"]

        # 重新赋值 token
        headers = {
            "user-agent": "iPhone10,3(iOS/14.4) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
            "accept": "*/*",
            "accept-language": "zh-cn",
            "accept-encoding": "gzip, deflate, br",
            "authorization": login_token
        }

        # post 请求
        post_health = requests.post(tools.health_url, headers=headers, json=tools.health_parameter)

        # 格式化为 json
        json_post_health = json.loads(post_health.text)

        # 判断北温打是否成功
        status = json_post_health["msg"]
        if status == "操作成功":
            print("北温打完毕。")
            tools.server(sckey, "北温打完毕")
            tools.mail(my_sender, my_pass, my_user, "北温打完毕")
        else:
            print("我也不知道啥情况，自己看输出结果 debug 下或者自己手动北温打吧？")
            print("返回的打卡结果是:   " + status)
            tools.server(sckey, "北温打失败，请手动北温打")
            tools.mail(my_sender, my_pass, my_user, "北温打失败，请手动北温打")
