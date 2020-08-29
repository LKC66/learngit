import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool

def main(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        save_data(item)
        # print(item)

def get_one_page(url):   #添加user-agent referer cookie 伪装浏览器
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
             'Referer': 'https://maoyan.com/board/4?offset=10',
              'Cookie': '__mta=251567801.1598622651876.1598679503282.1598679991053.14; uuid_n_v=v1; uuid=3AA12800E93511EA9B40998457BCB4EB91E6AFBA715646C99519079466D35CB2; mojo-uuid=4310b70c19e1ab152aa07eed701f8b0f; _lxsdk_cuid=1743555d493c8-05e9e80894ca-f7b1332-144000-1743555d494c8; _lxsdk=3AA12800E93511EA9B40998457BCB4EB91E6AFBA715646C99519079466D35CB2; _csrf=9976516c111f3f938d2f905981d7d2d03ee78646ff68a7f84a2158e85bed3dc3; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1598622631,1598663451; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=251567801.1598622651876.1598623030394.1598663454488.7; mojo-session-id={"id":"5d7914950326baead83276968d35d824","time":1598679500266}; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1598679991; _lxsdk_s=17438b9464c-a9-afa-3f8%7C%7C9'}
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            html=response.text
            return html
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?class="name".*?data-val.*?>(.*?)</a>.*?star">(.*?)</p>'
                       r'.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(\d+)</i></p>',re.S)
    results=re.findall(pattern,html)
    for result in results:
        yield {'rank':result[0],
                'film_name':result[1],
                'actor':result[2].strip()[3:],
                'time':result[3][5:],
                'score':result[4]+result[5]}

def save_data(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__=='__main__':
    pool=Pool()  #添加多线程 进程池
    pool.map(main,[i*10 for i in range(10)])

