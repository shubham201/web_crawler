#!/usr/bin/python
import urllib2
import os
import sys
from bs4 import BeautifulSoup
from Tkinter import *
import tkMessageBox

proxy_support = urllib2.ProxyHandler({'http':r'http://proxy_user_name:proxy_password@http_proxy:http_proxy_port'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy_support, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

class Content:
	def get_url_soup(self):
		webpage = urllib2.urlopen(self.url)
		content = webpage.read()
		webpage.close()
		soup = BeautifulSoup(content)
		return soup

	def extract(self):
		self.soup = self.get_url_soup()
		self.strng = self.soup.get_text()
	def __init__(self,url):
		self.url = url
		try:
			self.extract()
		except Exception,arg:
			tkMessageBox.showerror('Error',str(arg))
