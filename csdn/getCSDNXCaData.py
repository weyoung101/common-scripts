import base64
import hashlib
import hmac
import random

default_x_ca_key = "203803574"
default_app_secret = "9znpamsyl2c7cdrr9sas0le9vbc3r6ba"


def get_x_ca_signature(content, secret):
    secret_key = bytes(secret, 'utf-8')
    content_bytes = bytes(content, 'utf-8')
    hmac_obj = hmac.new(secret_key, msg=content_bytes, digestmod=hashlib.sha256)
    hmac_digest = hmac_obj.digest()
    base64_encoded = base64.b64encode(hmac_digest).decode('utf-8')
    return base64_encoded


def get_signature_part_string(method, x_ca_nonce, url):
    if method == "get":
        # return前面加f是因为字符串中有变量
        return f"GET\napplication/json, text/plain, */*\n\n\n\nx-ca-key:{default_x_ca_key}\nx-ca-nonce:{x_ca_nonce}\n{url}"
    else:
        return f"POST\n*/*\n\napplication/json\n\nx-ca-key:{default_x_ca_key}\nx-ca-nonce:{x_ca_nonce}\n{url}"


def get_x_ca_nonce():
    nonce_template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    result = []

    for char in nonce_template:
        if char != 'x' and char != 'y':
            result.append(char)
        else:
            result.append(deal_xy(char))
    return ''.join(result)


def deal_xy(e):
    n = int(16 * random.random())
    if e == 'x':
        t = n | 8
    else:
        t = 3 & n | 8
    return format(t, 'x')


# 获取 x-ca 请求头的数据
# 例如： {'x-ca-key': '203803574', 'x-ca-nonce': 'ccddc9cc-e9ea-4fc8-9bba-add9ef8cffeb', 'x-ca-signature': 'QvCb8sMu1NuUSpUIy4m3u4rHvbj1WUum45yF8NeSFQ8='}
def get_all_x_ca_data(method, url):
    x_ca_nonce = get_x_ca_nonce()
    x_ca_headers = {}
    x_ca_headers['x-ca-key'] = default_x_ca_key
    x_ca_headers['x-ca-nonce'] = x_ca_nonce

    content = get_signature_part_string(method, x_ca_nonce, url)

    x_ca_headers['x-ca-signature'] = get_x_ca_signature(content, default_app_secret)
    return x_ca_headers


# 调试方法
if __name__ == '__main__':
    # print(get_all_x_ca_data("post", "/points/api/task/activity/signin/addSignin"))
    print(get_x_ca_signature(
        get_signature_part_string("post", 'bacf8e88-9ff8-4dfb-8ecd-deabeffefebf',
                                  '/points/api/task/activity/signin/addSignin'),
        '9znpamsyl2c7cdrr9sas0le9vbc3r6ba'))
