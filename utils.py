import datetime

host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'  # 这里的user_agent是网上找的


def is_number(number):
    try:
        num = int(number)
        return num
    except ValueError:
        return -1


def now_time():
    return datetime.datetime.now().strftime('%m-%d %H:%M:%S')
