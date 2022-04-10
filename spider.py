# -*- codeing = utf-8 -*-
# @Time : 2022/4/9 10:30
# @Author : 张思惠
# @File : spider.py
# @Software : PyCharm
import urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3
import xlwt


findlink=re.compile(r'<a href="(.*?)".*>')
findimgsrc=re.compile(r'<img src="(.*?)"',re.S)
findtitle=re.compile(r'<a.*title="(.*)"')
findothertitle=re.compile(r'<span style="font-size:12px;">(.*?)</span>')
findrating=re.compile(r'<span class="rating_nums">(.*)</span>')
findjudge=re.compile(r'<span class="pl">(.*?)</span>',re.S)
findinq=re.compile(r'<span class="inq">(.*)</span>')
findbd=re.compile(r'<p class="pl">(.*?)</p>',re.S)

def main():
    path="https://book.douban.com/top250?start="
    datalist=getdata(path)
    print("...")
    sheetpath="豆瓣读书.xls"
    savexls(datalist,sheetpath)

def getdata(path):
    datelist=[]
    for i in range(0,10):
        html = askpath(path+str(i*25))
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all("table"):
            data=[]
            item=str(item)

            link=re.findall(findlink,item)[0]
            data.append(link)

            imgsrc=re.findall(findimgsrc,item)[0]
            data.append(imgsrc)

            title=re.findall(findtitle,item)[0]
            data.append(title)

            othertitle=re.findall(findothertitle,item)
            if len(othertitle)==0:
                data.append(" ")
            else:
                data.append(othertitle[0])


            rating=re.findall(findrating,item)[0]
            data.append(rating)

            judge = re.findall(findjudge,item)[0]
            data.append(judge.replace("\n","").replace("(","").replace(")","").replace(" ",""))

            inq=re.findall(findinq,item)
            if len(inq)!=0:
                data.append(inq[0])
            else:
                data.append("")

            bd=re.findall(findbd,item)[0]
            data.append(bd)
            datelist.append(data)

    return datelist




def askpath(path):
    head={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
    }
    req=urllib.request.Request(path,headers=head)
    res=urllib.request.urlopen(req)

    html=res.read().decode("utf-8")
    return html

def savexls(datalist,sheetpath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=True)
    sheet = workbook.add_sheet("sheet1", cell_overwrite_ok=True)
    col = ("书籍详情链接", "图片链接", "图书中文名", "图书外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        # print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    workbook.save(sheetpath)


if __name__=="__main__":
    main()