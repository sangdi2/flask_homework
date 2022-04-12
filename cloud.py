# -*- codeing = utf-8 -*-
# @Time : 2022/4/9 9:51
# @Author : 张思惠
# @File : cloud.py
# @Software : PyCharm
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3
con =sqlite3.connect("book.db")
cur=con.cursor()
sql='select instroduction from book'
data=cur.execute(sql)
text=""
for item in data:
    text=text+item[0]
cur.close()
con.close()

cut =jieba.cut(text)
string=' '.join(cut)


img=Image.open("./static/assets/img/tree.png")
img_array=np.array(img)
wc=WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"
)
wc.generate_from_text(string)

fig=plt.figure(1)
plt.imshow(wc)
plt.axis('off')

plt.savefig("./static/assets/img/word.jpg")