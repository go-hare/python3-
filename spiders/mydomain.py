import scrapy
import re
import json
import requests
import os

class www_ximalaya_com(scrapy.Spider):
    
    name = "www_ximalaya_com"
    
    start_urls = [
        "https://www.ximalaya.com/yinyue/liuxing/p1/"
    ]
    
    def parse(self, response):
        """
        该函数负责提取下一页的a链接 并提取歌曲集合的id
        拼接url 获取json数据
        :param response: 将数据返回给回调函数 parses
        :return:
        """
        #提取下一页的href 数据  '/yinyue/liuxing/p2/'
        a = response.css("li.page-next a.page-link::attr(href)").extract()[0]
        
        #拼接下一页的url
        a = "https://www.ximalaya.com" + a
        
        
        #提取歌曲集合的a链接的href 并进行正则提取id  /yinyue/460941/  这是一个 列表
        nums = response.css(" div.album-wrapper-card a::attr(href)").extract()
        # 循环列表进行正则和 拼接URL
        for val in nums:
            # 正则提取id 460941
            s = re.search("\d+",val,re.S)
            numd = s.group()
            #拼接URL
            url = "https://www.ximalaya.com/revision/play/album?albumId=" + numd
            #发起请求并移交给回调函数
            yield scrapy.Request(url,callback=self.parses)
            
            
        # 页数
        count = 2
        #循环页数
        while count <= 34:
            #拼接下一页的URL
            url = "https://www.ximalaya.com/yinyue/liuxing/p%d/" % count
            # 发去请求并移交给本身
            yield scrapy.Request(url,callback=self.parse)
            count += 1
            
            
            
    def parses(self,response):
        """
        该函用于解析 数据 提取数据 发起请求获取数据
        并将音乐保存在文件当中
        :param response:
        :return:
        """
        # 获取数据
        jsons = response.text
        
        #解析json数据
        jslod = json.loads(jsons)
        
        
        #循环数据
       
        for val in jslod["data"]["tracksAudioPlay"]:
            #获取URL
            url =  val["src"]
            #获取歌名
            name = val["trackName"]
            file_name = val["albumName"]
            lists = []
            #设置列表  将歌曲集合  URL 歌名  追加进列表
            lists.append(file_name)
            lists.append(url)
            lists.append(name)
            # #判断 URL是否为None
            if lists[1] != None:
                #打开文件
                if os.path.isdir(lists[0]) == False:
                    os.mkdir(lists[0])
                    with open("./"+ lists[0] + "/" + lists[2] + ".mp3", "wb+") as f:
                        #发起URL请求并获取内容
                        r = requests.get(lists[1])
                        #写入文件
                        f.write(r.content)
                     #生成错误日志
                    self.log("保存文件" + name)
                else:
    
                    with open("./" + lists[0] + "/" + lists[2] + ".mp3", "wb+") as f:
                        # 发起URL请求并获取内容
                        r = requests.get(lists[1])
                        # 写入文件
                        f.write(r.content)
                        # 生成错误日志
                    self.log("保存文件" + name)

       
        