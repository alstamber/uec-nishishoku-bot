# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString, Tag
from string import Template
import tweepy
import datetime
import sys


def br_handler(soup,result):
    if soup.name == 'br /':
        result.append(u'\n')


class Soup2string(object):
    def __init__(self):
        self.pre_handler = (br_handler,)

    def __call__(self,soup):
        return self.convert(soup=soup)

    def convert(self,soup):
        return u''.join(self._convert(soup=soup,result=[]))

    def _convert(self,soup,result):
        for obj in soup.contents:
            if isinstance(obj, NavigableString):
                result.append(obj.string)
            elif isinstance(obj, Tag):
                br_handler(obj,result)
                self._convert(obj,result)
            else:
                raise ValueError('not BeautifulSoup object')
        return result

soup2string = Soup2string()


def TableParser(soup,converter=lambda x:x):
    result = []
    temp = {}
    i = 0
    j = 0

    for tr in soup.findAll(name='tr',recursive=False):
        j = 0
        r = []
        for td in tr.findAll(name=['th','td'],recursive=False):
            colspan = int(td.get('colspan','1'))
            rowspan = int(td.get('rowspan','1'))
            for _ in range(colspan):
                while (i,j) in temp:
                    r.append(converter(temp[(i,j)]))
                    j += 1
                r.append(converter(td))
                for k in range(rowspan - 1):
                    temp[(i+k+1,j)] = td
                    print temp[(i+k+1,j)]
                j += 1
            else:
                while (i,j) in temp:
                    r.append(converter(temp[(i,j)]))
                    j += 1
        result.append(r)
        i += 1
    return result


def Parser(html):
    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'cellpadding':'5'})
    tabledata = TableParser(table,converter=soup2string)
    return tabledata


if __name__ == "__main__":
    f = open('key.txt')
    keyl = f.read()
    f.close();
    keysl = keyl.split('\n')

    url = "http://www009.upp.so-net.ne.jp/harmonia/nishishoku/"
    html = urllib.urlopen(url).read().decode("shift_jis").encode("utf-8")
    data = Parser(html)

    h_url = "http://www009.upp.so-net.ne.jp/harmonia/"
    h_html = urllib.urlopen(h_url).read().decode("shift_jis").encode("utf-8")
    h_data = Parser(h_html)


    auth = tweepy.OAuthHandler(linesl[0], linesl[1])
    auth.set_access_token(linesl[2], linesl[3])
    api = tweepy.API(auth_handler=auth)


    i = datetime.datetime.today().isoweekday()

    if len(sys.argv) != 2: quit()

    if i == 6 or i == 7:
        sys.exit()
    else:
        if sys.argv[1] == 'open':
            if data[1][i] != u'お休み' or data[2][i] != u'お休み':
                api.update_status(u'西食堂の開店時間になりました。今日のAセットは' + data[1][i] +
                        u'、Bセットは' + data[2][i] + u'、日替わり丼は' + data[3][i] + u'です。')
            else:
                api.update_status(u'本日西食堂はお休みです。')
        elif sys.argv[1] == 'h_open':
            if h_data[1][i] != u'お休み' or h_data[2][i] != u'お休み':
                api.update_status(u'ハルモニアの開店時間になりました。今日のスペシャルセットは' +
                        h_data[1][i] + u'、日替わりセットは' + h_data[2][i] + u'、おすすめメニューは' + h_data[3][i] + u'です。')
                api.update_status(u'ハルモニアの今日のどんぶりものは' + h_data[4][i] + u'、麺セットは' + h_data[5][i] + u'です。')
            else:
                api.update_status(u'本日ハルモニアはお休みです。')
        elif sys.argv[1] == 'lunch':
            if data[1][i] != u'お休み' or data[2][i] != u'お休み':
                api.update_status(u'お昼になりました。西食堂の今日のAセットは' + data[1][i] +
                        u'、Bセットは' + data[2][i] + u'、日替わり丼は' + data[3][i] + u'です。')
            else:
                api.update_status(u'本日西食堂はお休みです。')
            if h_data[1][i] != u'お休み' or h_data[2][i] != u'お休み':
                api.update_status(u'ハルモニアの今日のスペシャルセットは' + h_data[1][i] +
                        u'、日替わりセットは' + h_data[2][i] + u'、おすすめメニューは' + h_data[3][i] + u'です。')
                api.update_status(u'あわせてハルモニアの今日のどんぶりものは' + h_data[4][i] + u'、麺セットは' + h_data[5][i] + u'です。')
            else:
                api.update_status(u'本日ハルモニアはお休みです。')
        elif sys.argv[1] == 'dinner':
            if h_data[1][i] != u'お休み' and h_data[6][i] != u'お休み':
                api.update_status(u'ハルモニアのディナータイムになりました。今日のスペシャルセットは' +
                        h_data[1][i] + u'、日替わりセットは' + h_data[2][i] + u'、おすすめメニューは' + h_data[3][i] + u'です。')
                api.update_status(u'ハルモニアの今日のどんぶりものは' + h_data[4][i] + u'、麺セットは' +
                        h_data[5][i] + u'、サービスディナーは' + h_data[6][i] + u'です。')
            elif h_data[2][i] == u'お休み':
                api.update_status(u'本日ハルモニアはお休みです。')
            else:
                api.update_status(u'本日ハルモニアのディナータイムはお休みです。')



