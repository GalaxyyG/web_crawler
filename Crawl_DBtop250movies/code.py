import requests
import pandas as pd
from bs4 import BeautifulSoup
import pprint

'''1. download all html'''
page_indexs = range(0, 250, 25) #from 0 to 250, each is 25
list(page_indexs)
def download_all_htmls():
    htmls_list = []
    for idx in page_indexs:
        url = f"https://movie.douban.com/top250?start={idx}&filter="
        #字符串前加f：以f开头表示在字符串内支持大括号内的python表达式
        print("crawling: ", url)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
            #add headers to cover or the web-agent will refuse this crawl
            html = requests.get(url, headers=headers)
            html.raise_for_status()
        except:
            print('fail to craw!')
        htmls_list.append(html.text)
    return htmls_list

htmls_list = download_all_htmls() #execute crawling

'''2. analyze html to get data'''
def parse_single_html(html_list): #parse a single html_page
    soup = BeautifulSoup(html_list,'html.parser')
    article_items = (
                soup.find('div', class_='article')
                    .find('ol', class_='grid_view')
                    .find_all('div', class_='item')
                    #each html has 25 items by analyzing page in advance
    )
    datas = []

    for article_item in article_items: #get and store 25 items data from each html
        rank = article_item.find('div', class_='pic').find('em').get_text()
        info = article_item.find('div', class_='info')
        title = info.find('div', class_='hd').find('span', class_='title').get_text()
        div_bd = info.find('div', class_='bd').find_all('p')
        detial_info = div_bd[0].get_text()
        stars = (
            info.find('div', class_='bd')
                .find('div', class_='star')
                .find_all('span')
        )
        rating_star = stars[0]['class'][0]
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()

        datas.append({
            'rank': rank,
            'title': f'《{title}》',
            'rating_star': rating_star.replace('rating', '').replace('-t', ''),
            'rating_num': rating_num,
            'comments': comments,
            'detial_info': detial_info
        })
    return datas

if __name__ == '__main__':
    #pprint.pprint(parse_single_html(htmls_list[0])) #test
    all_datas = []
    for html_list in htmls_list:
        all_datas.extend(parse_single_html(html_list))
    print('successfully crawled all data!')

    '''store data into excel'''
    df = pd.DataFrame(all_datas)
    df.to_excel('/Users/gaoxingyu/Downloads/DBTop250Movies.xlsx', index=False)
    print('successfully saved all data!')