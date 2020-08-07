# netEase_List_download

# `downloadmp3.py`

 下载网易云歌单，个人迁移网易云到本地用。

## 环境

`python3.6.9` ，请确保`requests、urllib、eyed3`模块已安装

## 工作流：

1. 根据歌单ID先[导出歌单文本](https://yyrcd.com/2018/11/14/n2s-zh/)，保存于`lists.txt`；

2.  运行 `python3  downloadmp3.py`，开始下载；

## 说明

1. 本脚本借助[疯狂音乐搜索](http://music.ifkdy.com/?name=mc6%20-%20Leaf&type=netease)提供的服务进行下载；

2. 无法下载高品质（无损）音乐，网易云中现已无法播放的音乐只有部分可以下载（解决方法：加入其他站点资源搜索）；

3. 利用Python的`EyeD3`库将歌曲的专辑封面、歌词、作者等**元数据**一并写入`mp3`文件；

4. 极少数情况会运行出错，大概率是在`json.loads`处（原因是请求到的数据中的某个地方出现了期望外的**蛋疼的双引号**）；

5. 下载失败的歌曲会写入`notFoundList`里。


# `flacToMp3.sh`

将目录下（多层）的所有`.flac`无损音乐通过`ffmpeg`转为较高质量的MP3格式。
请先安装ffmpeg:
```bash
sudo apt-get install ffmpeg libavcodec-extra57  # Ubuntu 18.04
```

# `addlyricsToMp3.sh`

将目录下（单层）的所有`.mp3`音乐加上由[疯狂音乐搜索](http://music.ifkdy.com/?name=mc6%20-%20Leaf&type=netease)得到的歌词。  
需要用到`downloadLyrics.py`脚本，请将两者放在同一目录下。
