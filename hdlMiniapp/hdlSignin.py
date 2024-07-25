#####
# 海底捞 小程序签到
####

from signUpUtils import RandomUserAgent, LoadEnv
import requests
import json

# 自行抓包找cookie---------------------------------------------
cookie = LoadEnv.load_env().get('hdl_cookie')
_haidilao_app_token = LoadEnv.load_env().get('_haidilao_app_token')
# 自行抓包找cookie---------------------------------------------

def signInHDL():
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': RandomUserAgent.get_header(),
        '_haidilao_app_token': _haidilao_app_token,
        'cookie': cookie,
        'origin': 'https://superapp-public.kiwa-tech.com',
        'referer': 'https://superapp-public.kiwa-tech.com/app-sign-in/?SignInToken=TOKEN_APP_58053575-b4bd-43e1-81c2-0ed5658f3eed&source=MiniApp'
    }

    # 创建要发送的 JSON 数据
    data = {
        "signinSource": "MiniApp"
    }
    # 将 JSON 数据转换为字符串
    json_data = json.dumps(data)

    # 发送 POST 请求
    url = 'https://superapp-public.kiwa-tech.com/activity/wxapp/signin/signin'
    response = requests.post(url, headers=headers, data=json_data)
    # 检查响应
    if response.status_code == 200:
        dt = json.loads(response.text)
        if dt['success']:
            print('海底捞小程序签到请求成功！')
        else:
            response_data = response.json()  # 如果响应也是 JSON 格式的话
            print('签到失败：' + dt['msg'])
    else:
        print(f'海底捞小程序签到请求失败，状态码：{response.status_code}')
        print(response.text)  # 如果响应包含错误信息


if __name__ == '__main__':
    signInHDL()
