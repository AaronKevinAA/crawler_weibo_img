import datetime
import os
import sys
import time
from urllib.parse import urlencode
import utils
import requests

# 微博用户id
user_id = ''
# 收集图片最小张数
img_min = 10
# 收集图片张数
img_count = 0
# 收集图片地址
imgs = {}
# 下一次收集页面id
since_id = ''
# 头请求
headers = {}
# 页面返回json数据
json = ''


# 获取微博用户id
def get_userID(url):
    global user_id
    weibo = url.find('weibo')
    if weibo != -1:
        u = url.find('/u/')
        if u != -1:
            user_id = url[u + 3:][0:10]
            return True
    return False


def get_sinceID(id):
    if len(id) == 16:
        return True
    return False


# 获得页面返回数据
def get_single_page(since_id):
    global json
    params = {
        'type': 'uid',
        'uid': user_id,
        'containerid': int('107603' + user_id),
    }
    if since_id != '':
        params['since_id'] = since_id
    url = utils.base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json = response.json()
            return True
    except requests.ConnectionError as e:
        return False


# 从返回页面中获得图片
def get_page_img():
    global img_count, since_id, json
    since_id = json['data']['cardlistInfo']['since_id']
    cards = json['data']['cards']
    for card in cards:
        if card['card_type'] == 9:
            pic_num = card['mblog']['pic_num']
            if pic_num > 9:
                pic_num = 9
            for i in range(0, pic_num):
                img_url = card['mblog']['pics'][i]['large']['url']
                img_count += 1
                imgs[card['mblog']['pics'][i]['pid']] = img_url


# 开始程序
def start():
    loop_num = 1
    global headers, json
    headers = {
        'Host': utils.host,
        'Referer': 'https://m.weibo.cn/api/container/getIndex?uid=' + user_id + '&containerid=107603' + user_id,
        'User-Agent': utils.user_agent
    }

    try:
        while img_count <= img_min:
            fail_count = 1
            print('[' + utils.now_time() + ']开始第' + str(loop_num) + '轮收集...')
            loop_num += 1
            if get_single_page(since_id):
                get_page_img()

                if img_count > img_min:
                    print('[' + utils.now_time() + ']共收集到' + str(img_count) + '张照片')
                    break
                else:
                    print('[' + utils.now_time() + ']共收集到' + str(img_count) + '张照片，系统休息1分钟')
                    time.sleep(60)
            else:
                if fail_count <= 3:
                    print('[' + utils.now_time() + ']网络较差，页面访问失败，第' + str(fail_count) + '次重试')
                    get_single_page(since_id)
                    fail_count += 1
                else:
                    print('[' + utils.now_time() + ']页面访问失败，退出程序')
    except Exception as e:
        print('[' + utils.now_time() + ']系统发生错误，退出程序')
        sys.exit()


# 结果写入txt
def into_log():
    fp = open('result.txt', 'a')
    s = '[StarFollow]\n'
    fp.write(s)
    s = '于' + utils.now_time() + '收集' + str(img_count) + '张图片(user_id=' \
        + user_id + ',next_since_id=' + str(since_id) + ')\n'
    fp.write(s)
    for pic in imgs:
        fp.write(imgs[pic] + '\n')
    fp.close()


def download_img():
    success = 0
    path = os.path.join(os.getcwd(), 'imgs')
    if not os.path.exists(path):
        os.mkdir(path)
    for img_name in imgs:
        img_dict = imgs[img_name]
        try:
            img_data = requests.get(img_dict).content
            with open(os.path.join(path, img_name + '.jpg'), 'wb') as file:
                file.write(img_data)
                file.close()
                success += 1
        except Exception as e:
            print('[' + utils.now_time() + ']网络较差，页面访问失败，下载图片失败')

    print('[' + utils.now_time() + ']成功下载' + str(success) + '张图片!')


if __name__ == '__main__':
    print('----------------------------------欢迎使用 StarFollow 1.0版-------------------------------------')
    print('[' + utils.now_time() + ']请输入你想要收集的微博主页地址：')
    print('[' + utils.now_time() + ']例如https://m.weibo.cn/u/xxxxxxxxxx... 或https://weibo.com/u/xxxxxxxxxx...')
    input_url = input()
    print('[' + utils.now_time() + ']正在检查地址格式...')
    while not get_userID(input_url):
        print('[' + utils.now_time() + ']不正确！请检查地址并重新输入：')
        input_url = input()
    print('[' + utils.now_time() + ']正确！')

    print('[' + utils.now_time() + ']是否想在上次收集结果后继续?若是则输入result.txt中保存的next_since_id，否则输入0')
    input_since = input()
    if input_since != '0':
        while not get_sinceID(input_since):
            print('[' + utils.now_time() + ']since_id格式不正确！请检查后重新输入：')
            input_since = input()
        since_id = input_since

    print('[' + utils.now_time() + ']请输入你想要收集的图片最少张数：')
    input_max = utils.is_number(input())
    while input_max == -1:
        print('[' + utils.now_time() + ']输入数字！请重新输入：')
        input_max = utils.is_number(input())
    img_min = input_max

    start()

    into_log()

    print('[' + utils.now_time() + ']收集完成，图片地址如下：')
    for img in imgs:
        print(img)

    print('[' + utils.now_time() + ']是否下载图片到本地?')
    if bool(input()):
        print('[' + utils.now_time() + ']正在下载图片中...')
        download_img()

    print('[' + utils.now_time() + ']结果已保存在result.txt，感谢你的使用!')
