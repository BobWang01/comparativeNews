import re
import _thread
import requests
from bs4 import BeautifulSoup
from mutool.annotation import *
from mutool.validate import *
from mutool.date import *

date = None

# 构造请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
}

reqNum = 0
# 实例一个请求会话
req = requests.session()
# 设置请求头
req.headers=headers


# 所有的请求由本方法发送

@retry(10)
@log()
def loadPage(url,encoding="utf-8") -> str:
    global reqNum
    global req
    reqNum += 1
    # 请求模块执行POST请求,response为返回对象
    response = req.get(url, timeout=10)
    # 从请求对象中拿到相应内容解码成utf-8 格式
    html = response.content.decode(encoding)
    return html

@log()
def huanqiu():
    url = "https://www.huanqiu.com"
    html = loadPage(url)
    soup = BeautifulSoup(html,"html.parser")
    rightSecTag = soup.find('div',attrs={'class':'rightSec'})
    if rightSecTag:
        aTags = rightSecTag.find_all("a")
        for atag in aTags:
            try:
                scr = atag['href']
                title = atag.get_text()
                html = loadPage(scr)
                dSoup = BeautifulSoup(html,"html.parser")
                articleTag = dSoup.find("article")
                if articleTag:
                    article = codingList([articleTag.get_text()])[0]
                    title = validateFileTitle(title)
                    print("环球网",title)
                    if article:
                        with open("所有/环球网/{}/{}.txt".format(date,title),mode="w") as f:
                            f.write(article)
                            f.close()
            except Exception as e:
                print(e)
@log()
def xinhua():
    url = "http://m.xinhuanet.com/"
    html = loadPage(url).replace('  ',"")
    soup = BeautifulSoup(html,"html.parser")
    titleTags = soup.find_all('h3',attrs={'class':'thumb-tit'})
    for titleTag in titleTags[0:(20 if len(titleTags)>20 else len(titleTags))]:
        try:
            aTag = titleTag.find("a")
            if aTag:
                href = aTag['href']
                title = aTag.get_text()
                html = loadPage(href)
                if 'class="tadd"' in html:
                    html = html.split('<div class="tadd">')[0] + "</div>"
                soup = BeautifulSoup(html,"html.parser")
                detailTag = soup.find("div",attrs={'id':'p-detail'})
                if detailTag:
                    print("新华网",title)
                    title = validateFileTitle(title)
                    detail = codingList([detailTag.get_text()])[0]
                    with open("所有/新华网/{}/{}.txt".format(date,title), mode="w") as f:
                        f.write(detail.replace("\n\n\n","").strip("\n"))
                        f.close()
        except Exception as e:
            print(e)
@log()
def renmin():
    url = "http://finance.people.com.cn/"
    html = loadPage(url,encoding="gbk")
    soup = BeautifulSoup(html,"html.parser")
    titleTags = soup.find('h1')
    if titleTags:
        atags = titleTags.find_all("a")
        for atag in atags:
            href = ("http://finance.people.com.cn/"+atag['href']) if "http" not in atag['href'] else atag['href']
            title =  atag.get_text()
            html = loadPage(href,encoding="gbk")
            soup = BeautifulSoup(html, "html.parser")
            detailTag = soup.find("div", attrs={'class': 'box_con'})
            if detailTag:
                print("人民网", title)
                title = validateFileTitle(title)
                detail = codingList([detailTag.get_text()])[0]
                with open("所有/人民网/{}/{}.txt".format(date, title), mode="w") as f:
                    f.write(detail.replace("\n\n\n", "").strip("\n"))
                    f.close()
    frTags = soup.find('div',attrs={'class':'box_hot'})
    if frTags:
        atags = frTags.find_all("a")
        try:
            for atag in atags:
                href = ("http://finance.people.com.cn:" + atag['href']) if "http" not in atag['href'] else atag['href']
                title = atag.get_text()
                html = loadPage(href,encoding="gbk")
                soup = BeautifulSoup(html, "html.parser")
                detailTag = soup.find("div", attrs={'class': 'box_con'})
                if detailTag:
                    print("人民网", title)
                    title = validateFileTitle(title)
                    detail = codingList([detailTag.get_text()])[0]
                    with open("所有/人民网/{}/{}.txt".format(date, title), mode="w") as f:
                        f.write(detail.replace("\n\n\n", "").strip("\n"))
                        f.close()
        except Exception as e:
            print(e)
