import requests
import urllib3
import tools
import json
import base64
import os
import random

username = os.environ.get('IDCODE')
password = os.environ.get('PASSWORD')
location = os.environ.get('LOCATION')
sckey = os.environ.get('SCKEY')
my_sender = os.environ.get('MYSENDER')
my_pass = os.environ.get('MYPASS')
my_user = os.environ.get('MYUSER')

if username == None or password == None or location == None:
    # 引入 config 文件
    import config
    username = config.username
    location = config.location
    base64_password = str(base64.b64encode(bytes(config.password, encoding="utf-8")), encoding="utf-8")
else:
    base64_password = str(base64.b64encode(bytes(password, encoding="utf-8")), encoding="utf-8")

bzd = location.split(',')
location_x = str(bzd[1])
location_y = str(bzd[0])

#reqloc = "https://api.xiaobaibk.com/api/location/?location=" + bzd[1] + "," + bzd[0]
#result = requests.get(reqloc).text
#location_r_data = json.loads(result)

pool = urllib3.HTTPSConnectionPool(
	"117.34.13.47",
	assert_hostname="api.xiaobaibk.com",
	server_hostname="api.xiaobaibk.com",
)

result = pool.urlopen(
    "GET",
    "/api/location/?location=" + str(bzd[1]) + "," + str(bzd[0]),
     headers={"Host": "api.xiaobaibk.com"},
     assert_same_host=False
 )

location_r_data = json.loads(result.data)

if location_r_data['status'] == 0:
    province = location_r_data['result']['addressComponent']['province']
    city = location_r_data['result']['addressComponent']['city']
    district = location_r_data['result']['addressComponent']['district']
    zh_location = '中国-' + province + '-' + city + '-' + district
else:
    print("位置获取失败")
    os._exit(0)

#体温随机
random_tem_x=random.randint(3, 6)
random_tem_y=random.randint(35,36)
random_tem=random_tem_y+random_tem_x*0.1

#位置随机

rand = random.randint(1111, 9999)
location_x = location.split(',')[0].split('.')[0] + '.' + location.split(',')[0].split('.')[1][0:2] + str(rand)
location_y = location.split(',')[1].split('.')[0] + '.' + location.split(',')[1].split('.')[1][0:2] + str(rand)

health_parameter = {
    "temperature": "%s" %random_tem,                #体温为35.3~36.8的随机数
    "coordinates": zh_location,
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

if __name__ == '__main__':
    # 抓个滑动验证的包
    # {'msg': '操作成功', 'img': 'xxxxxx', 'code': 200, 'showCode': '2YG2', 'uuid': '25c897f5c0ca4e79bbce43318900266b'}
    captcha = requests.get(tools.captcha_url, headers=tools.headers).text
    code = json.loads(captcha)['showCode']
    uuid = json.loads(captcha)['uuid']
    # 登录时需要 post 的信息
    login_parameter={
        "username": username,
        "password": base64_password,
        "code": code,
        "uuid": uuid
    }

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
        post_health = requests.post(tools.health_url, headers=headers, json=health_parameter)

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
            print("返回的错误/打卡结果是:   " + status)
            tools.server(sckey, "北温打失败，请手动北温打")
            tools.mail(my_sender, my_pass, my_user, "北温打失败，请手动北温打")
