#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# @Time    : 2019-03-15 18:41
# @Author  : 孔德强
# @Email   : 2533004938@qq.com
# @File    : wangyiyun.py
# @Software: PyCharm

import scrapy

class wangyiyun(scrapy.Spider):
	name = "wangyiyun"
	start_urls = [
		"https://music.163.com/#/artist?id=6731"
	]
	
	def parse(self, response):
		filname = "ms-.html"
		print(response.body)
		#用 with open 打开 起个别名f
		with open(filname,"wb") as f:
			# 将 boby 写入 文件
			f.write(response.body)
			#生成错误日志
		self.log("保存文件 %s" % filname)