import requests
import pandas as pd
from io import StringIO
url = 'https://tianqi.2345.com/Pc/GetHistory'
headers = {
    'User-Agent': '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'''
}
def Crawl_Weather_History(year, month):
    params = {
        'areaInfo[areaId]': 60317, #this number represents different aera, 60317 is NingGuo
        'areaInfo[areaType]': 2,
        'date[year]': year,
        'date[month]': month
    }
    try:
        r = requests.get(url, headers=headers, params=params)
    except:
        print('fail to get data!')
        exit()
    data = r.json()['data']
    df = pd.read_html(StringIO(data))[0] #analyze the first table in the page
    return df

if __name__ == '__main__':
    # year, month = map(int, input('please enter year and month(split by comma ): ').split(','))
    # df = Crawl_Weather_History(year, month)
    df_list = []
    begin_year, end_year = map(int, input('please enter the begin year and end year(split by space): ').split(' '))
    for year in range(begin_year, end_year):
        print('crawling year {}'.format(year))
        for month in range(1, 13):
            df = Crawl_Weather_History(year, month)
            df_list.append(df)
    print('successfully crawled all data!')
    pd.concat(df_list).to_excel('/Users/gaoxingyu/Downloads/NingGuo_Weather.xlsx', index=False)
    print('successfully saved data!')