import requests


def server(sckey, msg):
    if sckey is not None:
        uri = 'https://sc.ftqq.com/{}.send?text={}'.format(sckey, msg)
        requests.get(uri)
        pass
    else:
        print('SCKEY 为空，跳过推送')


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

#  瞎几把写个西安周边的位置
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
