from requests import get,post
from pyrubika.encryption import encryption
from random import randint, choice
from rabino.How import *

class rubino:
	def __init__(self, auth):
		self.auth = auth
		self.print = chup.x_coder
	def _getUrl():
		return f'https://rubino{randint(1,30)}.iranlms.ir/'
		
		
	def _request(self,inData,method):
		data = {"api_version": "0","auth": self.auth,"client": {"app_name": "Main","app_version": "3.0.2","lang_code": "fa","package": "app.rbmain.a","platform": "Android"},"data": inData,"method": method}
		while True:
			try:
				return post(rubino._getUrl(),json=data).json()
			except:
				continue
				
				
	def follow(self,followee_id,profile_id=None):
		inData = {"f_type": "Follow","followee_id": followee_id,"profile_id": profile_id}
		method = 'requestFollow'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def getPostByShareLink(self,link,profile_id=None):
		inData = {"share_string":link,"profile_id":profile_id}
		method = "getPostByShareLink"
		while True:
			try:
				return self._request(inData,method).get('data')
			except:continue
			
			
	def addPostViewCount(self,post_id,post_target_id):
		inData = {"post_id":post_id,"post_profile_id":post_target_id}
		method = "addPostViewCount"
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getStoryIds(self,target_profile_id,profile_id=None):
		inData = {"profile_id":profile_id,"target_profile_id":target_profile_id}
		method = 'getStoryIds'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def updateProfile(self,profile_id=None):
		inData = {"profile_id":profile_id,"profile_status":"Public"}
		method = 'updateProfile'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getRecentFollowingPosts(self,profile_id=None):
		inData = {"equal":False,"limit":30,"sort":"FromMax","profile_id":profile_id}
		method = 'getRecentFollowingPosts'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getProfileList(self):
		inData = {"equal":False,"limit":10,"sort":"FromMax"}
		method = 'getProfileList'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getMyProfileInfo(self,profile_id=None):
		inData = {"profile_id":profile_id}
		method = 'getMyProfileInfo'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def Like(self,post_id,target_post,prof=None):
		inData ={"action_type":"Like","post_id":post_id,"post_profile_id":target_post,"profile_id":prof}
		method = 'likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def getShareLink(self):
		inData = {"post_id":post_id,"post_profile_id":post_profile,"profile_id":prof}
		method = 'getShareLink'
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def addViewStory(self,story,ids,prof=None):
		indata = {"profile_id":prof,"story_ids":[ids],"story_profile_id":story}
		method = 'addViewStory'
		while True:
			try:
				return self._request(indata,method)
			except:continue
			
			
	def createPage(self,name,username,bio=None):
		inData = {"bio": bio,"name": name,"username": username}
		method = 'createPage'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def comment(self,text,poat_id,post_target,prof=None):
		inData = {"content": text,"post_id": poat_id,"post_profile_id": post_target,"rnd":f"{randint(100000,999999999)}" ,"profile_id":prof}
		method = 'addComment'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def UnLike(self,post_id,post_profile_id,prof=None):
		inData = {"action_type":"Unlike","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":prof}
		method ='likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def sevaePost(self,post_id,post_profile_id,prof=None):
		inData = {"action_type":"Bookmark","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":prof}
		method ='postBookmarkAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue

