import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pymongo import MongoClient

#从数据库获取数据
client=MongoClient('localhost',27017)
db=client['quotes']
con=db['SanItem']
string=''
for item in con.find({},{'_id':0,'text':1}):
    string+=(item['text'][0])
#字符串切分
cut=jieba.cut(string)
text_data=' '.join(cut)
#制作遮罩图
image_array=np.array(Image.open('bg01.jpg'))
#设置词云
wc=WordCloud(
    background_color='white',
    mask=image_array,
    font_path='SIMLI.TTF',
    max_words=500
).generate_from_text(text_data)
#绘制图片
fig=plt.figure()
plt.imshow(wc)
plt.axis('off')
plt.savefig('词云图2.png',dpi=350)
