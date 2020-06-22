import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os
import urlparse

from instagramdb import *


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)



class friends(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/html"
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		userd = ''
		name=''
		user=''
		email_address=''

		template_values=''

		user = users.get_current_user()

		user1 = self.request.get("key")
		key1 = self.request.get("key1")
		list=[]
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			# user_key = ndb.Key('User', user.user_id())
			# userd = user_key.get()

			list1 = ndb.Key('User',int(user1)).get()
			if key1=="followers":
				for lst in list1.fllower:
					usr = ndb.Key('User',int(lst)).get()
					list.append(usr)
			else:
				for lst in list1.folows:
					usr = ndb.Key('User',int(lst)).get()
					list.append(usr)


		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'


		template_values={
		'url' : url,
		'url_string' : url_string,
		'user' : user,
		'welcome' : welcome,
		'showList' : list,
		'key1' : key1,
		}

		template = JINJA_ENVIRONMENT.get_template('friends.html')
		self.response.write(template.render(template_values))
