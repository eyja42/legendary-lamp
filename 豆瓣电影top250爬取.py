'''
Author: Eyja
Date: 2022-01-22 15:36:01
LastEditTime: 2022-01-25 16:45:09
Description: 爬虫练习
'''
# -*- coding: utf-8 -*-
from os import sep
from turtle import st
from bs4 import BeautifulSoup
import re
import xlwt
import urllib
import urllib.request
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    data = getData(baseurl)
    path = "d:code/spider/豆瓣电影top250.xls"
    saveData(data,path)
    
    




findLink = re.compile(r'<a class="" href="(.*?)">')
findImg = re.compile(r'<img.*src="(.*?)"',re.S)     #让换行符包括在字符中
findTitle = re.compile(r'<span class="title">(.*?)</span>')
findStar = re.compile(r'class="rating_num" property="v:average">(.*?)</span>')
findJug = re.compile(r'<span>(\d*)人评价</span>')   #评价人数
findQuo = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#获取网页并逐一解析,返回一个二维数组
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        #获取
        html = askUrl(baseurl+str(i*25))
        #解析
        soup = BeautifulSoup(html,"html.parser")              
        for movie in soup.find_all('div',class_="item"):
            # print(movie)  #输出该电影所有内容
            src = str(movie)
            info = []
            link = re.findall(findLink,src)[0]   #豆瓣链接
            info.append(link)

            img = re.findall(findImg,src)[0]     #电影图片
            info.append(img)

            title = re.findall(findTitle,src)    #电影标题
            if len(title) == 2:
                info.append(title[0]+title[1])
            elif len(title) == 1:
                info.append(title[0])
            else:
                info.append("")

            star = re.findall(findStar,src)[0]  #电影评分
            info.append(star)

            jug = re.findall(findJug,src)[0]    #评分人数
            info.append(jug)

            quo = re.findall(findQuo,src)       #介绍文字
            if len(quo) == 1:
                info.append(quo[0])
            else:
                info.append("")

            bd = re.findall(findBd,src)[0]      #相关内容(导演等)
            bd = re.sub("<br(\s?)/(\s?)>"," ",bd)   #去掉<br/>
            bd = bd.replace('\n',' ').replace("</p>","").strip()    #去掉多余的换行,空格和</p>
            info.append(bd)

            datalist.append(info)
    return datalist





#源网页爬取工作
def askUrl(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
    }
    req = urllib.request.Request(headers = header,url=url)
    html = ''
    try:
        res = urllib.request.urlopen(req)
        html = (res.read())
    except urllib.error.URlError as e:
        return e
    return html

    


#存储数据
def saveData(data,path):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet("豆瓣电影top250")                #新建一个excel表格
    
    top = ["排名","链接","图片链接","标题","评分","评分人数","介绍","其他信息"] 
    for j in range(8):                                      #在第一行添加标题
        sheet.write(0,j,top[j])                             
    for i in range(len(data)):                              #写入数据
        sheet.write(i+1,0,"No.{}".format(i+1))  
        for j in range(len(data[i])):
            sheet.write(i+1,j+1,data[i][j])

    book.save(path)     #保存







def saveDataAsTxt(data,path):
    file = open(path,'w',encoding='utf-8')
    for movie in data:
        for item in movie:
            file.write(item)
            file.write('\n')
        file.write('\n\n\n')        #电影之间换三行




if __name__ == "__main__":
    main()
    print("爬取完毕!")




