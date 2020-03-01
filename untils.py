# coding:utf-8
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup
import re
import hashlib
from config import connect
import pymysql


def deal_woff():
    font = TTFont('./font_files/50065430.woff')
    font.saveXML('./font_files/50065430.xml')


def get_name_id(path):
    with open(path, 'r', encoding='utf-8')as f:
        t = f.read()
    soup = BeautifulSoup(t, 'xml')
    names = [i['name'] for i in soup.find_all('GlyphID')]
    return names


def md5_code(path):
    with open(path, 'r', encoding='utf-8')as f:
        t = f.read()
    md5_list = {}
    soup = BeautifulSoup(t, 'xml')
    ttg_list = soup.find_all('TTGlyph')
    for ttg in ttg_list:
        tar = re.findall(r'name=".*?"', str(ttg))[0]
        name = re.findall(r'name="(.*?)"', str(ttg))[0]
        result = str(ttg).replace(tar, '')
        md5_code = hashlib.md5(result.encode(encoding='utf-8')).hexdigest()
        md5_list[name] = md5_code
    return md5_list


if __name__ == '__main__':
    # deal_woff()
    # 随意配置一个 xml路径用于生产md5 和 文本对应关系入库
    xml_path = './font_files/50065430.xml'
    names = get_name_id(xml_path)[2:]
    print(names)
    md5_l = md5_code(xml_path)
    md5_sort = []
    for name in names:
        md5_sort.append(md5_l[name])
    print(names)
    print(md5_l)
    print(md5_sort)
    words = '''
     1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通昧所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站徳王光名 丽油院堂烧江社合星货型村自科快便日民营和活盦眀器烟育瑸精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来髙厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺內侧元购前幢滨处向座下県凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团 外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想岀员两推做排实分间甜度起满给热完格荐喝等其再几只现眀候样直而买于般豆量选奶圢每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晩微周值费性桌拍跟块调糕
     '''
    words = words.replace('\n', '').replace(' ', '')
    print(len(words), words, len(md5_sort))
    if len(words) == len(md5_sort):
        db = connect()
        cursor = db.cursor()
        for m, w in zip(md5_sort, words):
            sql = "INSERT INTO woff (hash_code,word) VALUES (%s,%s)"
            args = (m, w)
            cursor.execute(sql, args)
        db.close()

