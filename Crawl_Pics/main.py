import requests
from bs4 import BeautifulSoup
import os

# url = 'https://pic.netbian.com/4kmeinv/'

def get_and_parse_html(url):
    r = requests.get(url)
    print(r.status_code)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img')
    src_list = []
    for img in imgs:
        src = img['src']
        if '/uploads/' not in src:
            continue
        src = f'https://pic.netbian.com{src}'
        print(src)
        src_list.append(src)
    return src_list

def download_pics(src_list):
    for src in src_list:
        filename = os.path.basename(src)
        with open(f'/Users/gaoxingyu/Downloads/Crawl_Pics/{filename}', 'wb') as f:
            f.write(requests.get(src).content) #这种方式获得的content是二进制，所以以wb方式写入

if __name__ == '__main__':
    urls = ['https://pic.netbian.com/4kmeinv/'] +[
            f'https://pic.netbian.com/4kmeinv/index_{i}.html'
            for i in range(2, 3)] #here edit the number of pages you want to crawl
    for url in urls:
        print("###crawling: ", url)
        download_pics(get_and_parse_html(url))

