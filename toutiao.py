import requests
import re
import json
from multiprocessing import Pool
from hashlib import md5
def get(offset):
    url='https://www.toutiao.com/api/search/content'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
              ,'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
             'x-requested-with': 'XMLHttpRequest'}
    payload={'aid': '24',
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': '20',
            'en_qc': '1',
            'cur_tab': '1',
            'from': 'search_tab',
            'pd': 'synthesis',
            'timestamp': '1598684551322',
            '_signature': 'i8J2oAAgEBAv3ubNXj9roIvDN7AANSYWSVGCs8qtBqF12qaC.eUBFHKbhx7tRIwE5Ph6eX42O3ux7WxFrjhA6OHihSOi.9v7IhllUhAM.K-E-MfkoppQd7wBCxClsK89YbQ'}
    response=requests.get(url,headers=headers,params=payload)
    data=response.json()   #直接用json()方法将内容解析为JSON
    if data and 'data' in data.keys():
        try:
            for item in data.get('data'):
                for i in item['display']['self_info']['image_list']:
                    print(i.get('url'))
                    content=download(i.get('url'))
                    sava_image(content)
        except KeyError:
            pass

def download(url):
    headers={'cache-control': 'no-cache','pragma': 'no-cache'}  #如果状态码为304，可以添加此headers表示强制刷新，相当于ctrl+F5
    res=requests.get(url,headers=headers)
    return res.content

def sava_image(content):
    path='image_list/{}.{}'.format(md5(content).hexdigest(),'jpeg')    #保存图片名用md5方法
    with open(path,'wb') as file:
        file.write(content)

def main(offest):
    return get(offest)

if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*20 for i in range(5)])