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
    seg_generator = jieba.cut(text)  # 使用结巴分词，也可以不使用  
  
    seg_list = [i for i in seg_generator if i not in stopwords]  
  
    seg_list = [i for i in seg_list if i != u' ']  
  
    seg_list = r' '.join(seg_list)  
  
    return seg_list  
  
importStopword(filename='./static/stopwords.txt')  
  
  
# 获取当前文件路径  
# __file__ 为当前文件, 在ide中运行此行会报错,可改为  
# d = path.dirname('.')  
d = path.dirname(__file__)  
  
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['wsc']
coll=db['articles']
strings =""
for content in coll.find({"poster":"王维丹"}):
    urlx=content['content']
    strings=strings+urlx     
text= strings  
#text = open(path.join(d, 'love.txt'),encoding ='utf-8').read()  
  
#如果是中文  
#text = processChinese(text)#中文不好分词，使用Jieba分词进行  
  
# read the mask / color image  
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010  
# 设置背景图片  
back_coloring = imread(path.join(d, "./image/love.jpg"))  
  
wc = WordCloud( font_path='./static/simhei.ttf',#设置字体  
                background_color="black", #背景颜色  
                max_words=2000,# 词云显示的最大词数  
                mask=back_coloring,#设置背景图片  
                max_font_size=100, #字体最大值  
                random_state=42,  
                )  
# 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数  
wc.generate(text)  
# wc.generate_from_frequencies(txt_freq)  
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]  
# 从背景图片生成颜色值  
image_colors = ImageColorGenerator(back_coloring)  
  
plt.figure()  
# 以下代码显示图片  
plt.imshow(wc)  
plt.axis("off")  
plt.show()  
# 绘制词云  
  
# 保存图片  
wc.to_file(path.join(d, "名称.png"))  