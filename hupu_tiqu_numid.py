import requests
import re
from bs4 import BeautifulSoup
import codecs
import csv

#------------
#虎扑帖子提取数字id
#-----------


#构建帖子地址

hu_url="http://bbs.hupu.com/16576475.html"

#下载网页源代码

#下载网页内容
def download_url(url):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
             "Referer":"http://bbs.hupu.com/cavaliers-postdate-999",
             "cookie":"_dacevid3=a5e060cf.9a9e.bb7e.9c31.91dfbe6111d3; __gads=ID=c7effd63a9ba4fcc:T=1460126868:S=ALNI_MaMg5Em5qVxbZjPnWWiQ4Q7WpgUSg; _HUPUSSOID=f9973b38-2d4d-49c4-8d4a-f95ae83a0edb; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18259070|UnVuV2l0aERyZWFt|a321|384fa2d45173ed8be414aa45c96ae0c6|5173ed8be414aa45|UnVuV2l0aERyZWFt; ipfrom=9e65102319918645b98f0bb81856e59f%09Unknown; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1460907460,1460988371,1460989457,1461333036; CNZZDATA30020080=cnzz_eid%3D752605842-1458346817-%26ntime%3D1461330159; Hm_lvt_c001b67f70039d825f661bc9fc3a0ac4=1460907461,1460988371,1460989457,1461333037; wP_v=ef1c933f6536P3c9sbsJdP0PlPhJqKk7gK3vfP0Pgw3m95kU5ehmvH77VCbDc3dbhb; ua=20602712; lastvisit=8644%091462792519%09%2Findex.php%3F_t_t_t%3D0.46971801852286243; __dacevst=bed5081e.4b20c5bc|1462794326575; _cnzz_CV30020080=buzi_cookie%7Ca5e060cf.9a9e.bb7e.9c31.91dfbe6111d3%7C-1"}
    html=requests.post(url,headers=headers)
    html.encoding="gb2312"
    html_content=html.text
    #print(html_content)
    return html_content

#抽取数字id

def parser_url(tiezi_html):
        tiezi_soup=BeautifulSoup(tiezi_html,"html.parser")
        response_soup=tiezi_soup.find("div",id="t_main")
        num_id_list=[]
        try:
            for response_ceng in response_soup("div",class_="floor",id=re.compile("\d+"),style=False):
                id_floor=response_ceng.find("a",class_="floornum").get_text()[:-1]          #提取楼层数
                id_name=response_ceng.find("a",class_="u").get_text()                  #提取出ID
                zhuye_link=response_ceng.find("a",class_="u")["href"]+"/profile"
                yuming_num_name=response_ceng.find("a",class_="u")["href"].split("/")[-1]  #提取出后台数字或者字母id，可以避免查找时候的编码问题
                id_num_name=response_ceng.find("a",class_="u")["href"].split("/")[-1]
                if not re.match("^[0-9]*$",id_num_name):
                    zhuye_html=download_url(zhuye_link)
                    zhuye_soup=BeautifulSoup(zhuye_html,"html.parser")
                    real_num_id=zhuye_soup.find("table",class_="profile_table").find("tr").get_text().split("：")[-1]
                    print(real_num_id)
                    id_num_name=real_num_id

                num_id_list.append([id_floor,id_name,yuming_num_name,int(id_num_name),zhuye_link])   #得到list

        except:
            AttributeError,TypeError
        try:
            next_page=tiezi_soup.find("div",class_="page").find("a",class_="next")     #自动翻页
            if next_page:
                return num_id_list,"http://bbs.hupu.com/"+next_page["href"]
        except:
            AttributeError
        return num_id_list,None

def main():
    url = hu_url
    while url:
        with codecs.open("hpxzid4.csv","ab+",encoding="gbk",errors="ignore") as f:
            writer=csv.writer(f)
            tiezi_html=download_url(url)
            finals,url=parser_url(tiezi_html)
            writer.writerows(finals)
    print("全部提取成功！")

#运行
if __name__ == '__main__':
    main()
