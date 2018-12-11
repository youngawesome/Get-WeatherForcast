
# coding: utf-8

#本代码适用于普通省份及自治区县市区天气查询，如河南-郑州-中原；不适用于直辖市县区的查询，如北京-海淀
import re
import bs4,requests,pprint

def getHTMLText(url): # 抓取中国天气网官网天气数据
    try:
        res = requests.get(url,timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return 'error'

def getWeatherList(html): # 分析天气数据，提取需要的数据
    # 通过 bs4 类获取标签 <ul class="t clearfix"> </ul> 内的天气信息 
    weatherSoup = bs4.BeautifulSoup(html,'html.parser')
    elems = weatherSoup.find('ul',attrs={'class':'t clearfix'})
    cswe = weatherSoup.find('div',attrs={'class':'crumbs fl'})

    # 初始化变量
    name1List = []
    name2List = []
    dateList = []
    weaList=[]
    temList = []
    winList =[]
    wList = []

    # 从 elems 中再进行数据提取
    name1 = cswe.select('a')# 省市
    name2 = cswe.select('span')#县区
    date = elems.select('h1') # 日期
    weat = elems.select('.wea') # 天气
    temp = elems.select('.tem') # 温度
    wind = elems.select('.win') # 风力
    
    #print(name1)
    #print(name2)
    #print(dirc)

    # 剔除多余的标签，保留需要的目标字符
    for i in name1:
        name1List.append(i.text)
    for i in name2:
        name2List.append(i.text)     
    for i in date:
        dateList.append(i.text)
    for i in weat:
        weaList.append(i.text)
    for i in temp:
        temList.append(i.text.replace('\n',''))
    for i in wind:
        winList.append(i.text.replace('\n',''))

    # 将提取出的数据保存在列表中
    for i in range(len(dateList)):
        n1 = name1List[0]+name1List[1]
        n2 = name2List[2]   #[<span>&gt;</span>, <span>&gt;</span>, <span>中原</span>]城市名所在顺序索引为2
        d1 = dateList[i]
        w1 = weaList[i]
        t1 = temList[i]
        wi1 = winList[i]
        wList.append([n1+n2,d1,w1,t1,wi1])
    return wList


def printWeatherInfo(wList): # 格式化输出数据

    tplt = '\n城市: {:9} \n日期: {:9}\n天气: {:9}\n温度: {:9} \n风力: {:10}' # 定义输出模板格式
    sessionTxt = '' # 初始化字符串，将格式化后的数据保留在其中
    for i in wList:
        print(tplt.format(i[0],i[1],i[2],i[3],i[4]))
        sessionTxt = sessionTxt + '\n' + tplt.format(i[0],i[1],i[2],i[3],i[4]) + '\n'
    return sessionTxt


def main():
    url = 'http://www.weather.com.cn/weather/101180109.shtml'#某地天气
    html = getHTMLText(url)
    weaInfoList = getWeatherList(html)
    text = printWeatherInfo(weaInfoList)

if __name__ == '__main__':
    main()

