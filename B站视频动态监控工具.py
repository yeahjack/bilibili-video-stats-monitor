import pandas as pd
import time
import datetime
import requests
import os

print('B站视频动态实时跟踪系统')
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    '(KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36'
}
video_id = str(input('请输入视频ID(支持av或bv)： '))
if str(video_id[0:2]) == 'AV' or str(video_id[0:2]) == 'av':
    link = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + video_id[
        2:]
elif str(video_id[0:2]) == 'BV' or str(video_id[0:2]) == 'bv':
    link = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + video_id
else:
    print('输入错误')
    os._exit()
print('请注意，只支持csv文件格式！')
file_id = str(input('请输入存放文件名（如a.csv）： '))
if os.path.exists(file_id) == False:
    print('没有此文件！')
refresh_interval = int(input('请输入刷新间隔秒数（如5）： '))
print('开始监控！')
while True:
    r = requests.get(link, headers=headers)
    result = r.json()['data']
    result_selected = {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'view': result['view'],
        'danmaku': result['danmaku'],
        'reply': result['reply'],
        'favourite': result['favorite'],
        'coin': result['coin'],
        'share': result['share'],
        'like': result['like']
    }
    dataframe = pd.DataFrame(result_selected, index=[range(7)])
    dataframe.to_csv('statistics.csv',
                     index=False,
                     sep=',',
                     mode='a',
                     header=0)
    time.sleep(refresh_interval)
