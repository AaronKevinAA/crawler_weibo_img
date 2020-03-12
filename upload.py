import datetime
import os

import pymysql

success = 0
conn = pymysql.connect(host='175.24.5.231', port=3306, user='cj', passwd='123', db='starfollow')

cursor = conn.cursor()
date = datetime.datetime.now().strftime('%Y-%m-%d')
path = 'F:\myscrap\imgs'

for root, dirs, files in os.walk(path):
    for file in files:
        img_name = str('img/' + file)
        effect_row = cursor.execute(
            "INSERT INTO star_img(img_type,img_src,link_id_id,upload_date,upload_user_id,like_num,see_num,download_num,"
            "star_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (0, img_name, 1, date,'897227333@qq.com',0,0,0, 1))
        if effect_row == 1:
            success += 1
conn.commit()
print('成功上传' + str(success) + '条数据')
effect_row = cursor.execute("select * from star_img")
print(cursor.fetchall())
cursor.close()
conn.close()
