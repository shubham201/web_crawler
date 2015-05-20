#!/usr/bin/python
import urllib2
import os
import sys
from bs4 import BeautifulSoup
from collections import deque
from Tkinter import *
import tkMessageBox
from extract_content import Content

proxy_support = urllib2.ProxyHandler({'http':r'http://proxy_user_name:proxy_password@http_proxy:http_proxy_port'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy_support, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)


def final_links(self,soup):
	templinks = []
	for tag in soup.find_all('a'):
		templinks.append(tag.get('href','/'))
	templinks = list(set(templinks))
	i=0
	for link in templinks:
		if(link.startswith('/')):
			templinks[i] = self.test_url + link
		elif((link.endswith(".php") or link.endswith(".htm")) and not link.startswith(self.test_url)):
			templinks[i] = self.test_url +'/'+ link
		i = i+1
	i=0
	for link in templinks:
		if(link.startswith('#')):
			templinks.pop(i)
		i = i+1
	return templinks

def get_url_soup(url):
	webpage = urllib2.urlopen(url)
	content = webpage.read()
	webpage.close()
	soup = BeautifulSoup(content)
	return soup

class Application(Frame):
	def inlist(self):
		self.config(cursor = "watch")
		self.update()
		queue = deque([])
		crawled_links = []

		test_url = self.test_url
		while(1):
			try:
				self.soup = get_url_soup(test_url)
				break
			except Exception,args:
				if tkMessageBox.askretrycancel("Error2",args):
					pass
				else:
					root.destroy()
					exit()
		links = final_links(self,self.soup)

		for link in links:
			if link.startswith(test_url):
				queue.append(link)

		queue2 = deque([])

		i=1
		for link in queue:
			print i," - ",link,'\n'
			try:
				self.Lb1.insert(END, str(i) + " - " + str(link))
				self.Lb1.see(i)
				if(i%5==0):
					if tkMessageBox.askyesno("Answer", "want to continue?"):
						pass
					else:
						break
			except Exception,args:
				if not tkMessageBox.showerror('Error',str(args)):
					root.destroy()
					exit()
			i=i+1
			try:
				self.soup = get_url_soup(link)
			except Exception,args:
				if not tkMessageBox.showerror('Error',str(args)):
					root.destroy()
					exit()
			try:
				links = final_links(self,self.soup)
			except Exception,args:
				if not tkMessageBox.showerror('Error',str(args)):
					root.destroy()
					exit()
			for link2 in links:
				if(link2 not in queue and link2 not in queue2):
					try:
						queue2.append(link2)
					except Exception,args:
						if not tkMessageBox.showerror('Error',str(args)):
							root.destroy()
							exit()
			crawled_links.append(link)
		del queue
		queue = queue2

		alllinks = []
		for link in queue:
			alllinks.append(link)
		for link in crawled_links:
			alllinks.append(link)
		alllinks = list(set(alllinks))
		print alllinks

		print "\nEND!!!\n"
		self.config(cursor = "")

	def enter(self,event):
		self.enterUrl()
	def quit(self):
		self.destroy()
		exit()
	def enterUrl(self):
		i=0
		while(1):
			try:
				self.test_url = self.E1.get()
				if(self.test_url.endswith('.com/') or self.test_url.endswith('.com')):
					pass
				else:
					raise Exception
				if(self.test_url.endswith('/')):
					self.test_url=self.test_url[:-1]
				mssg="URL is :"+self.test_url
				print mssg
				if tkMessageBox.askyesno("Message",mssg):
					try:
						self.inlist()
					except Exception,arg:
						if not tkMessageBox.showerror('Error',str(arg)):

							root.destroy()
							exit()
					return
				else:
					root.destroy()
					exit()
					break
			except Exception,arg:
				if not tkMessageBox.askretrycancel('Verify', 'Wrong Url, Re-enter or Cancel'):
					root.destroy()
					exit()
				break
		return
	def extractcontent(self):
		self.top = Toplevel(self)
		self.top.title("Extracted Contents")
		self.txt = Text(self.top)
		cont = Content(self.value)
		self.txt.insert(END, cont.strng)
		print "Text Inserted!!! is ", cont.strng[:50]
		self.txt.pack(fill=BOTH,expand=TRUE)
	def onselect(self,event):
		w = event.widget
		index = int(w.curselection()[0])
		self.value = w.get(index)
		self.value = self.value[4:]
		if tkMessageBox.askyesno('Content Extraction', 'Do you want to extract content?'):
			print "content extraction level reached :D"
			print "Extracting content of: ",self.value
			try:
				self.extractcontent()
			except Exception,args:
				if not tkMessageBox.showerror('Error',str(args)):
					root.destroy()
					exit()
		else:
			return
	def createWidgets(self):
		self.L1 = Label(self)
		self.L1["text"] = "Enter the URL to be crawled:"
		self.L1["fg"] = "red"
		self.L1.grid(row=0, column=0, padx=2,pady=2, sticky=N+S+W)

		self.E1 = Entry(self)
		self.E1["bd"] = "5"
		self.E1["width"] = "30"
		self.E1.bind('<Return>', self.enter)
		self.E1.grid(row=0, column=2, padx=2, pady=2, sticky=N+S)

		
		self.Sb1 = Scrollbar(self)
		self.Sb1.grid(row=2, column=7, rowspan=20, columnspan=1, sticky=N+S+E)

		self.Lb1 = Listbox(self, yscrollcommand = self.Sb1.set)
		self.Lb1.grid(row=2, column=0, rowspan=20, columnspan=7, sticky= N+S+W+E)
		self.Lb1.bind('<<ListboxSelect>>', self.onselect)
		self.Sb1.config(command = self.Lb1.yview)
		
		self.B = Button(self)
		self.B["text"] = "Enter"
		self.B["padx"] = 10
		self.B["command"] = self.enterUrl
		self.B.grid(row=0, column=4, padx=2, pady=2, sticky=N+S+E)
		
		self.B2 = Button(self)
		self.B2["text"] = "Quit"
		self.B2["padx"] = 10
		self.B2["command"] = self.quit
		self.B2.grid(row=0, column=6, padx=2, pady=2, sticky=N+S+E)
		
		return
		
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack(fill=BOTH,expand=TRUE)
		self.createWidgets()
		return

root = Tk()
app = Application(master=root)
app.master.title("My Web-Crawler")
app.mainloop()
