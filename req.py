import requests
import argparse
from bs4 import BeautifulSoup as bs
import datetime

# ユーザー入力からゴミの種類を取得
# デフォルトは一般
# enum:
#   一般
#   プラ
#   有害
#   ペット
#   繊維
#   ビン
#   カン
#   金属
#   紙
parser = argparse.ArgumentParser()
parser.add_argument("-target", default="一般")
kind = parser.parse_args()

# URLなどの基本情報
# 日付は実行日時から取得
url_base = 'http://kawaguchi-gomimaru.jp/calendar'
area_no = '8'
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

# 川口市のゴミ収集カレンダーをスクレイピング
def get_gomimaru(url, day, target):
    # htmlを取得してパース
    page = requests.get(url)
    soup = bs(page.content, "html.parser")

    # いい感じのところまで掘る（引っかかったら日付のみ返す）
    table = soup.find('table', {'class': 'calendarTable'})
    res = ''
    for tr in table.findAll('tr'):
        for td in tr.findAll('td'):
            searchable = False
            item = ''
            for div in td.findAll('div'):
                item += div.get_text()
                if div.get_text() == target:
                    searchable = True
            if searchable == True and int(td.get_text().replace(item, '')) >= day:
                res = td.get_text().replace(item, '')
                break
        else:
            continue
        break
    return res

url = url_base + '/' + area_no + '/' + str(year) + '/' + str(month)
result = get_gomimaru(url, day, kind.target)
# 翌月、年越し対応
if result == '':
    if month == 12:
        year = year + 1
        month = 1
    else:
        month = month + 1
    url = url_base + '/' + area_no + '/' + str(year) + '/' + str(month)
    result = get_gomimaru(url, 1, kind.target)

# 結果返却
print('次の' + str(kind.target) + 'ゴミの日は、' + str(month) + '/' + result + 'だよー！')
