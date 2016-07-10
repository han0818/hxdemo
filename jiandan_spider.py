import urllib
from bs4 import BeautifulSoup
import re
import os
import requests
url="http://jandan.net/ooxx/page-1672#comments"
User_Agent=" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
headers={"User-Agent":User_Agent,"Referer":"http://jandan.net/ooxx/page-1639",
         "Cookie":'3318058791=12; _ga=GA1.2.277388362.1449659183; _gat=1; Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1449579985,1449659183; Hm_lpvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1449661482'}
html=requests.post(url,headers=headers)
html.encoding="utf-8"
html_content=html.text
soup=BeautifulSoup(html_content,"html.parser")
for img_tag in soup.find_all("img",src=re.compile("http://w(.*)")):
    img_link=img_tag.get("src")
    picname="%s" %img_link[-8:]
    adds="C:\\Users\\hanxi\\Desktop\\jiandan"
    def downlown(imgUrl):
        r=requests.get(imgUrl,stream=True)
        with open(os.path.join(adds,picname),"wb") as f:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
        return picname
    imgUrl=img_link
    downlown(imgUrl)










