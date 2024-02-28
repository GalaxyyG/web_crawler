#从笔趣阁网站爬取《斗罗大陆》
import requests
from bs4 import BeautifulSoup

def get_novel_chapters(): #get all novel's chapters and return all chapters' url and title
    root_url = "https://www.biqg.cc/book/937/"
    r= requests.get(root_url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')

    data = []
    for dd in soup.find_all('dd'):
        chap_title = dd.find('a')
        if not chap_title:
            continue
        data.append(("https://www.biqg.cc/%s"%chap_title['href'], chap_title.get_text()))
    return data

def get_chap_content(url): #get each chapters' content
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find('div', id='chaptercontent').get_text()

if __name__ == '__main__':
    novel_chapters = get_novel_chapters()
    novel_len = len(novel_chapters)
    idx = 0
    for chapter in novel_chapters:
        idx += 1
        print(str(idx) + "/" + str(novel_len))
        url, title = chapter
        with open('%s.txt'%title, 'w') as f: #save crawled text
            f.write(get_chap_content(url))