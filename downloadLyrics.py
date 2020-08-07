#!/usr/bin/python
# coding=utf-8
import requests
import random
from requests.exceptions import ConnectionError
from urllib import parse
import urllib.request
import re
import os
import json
import eyed3
import time
import sys


my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

def validateTitle(title):
    rstr = r'[(\s* )(/)(\\)(\:)(\*)(\-)(\?)(\")(\<)(\>)(\|)(\')(\()(\))(~)(～)(\.)(（)(）)]'  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

#json中含有双引号会导致json.loads失败
def varifyJson(title):
    #rstr = r'(?:[^,{\[\:\(](")[^,}\]\:\)]|(\\)[^/])'
    #rstr = r'[(?:\t("))(?:(")\t)(?:(")")(?:(")\n)(?:(\\)[^/])]'
    title = re.sub(r'\"', "\'", title)
    title = re.sub(r'\'data\'', "\"data\"", title)
    title = re.sub(r'\'type\':\'', "\"type\":\"", title)
    title = re.sub(r'\',\'link\':\'', "\",\"link\":\"", title)
    title = re.sub(r'\',\'songid\':', "\",\"songid\":", title)
    title = re.sub(r',\'title\':\'', ",\"title\":\"", title)
    title = re.sub(r'\',\'author\':\'', "\",\"author\":\"", title)
    title = re.sub(r'\',\'lrc\':\'', "\",\"lrc\":\"", title)
    title = re.sub(r'\',\'url\':\'', "\",\"url\":\"", title)
    title = re.sub(r'\',\'pic\':\'', "\",\"pic\":\"", title)
    title = re.sub(r'\'},{', "\"},{", title)
    title = re.sub(r'\'}\]', "\"}]", title)
    title = re.sub(r'\'code\'', "\"code\"", title)
    title = re.sub(r'\'error\':\'\'', "\"error\":\"\"", title)
    title = re.sub(r'(?:(\\)[^/])', "`", title)
    return title



def find_links(item,Type):
    html="http://music.ifkdy.com/?name="+parse.quote(item)+"&type="+Type
    #print(html)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'UM_distinctid=173b86a737fb-0091acadac16b8-3972095d-1fa400-173b86a7380ca3; CNZZDATA1261550119=186822127-1596523892-%7C1596523892',
        'Host': 'music.ifkdy.com',
        'Origin': 'http://music.ifkdy.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': html,
        'User-Agent': random.choice(my_headers),
        'X-Requested-With': 'XMLHttpRequest',
    }
    fromdata={
        'input': item,
        'filter': 'name',
        'type': 'netease',
        'page':'1',
    }
    response =requests.post(html,data=fromdata, headers=headers)
    output=response.content.decode("unicode-escape")
    json_output=json.loads(varifyJson(output),strict=False)
    return json_output['data'][0]


def downloadlyrics(musicDict,filename):
    lrcname=filename+".lrc"
    print(lrcname)
    lrcfile=open(lrcname,"w",encoding='utf-8')
    lrcfile.write(musicDict['lrc'])
    lrcfile.close()

def main():

    filename=sys.argv[1]
    musicDict=find_links(filename,"netease")
    downloadlyrics(musicDict,filename)


if __name__ == '__main__':
    main()
