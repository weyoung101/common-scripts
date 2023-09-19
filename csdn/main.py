#####
# CSDN 小程序签到
####

import getCSDNXCaData
from signUpUtils import RandomUserAgent, LoadEnv
import requests
import json

jwt_token = LoadEnv.load_env().get('jwt_token')
cookie = LoadEnv.load_env().get('cookie')


def wxAppSignIn():
    # 获取签名参数
    caMap = getCSDNXCaData.get_all_x_ca_data("post", "/points/api/task/activity/signin/addSignin")

    # print('caMap的值： ', caMap)

    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': RandomUserAgent.get_header(),
        'x-ca-key': caMap.get("x-ca-key"),
        'x-ca-nonce': caMap.get("x-ca-nonce"),
        'x-ca-signature': caMap.get("x-ca-signature"),
        'x-ca-signature-headers': 'x-ca-key,x-ca-nonce',
        'jwt-token': jwt_token,
        'cookie': cookie,
        'referer': 'https://servicewechat.com/wx94ba57502711952f/120/page-frame.html'
    }

    # 创建要发送的 JSON 数据
    data = {
        "activityId": 1005,
        "pageNum": 2,
        "pageSize": 4,
        "queryType": "noCash"
    }
    # 将 JSON 数据转换为字符串
    json_data = json.dumps(data)

    # 发送 POST 请求
    url = 'https://miniapp-api.csdn.net/points/api/task/activity/signin/addSignin'  # 你的 API 地址
    response = requests.post(url, headers=headers, data=json_data)

    # 检查响应
    if response.status_code == 200:
        print('请求成功！')
        response_data = response.json()  # 如果响应也是 JSON 格式的话
        print(response_data)
    else:
        print(f'请求失败，状态码：{response.status_code}')
        print(response.text)  # 如果响应包含错误信息


if __name__ == '__main__':
    wxAppSignIn()
