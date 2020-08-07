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


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)



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
    #print(varifyJson(output))
    json_output=json.loads(varifyJson(output),strict=False)

    return json_output['data'][0]


def getAlbum_And_pubDate_And_songImg(songid):
    headers={
        'User-Agent': random.choice(my_headers),
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'}
    response=requests.get('http://music.163.com/song?id='+str(songid),headers=headers)
# 0,album_name; 1,img; 2, pubDate
    pattern = re.compile('meta property="og:description" content="歌曲名《(?:.*?)》.*?收录于《(.*?)》专辑中(?:.|\n)*?images.*?\["(.*?)"\](?:.|\n)*?pubDate.*?": "(.*?)"', re.S)
# 0,img; 1, album_name; 2, pubDate
    #pattern = re.compile('images.*?\["(.*?)"\](?:.|\n)*?收录于《(.*?)》(?:.|\n)*?pubDate.*?": "(.*?)"', re.S)
    result= re.findall(pattern, str(response.text))[0]
    return list(result)

# https://eyed3.readthedocs.io/en/latest/
# type,link,songid,title,author,lrc,url,pic
def downloadMusic_WithMetaData(musicDict):

    filename=validateTitle(musicDict['title']+'_'+musicDict['author'])+'.mp3'
    imagename=validateTitle(musicDict['title'])+'.jpg'
    lrcname=validateTitle(musicDict['title'])+".lrc"

    if not os.path.exists(filename):
        os.system("wget \"" + musicDict['url']+"\" -O" +filename)
    else:
        print(filename+"文件已存在，跳过")
        raise Exception("File already exists!")

    if get_FileSize(filename)<0.5 :
        os.system("echo "+filename+" >> notFoundList")
        os.system("rm "+filename)
        raise Exception("Invalid File Size!")

    ExtraInfo=getAlbum_And_pubDate_And_songImg(musicDict['songid'])
    lrcfile=open(lrcname,"w",encoding='utf-8')
    lrcfile.write(musicDict['lrc'])
    lrcfile.close()
    os.system("wget " + ExtraInfo[1]+' -O ' +imagename)
    os.system("eyeD3 --add-image "+imagename+":MEDIA "+filename)
    os.system("eyeD3 --add-lyrics "+lrcname+" "+filename)

    print(musicDict['title'])
    audiofile = eyed3.load(filename)
    audiofile.tag.artist = musicDict['author']
    audiofile.tag.album = ExtraInfo[0]
    audiofile.tag.album_artist = musicDict['author']
    audiofile.tag.title = musicDict['title']
    audiofile.tag.release_date= ExtraInfo[2]
    audiofile.tag.track_num = int(musicDict['songid'])
    audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION,encoding='utf-8')
    os.system("rm "+imagename)
    os.system("rm "+lrcname)



if __name__ == '__main__':

    f = open("lists.txt","r",encoding='utf-8')   #设置文件对象
    fileContent=f.read().splitlines() #将txt文件的所有内容读入到字符串str中
    f.close()
    for item in fileContent:
        try:
            singleMusic=find_links(item,"netease")
        except:
            time.sleep(2)
            singleMusic=find_links(item,"netease")
        try:
            downloadMusic_WithMetaData(singleMusic)
        except Exception:
            continue


    #os.system("rm *.lrc;rm *.jpg")
    os.system("rm downloadmp3.py")
            #try:
            #    downloadMusic_WithMetaData(find_links(item,"qq")[0])
            #except Exception:
            #    try:
            #        downloadMusic_WithMetaData(find_links(item,"kugou")[0])
            #    except Exception:
            #        try:
            #            downloadMusic_WithMetaData(find_links(item,"kuwo")[0])
            #        except Exception:
            #            try:
            #                downloadMusic_WithMetaData(find_links(item,"xiami")[0])
            #            except Exception:
            #                continue
