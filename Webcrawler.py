#!/usr/bin/env python
#-*-coding:utf-8-*-

' a test module '

__author__ = 'Jrwong'

import urllib2
import re
import os
from time import ctime,sleep
from HTMLParser import HTMLParser

class Person(object):
	def __init__(self):
		pass

	@property
	def sex(self):
	    return self._sex
	@sex.setter
	def sex(self, value):
	    self._sex = value
	
	@property
	def agelevel(self):
	    return self._agelevel
	@agelevel.setter
	def agelevel(self, value):
	    self._agelevel = value
	
	@property
	def message(self):
	    return self._message
	@message.setter
	def message(self, value):
	    self._message = value
	
	@property
	def updatetime(self):
	    return self._updatetime
	@updatetime.setter
	def updatetime(self, value):
	    self._updatetime = value
	
	@property
	def address(self):
	    return self._address
	@address.setter
	def address(self, value):
	    self._address = value
	
	@property
	def sex(self):
	    return self._sex
	@sex.setter
	def sex(self, value):
	    self._sex = value


class HTMLDom(object):
	"""docstring for HTMLDom"""
	def __init__(self):
		self.tags = []
		pass

	def blank(self, level):
		blanks = ''
		for i in range(0, level):
			blanks = blanks + '|---'
		return blanks
		pass

	def __str__(self):		
		def descriptionGenerator(tag, level):
			string = self.blank(level) + tag.__str__()
			if len(tag.children) > 0:
				for t in tag.children:
					string = string + descriptionGenerator(t, level + 1)
			return string

		desc = ''

		for tag in self.tags:
			desc = desc + descriptionGenerator(tag, 0)

		return desc

	def getTagsByName(self, name):
		if not isinstance(name, str):
			raise TypeError

		def filterTagsByName(tags, name):
			ts = filter(lambda x:x.name == name, tags)
			for tag in tags:
				if len(tag.children) > 0:
					ts.extend(filterTagsByName(tag.children, name))
			return ts

		return filterTagsByName(self.tags, name)


	def getTagByAttribute(self, attribute, value):
		if not isinstance(attribute, str) or not isinstance(value, str):
			raise TypeError
		def filterTagsByAttr(tag, attr, v):
			ts = []
			for key in tag.attrs:
				if key == attr and v == tag.attrs[key]:
					ts.append(tag)
			if len(tag.children) > 0:
				for t in tag.children:
					ts.extend(filterTagsByAttr(t, attr, v))
			return ts
		targetTags = []
		for tag in self.tags:
			targetTags.extend(filterTagsByAttr(tag, attribute, value))
		return targetTags
	
	def getTagByID(self, ID):
		if not isinstance(ID, str):
			raise TypeError
		tags = self.getTagByAttribute('id', ID)
		if len(tags) > 0:
			return tags[0]
		else:
			return None

	
#HtmlTag
class HTMLTag(object):
	"""docstring for HtmlTag"""
	def __init__(self, tagName, attrs):
		self.parent = None
		self.children = []
		self.name = tagName
		self.html = None
		self.attrs = {}
		for i in range(0, len(attrs)):
			self.attrs[attrs[i][0]] = attrs[i][1]

	def __str__(self):
		return '<tagName: %s, html: %s, attrs: %s>\n' % (self.name, self.html, self.attrs)

	__repr__ = __str__



#MyHtmlParser
class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []
		self.currentTag = None
		self.dom = HTMLDom()
		

	def handle_starttag(self, tag, attrs):
		nowTag = HTMLTag(tag, attrs)

		nowTag.parent = self.currentTag
		self.currentTag = nowTag

		if nowTag.parent != None:
			nowTag.parent.children.append(nowTag)
		else:
			self.dom.tags.append(nowTag)
		pass


	def handle_endtag(self, tag):
		self.currentTag = self.currentTag.parent
		pass

	def hanle_startendtag(self, tag, attrs):
		nowTag = HTMLTag(tag, attrs)
		nowTag.parent = self.currentTag

		if nowTag.parent != None:
			nowTag.parent.children.append(nowTag)
		else:
			self.dom.tags.append(nowTag)

	def handle_data(self, data):
		if self.currentTag != None:
			self.currentTag.html = data.strip()


waitingList = []
viewedList = []

# /Users/jmacmini/Desktop/net   文件夹
def writeToFile(url, result):
	if not isinstance(result, str):
		raise TypeError
	reg = r'[^:/?]+'
	newurl = ''.join(re.findall(reg, url))
	print newurl
	path = '/Users/jmacmini/Desktop/net/' + newurl	

	isPic = url.endswith('.png') or url.endswith('.jpg')

	if not os.path.exists(path):
		os.mkdir(path)
		if isPic:
			filepath = path + '/pic.jpg'
		else:
			filepath = path + '/html.html'

		fileobj = None
		try:	
			if isPic:
				fileobj = open(filepath, 'wb')
			else:
				fileobj = open(filepath, 'w')
			
			fileobj.write(result)
		except Exception, e:
			print '---------------'+e.__str__()
		finally:
			if fileobj != None:
				fileobj.close()
			

def findLinksInString(string):
	res = r'https:\/\/.*?[^\ \"\']+'
	mlist = re.findall(res, string)
	return mlist

def requestLink(link):
	print '\n\nrequesting: ' + link
	req = urllib2.Request(link)
	req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
	resp = urllib2.urlopen(req, timeout = 10)
	ret = resp.read()
	return ret

waitingList.append('http://news.163.com')
# print requestLink(waitingList[0])

count = 0
while True:
# while False:
	# sleep(1)
	count = count + 1
	if len(waitingList) > 0:
		link = waitingList.pop(0)
		if link.endswith('.js') or link.endswith('.css'):
			continue
		if link not in viewedList:
			viewedList.append(link)
			try:
				result = requestLink(link)
				print type(result)
				writeToFile(link, result)
				links = findLinksInString(result)
				print '------------------------------------------------------------------------' + str(count)
				print links
				if links != None and len(links) > 0:
					waitingList.extend(links)
			except Exception, e:
				pass
			finally:
				pass
			

# res = r'https?:\/\/.*?[^\ \"\']+'
# link = 'href=\"http://movie.douban.com/feed/review/movie\"'
# print re.findall(res, link)

# <div class="post man" data-inset="true">
# 	<div class="post-header">
# 		<div class="icon">
# 			<img src="/images/icon-man.png" alt="男性" />
# 		</div>
# 		<div class="text">
# 			<a href="/view/12664590/">ゆー</a>
# 			<br />20代 / 東京
# 		</div>
# 	</div>
# 	<div class="post-lineid">
# 		<img src="/images/icon-lineid.png" alt="LINE ID" class="lineid"/>today.62
# 	</div>
# 	<div class="post-content"><p class="message">いちゃいちゃしたい(´・・`)
# 		会える人ー。</p>
# 	</div>
# 	<div class="post-footer">
# 		<div class="updated">07-05 16:52</div>
# 	</div>
# </div>

