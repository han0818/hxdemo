import requests
from bs4 import BeautifulSoup
import re
import codecs
import csv
import time


#帖子链接

def confirm_url(page):
    hupu_url="http://bbs.hupu.com/vote-postdate-{}".format(page)
    return hupu_url


#下载网页内容
def download_url(url):
    time.sleep(2)
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
             "Referer":"http://bbs.hupu.com/cavaliers-postdate-999",
             "cookie":"_dacevid3=a5e060cf.9a9e.bb7e.9c31.91dfbe6111d3; __gads=ID=c7effd63a9ba4fcc:T=1460126868:S=ALNI_MaMg5Em5qVxbZjPnWWiQ4Q7WpgUSg; _HUPUSSOID=f9973b38-2d4d-49c4-8d4a-f95ae83a0edb; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18259070|UnVuV2l0aERyZWFt|a321|384fa2d45173ed8be414aa45c96ae0c6|5173ed8be414aa45|UnVuV2l0aERyZWFt; ipfrom=9e65102319918645b98f0bb81856e59f%09Unknown; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1460907460,1460988371,1460989457,1461333036; CNZZDATA30020080=cnzz_eid%3D752605842-1458346817-%26ntime%3D1461330159; Hm_lvt_c001b67f70039d825f661bc9fc3a0ac4=1460907461,1460988371,1460989457,1461333037; wP_v=ef1c933f6536P3c9sbsJdP0PlPhJqKk7gK3vfP0Pgw3m95kU5ehmvH77VCbDc3dbhb; ua=20602712; lastvisit=8644%091462792519%09%2Findex.php%3F_t_t_t%3D0.46971801852286243; __dacevst=bed5081e.4b20c5bc|1462794326575; _cnzz_CV30020080=buzi_cookie%7Ca5e060cf.9a9e.bb7e.9c31.91dfbe6111d3%7C-1"}
    #proxies = { "http": "http://119.4.252.138:3128","https": "http://119.4.252.138:1080"}
    html=requests.post(url,headers=headers)
    html.encoding="gb2312"
    html_content=html.text
    #print(html_content)
    return html_content

#解析网页
title_list=[]
def parse_url(page_html):
    soup=BeautifulSoup(page_html,"html.parser")
    tiezi_frame=soup.find("table",id="pl")
    title_list=[]
    title_frame=tiezi_frame("tr",attrs={"mid":True})
    #print(tiezi_frame)
    for titleinfo in title_frame:

        try:
            title=titleinfo.find("a",href=re.compile("/(\d){8}.html$")).get_text()
            author_id=titleinfo.find("a",class_="u").get_text()
            author_num_id=titleinfo.find("a",class_="u")["href"].split("/")[-1]
            title_date=titleinfo.find("td",class_="p_author").get_text()[-10:]
            response_num=titleinfo.find("td",class_="p_re").get_text().split("/")[0]
            read_num=titleinfo.find("td",class_="p_re").get_text().split("/")[-1]
            title_link="http://bbs.hupu.com"+titleinfo.find("a",href=re.compile("/(\d){8}.html$"))["href"]
            title_list.append([title,author_id,author_num_id,title_date,response_num,read_num,title_link])
        except:
            AttributeError
    return title_list

#解析帖子
def parser_tiezi(tiezi_link):
        tiezi_html=download_url(tiezi_link)
        tiezi_soup=BeautifulSoup(tiezi_html,"html.parser")
        response_soup=tiezi_soup.find("div",id="t_main")
        response_content_list=[]
        try:
            for response_ceng in response_soup("div",class_="floor",id=re.compile("\d+"),style=False):
                id_floor=response_ceng.find("a",class_="floornum").get_text()          #提取楼层数
                id_name=response_ceng.find("a",class_="u").get_text()                  #提取出ID
                id_num_name=response_ceng.find("a",class_="u")["href"].split("/")[-1]  #提取出后台数字或者字母id，可以避免查找时候的编码问题
                id_dengji = response_ceng.find("span",class_="f666").get_text()        #提取ID等级
                response_content_tag=response_ceng.find("td")
                if response_ceng.find("small"):                                        #去除楼层中来自客户端的提示
                    response_content_tag.small.decompose()
                response_content=response_content_tag.get_text().replace("\r"," ")     #提取出楼层内容
                response_content_list.append([id_floor,id_name,id_num_name,id_dengji,response_content])   #得到list
        except:
            AttributeError,TypeError
        try:
            next_page=tiezi_soup.find("div",class_="page").find("a",class_="next")     #自动翻页
            if next_page:
                return response_content_list,"http://bbs.hupu.com/"+next_page["href"]
        except:
            AttributeError
        return response_content_list,None


#得到所有的回复
def get_response(tiezi_list):
    all_response_list=[]
    for item_title_list in tiezi_list:
        tiezi_link=item_title_list[-1]
        print(tiezi_link)
        while tiezi_link:
            response_list,tiezi_link=parser_tiezi(tiezi_link)
            all_response_list.extend(response_list)

    return all_response_list


#得到某人的回复
def get_sb_rp(searhed_id,need_list):
    sb_rp_list=[]
    for sb_rp in need_list:
        if sb_rp[2]==searhed_id:
            sb_rp_list.append(sb_rp)
    return sb_rp_list




#写入文件
def written_file(file_name,final_list):
    with codecs.open(file_name,"ab+",encoding="gbk",errors="ignore") as f:
        writer=csv.writer(f)
        writer.writerows(final_list)

'''
#判断是否为工作组帖子：
worker_list=[]
def is_worker(give_list):
    for item in give_list:
        for worker_keyword in ["Wine&Gold","骑文趣谈","克家之言","CAVS・译","Terry Pluto碎碎念"]:
            if worker_keyword in item[0]:
                item.append(worker_keyword)
                worker_list.append(item)
    return worker_list

#判断是否为某个人的帖子：
worker_list=[]
def is_worker(be_search_id,give_list):
    for item in give_list:
        if "dashensiteen" == item[2]:
            print("发现",item[1])
            worker_list.append(item)
    return worker_list
'''

#调用
def main():

    for page in range(1,30):
        url=confirm_url(page)
        print(url)
        page_html=download_url(url)
        tiezi_list=parse_url(page_html)
        need_list=get_response(tiezi_list)
        final_list=get_sb_rp("18153755",need_list)
        written_file("hupuxiaowu.csv",final_list)

#运行
if __name__ == '__main__':
    main()