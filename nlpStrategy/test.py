# coding: utf-8
from os import path  
from scipy.misc import imread  
import matplotlib.pyplot as plt  
import jieba  
import pymongo
  
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  
  
stopwords = {}  
def importStopword(filename=''):  
    global stopwords  
    f = open(filename, 'r', encoding='utf-8')  
    line = f.readline().rstrip()  
  
    while line:  
        stopwords.setdefault(line, 0)  
        stopwords[line] = 1  
        line = f.readline().rstrip()  
  
    f.close()  
  
def processChinese(text):  
    seg_generator = jieba.cut(text)  # 
  
    seg_list = [i for i in seg_generator if i not in stopwords]  
  
    seg_list = [i for i in seg_list if i != u' ']  
  
    seg_list = r' '.join(seg_list)  
  
    return seg_list  
  
importStopword(filename='./static/stopwords.txt')  
  

d = path.dirname(__file__)  
  
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['wsc']
coll=db['articles']
strings =""
for content in coll.find({"poster":"王维丹"}):
    urlx=content['content']
    strings=strings+urlx     
text= strings  

back_coloring = imread(path.join(d, "./image/love.jpg"))  
  
wc = WordCloud( font_path='./static/simhei.ttf',
                background_color="black", 
                max_words=2000,
                mask=back_coloring,  
                max_font_size=100,   
                random_state=42,  
                )  

wc.generate(text)  

image_colors = ImageColorGenerator(back_coloring)  
  
plt.figure()  

plt.imshow(wc)  
plt.axis("off")  
plt.show()  

wc.to_file(path.join(d, "名称.png"))  