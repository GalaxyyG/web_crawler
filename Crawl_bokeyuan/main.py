import json
import requests
from bs4 import BeautifulSoup
url = 'https://www.cnblogs.com/AggSite/AggSitePostList'
headers = {
        'Content-Type': 'application/json; charset=UTF-8', #如何找到这个headers
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
} #找有效headers方法：复制所有headers，挨个删去看看哪个是有效的
def crawl_page(page_index):
        data = {"CategoryType": "SiteHome",
                "ParentCategoryId": 0,
                "CategoryId": 808,
                "PageIndex": page_index,
                "TotalPostCount": 2000,
                "ItemListActionName": "AggSitePostList"}
        r = requests.post(url, data=json.dumps(data), headers=headers) #post请求，data是json格式
        print('status code: ', r.status_code)
        return r.text

def parse_page(html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_='post-item')
        datas = []
        for article in articles:
                link = article.find('a', class_='post-item-title')
                title = link.text
                href = link['href']
                author = article.find('a', class_='post-item-author').get_text()

                icon_comment = 0
                icon_digg = 0
                icon_views = 0
                for a in article.find_all('a'):
                        if 'icon_comment' in str(a):
                                icon_comment = a.find('span').get_text()
                        if 'icon_digg' in str(a):
                                icon_digg = a.find('span').get_text()
                        if 'icon_views' in str(a):
                                icon_views = a.find('span').get_text()
                datas.append([title, href, author,icon_comment, icon_digg, icon_views])
        return datas

if __name__ == '__main__':
        html = crawl_page(0)
        datas = parse_page(html)
        import pandas as pd
        df = pd.DataFrame(datas, columns=['title', 'href', 'author', 'icon_comment', 'icon_digg', 'icon_views'])
        df.to_excel('data.xlsx', index=False)