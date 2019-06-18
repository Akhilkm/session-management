#!/usr/bin/python3.6

#title           :session.py
#description     :This program can be used for managing cookie based sessions in CGI-Python using backend MongoDB.
#author          :Kuberiter
#date            :2018/02/18
#version         :0.1
#usage           :cgi python (designed to handle web requests)
#notes           :Need to import this program in all the webpages
#python_version  :3.6.*


import hashlib
import os
import time
import http.cookies as Cookie
from settings import *


class Session:

	def __init__(self):
		"""
		Function Name : __init__
		Purpose       : Constructor function to initialize cookie data.
		Arguments     : self
		Returns       : N/A
		"""

		string_cookie = os.environ.get('HTTP_COOKIE', '')
		self.cookie = Cookie.SimpleCookie()
		self.cookie.load(string_cookie)

	
	def checkSession(self):
		"""
		Function Name : checkSession
		Purpose       : This function query the database and check the validity of session
		Arguments     : self
		Returns       : validity and session data
		"""

		if self.cookie.get('sid'):
			self.sid = self.cookie['sid'].value
			self.session_data = db_session.session.find_one({'sid': self.sid})
			if self.session_data:
				return 'valid', self.session_data
		return 'invalid', None


	def createSession(self, username, password, expires=None, cookie_path=None):
		"""
		Function Name : createSession
		Purpose       : This function will create a session.
		Arguments     : self, username, password, expiration time (seconds), cookie path
		Returns       : N/A
		"""

		self.cookie.clear()
		self.sid = hashlib.sha256((repr(time.time())+username+password).encode('utf8')).hexdigest()
		self.cookie['sid'] = self.sid
		if cookie_path:
			self.cookie['sid']['path'] = cookie_path
		db_session.session.insert_one({'sid': self.sid, 'username': username})
		self.setExpires(expires)


	def updateSession(self, data):
		"""
		Function Name : updateSession
		Purpose       : This function update the session data in the backend MongoDb
		Arguments     : self, data (data should be in json format)
		Returns       : N/A
		"""

		self.session_data = db_session.sid.find_one({'sid': self.sid})
		if not self.data:
			return 'invalid'
		return self.session_data


	def setExpires(self, expires=None):
		"""
		Function Name : setExpires
		Purpose       : This function will set expiration period for the browser cookie
		Arguments     : Expiary period in seconds
		Returns       : N/A
		"""

		if expires == '':
			db.sid.update_one({"sid": self.sid}, {"$set": {"cookie": {"expires": ''}}})
		elif isinstance(expires, int):
			db.sid.update_one({"sid": self.sid}, {"$set": {"cookie": {"expires": expires}}})
		self.cookie['sid']['expires'] = expires