@log()
def niuyue():
    url = "https://www.nytimes.com"
    html = loadPage(url)
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find('div',attrs={'class':'css-16ugw5f'})
    if tag:
        atags = tag.find_all('a')
        for aTag in atags:
            try:
                href = "https://www.nytimes.com"+aTag['href']
                title = aTag.get_text().strip()
                if "comments" in title:
                    continue

                html = loadPage(href)

                soup = BeautifulSoup(html, "html.parser")
                detailTag = soup.find("section",attrs={'name':'articleBody'})
                if detailTag:
                    print("纽约时报", title[:37] + "***")
                    ptitle = title
                    title = validateFileTitle(title[:37] + "***")
                    detail = ""
                    for pTag in detailTag.find_all("p"):
                        detail += (pTag.get_text()+"\n")
                    detail = codingList([detail])[0]
                    with open("所有/纽约时报/{}/{}.txt".format(date, title), mode="w") as f:
                        f.write(ptitle + "\n" + detail.replace("\n\n\n", "").strip("\n"))
                        f.close()
            except Exception as e:
                print(e)
@log()
def bbc():
    url = "https://www.bbc.com"
    html = loadPage(url).replace('module module--news   module--collapse-images',"news111")
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find('section',attrs={'class':'module--promo'})
    if tag:
        atags = tag.find_all('a',attrs = {'class':'block-link__overlay-link'})
        for aTag in atags:
            try:
                href = "https://www.bbc.com"+aTag['href'] if "http" not in aTag['href'] else aTag['href']
                title = aTag.get_text().strip()
                html = loadPage(href)

                dsoup = BeautifulSoup(html, "html.parser")
                detailTag = dsoup.find("article")
                if detailTag:
                    print("BBC", title[:37] + "***")
                    ptitle = title
                    title = validateFileTitle(title[:37] + "***")
                    detail = ""
                    for pTag in detailTag.find_all("p"):
                        detail += (pTag.get_text()+"\n")
                    detail = codingList([detail])[0]
                    with open("所有/BBC/{}/{}.txt".format(date, title), mode="w") as f:
                        f.write(ptitle + "\n" + detail.replace("\n\n\n", "").strip("\n"))
                        f.close()
            except Exception as e:
                print(e)
    tag = soup.find('div',attrs={'class':'content--block--modules'})
    if tag:
        atags = tag.find_all('a',attrs = {'class':'media__link'})
        for aTag in atags:
            try:
                href = "https://www.bbc.com"+aTag['href'] if "http" not in aTag['href'] else aTag['href']
                title = aTag.get_text().strip()
                html = loadPage(href)

                soup = BeautifulSoup(html, "html.parser")
                detailTag = soup.find("article")
                if detailTag:
                    print("BBC", title[:37] + "***")
                    ptitle = title
                    title = validateFileTitle(title[:37] + "***")
                    detail = ""
                    for pTag in detailTag.find_all("p"):
                        detail += (pTag.get_text()+"\n")
                    detail = codingList([detail])[0]
                    with open("所有/BBC/{}/{}.txt".format(date, title), mode="w") as f:
                        f.write(ptitle + "\n" + detail.replace("\n\n\n", "").strip("\n"))
                        f.close()
            except Exception as e:
                print(e)
@log()
def huashengdun():
    url = "https://www.washingtonpost.com"
    html = loadPage(url)
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find('div',attrs={'class':'no-skin'})
    if tag:
        atags = tag.find_all('a',attrs={'data-pb-field':'headlines.basic'})
        for aTag in atags:
            try:
                href = aTag['href']
                title = aTag.get_text().strip()
                if "comments" in title:
                    continue
                html = loadPage(href)
                soup = BeautifulSoup(html, "html.parser")
                detailTag = soup.find("div",attrs={'class':'article-body'})
                if detailTag:
                    print("华盛顿邮报", title[:37] + "***")
                    ptitle = title
                    title = validateFileTitle(title[:37] + "***")
                    detail = ""
                    for pTag in detailTag.find_all("p"):
                        detail += (pTag.get_text()+"\n")
                    detail = codingList([detail])[0]
                    with open("所有/华盛顿邮报/{}/{}.txt".format(date, title), mode="w") as f:
                        f.write(ptitle + "\n" + detail.replace("\n\n\n", "").strip("\n"))
                        f.close()
            except Exception as e:
                print(e)

if __name__ == '__main__':
    while 1:
        date = timestampToDate(format="%Y-%m-%d")
        validatePath("所有/环球网/{}".format(date))
        _thread.start_new_thread(huanqiu,())
        validatePath("所有/新华网/{}".format(date))
        _thread.start_new_thread(xinhua,())
        validatePath("所有/人民网/{}".format(date))
        _thread.start_new_thread(renmin,())
        validatePath("所有/纽约时报/{}".format(date))
        _thread.start_new_thread(niuyue,())
        validatePath("所有/BBC/{}".format(date))
        _thread.start_new_thread(bbc,())
        validatePath("所有/华盛顿邮报/{}".format(date))
        _thread.start_new_thread(huashengdun,())

        time.sleep(24*60*60)