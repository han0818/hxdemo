import urllib
from bs4 import BeautifulSoup
import re
import os
import requests
import time
import random


# 抓取豆瓣小组帖子中的图片

def get_url(page):
    douban_url= "http://www.douban.com/group/haixiuzu/discussion?start="+str(int(page)*25)
    return douban_url

def parser_html(url):
    User_Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers={"User-Agent":User_Agent}
    time.sleep(1)
    html=requests.post(url,headers=headers)
    html_content=html.text
    soup=BeautifulSoup(html_content,"html.parser")

    link_list=[]
    for link_div in soup("a"):
        link_tag=link_div["href"]
        link_list.append(link_tag)
    print(link_list)
    print("本页一共%s个帖子" %len(link_list))
    print("----------------------------")
    for item_link in link_list:
        print(item_link)
        print("正在解析第%s个帖子:"  % (int(link_list.index(item_link))+1))
        time.sleep(1)
        item_data=requests.post(item_link,headers=headers).text
        item_soup=BeautifulSoup(item_data,"html.parser")
        detail_soup=item_soup.find("div",class_="topic-content")
        if detail_soup("img"):
            pic_link_list=[]
            for pic_tag in detail_soup("img",src=re.compile("group")):
                pic_link=pic_tag["src"]
                pic_link_list.append(pic_link)
            print("本帖子一共有%s张图片" %len(pic_link_list))
            for pic_link in pic_link_list:
                adds="C:\\Users\\hanxi\\Desktop\\douban"
                pic_name="douban"+pic_link[-13:]
                r=requests.get(pic_link,stream=True)
                try:
                    with open(os.path.join(adds,pic_name),"wb") as f:
                        for chunk in r.iter_content(chunk_size=5120):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    print("正在下载第%s张图片" %(int(pic_link_list.index(pic_link))+1))
                except:
                    print("图片因为名称中有不合规范的符号所以无法下载")
            print("本页帖子图片全部下载完成")
            print("------")
        else:
            print("此网页内无图片")

def main():
    page_list=range(int(input("请输入开始页码：")),int(input("请输入结束页码:")))
    for page in page_list:
        url=get_url(page)
        print(url)
        parser_html(url)


if __name__ == '__main__':
    main()








