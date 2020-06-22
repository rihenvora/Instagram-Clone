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



class SearchUser(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		# URL that will contain a login or logout link
		# and also a string to represent this
		url = ''
		url_string = ''
		welcome = ''
		userd = ''
		template_values = ''
		list = ''
		# pull the current user from the request
		user = users.get_current_user()

		# determine if we have a user logged in or not
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			#list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
			user_key = ndb.Key('User', user.user_id())
			userd = user_key.get()
			#list = User.query(User.email_address == user.email()).fetch() #Query To GetUser Email Address


		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		#list = EleVhe.query().fetch()
		# generate a map that contains everything that we need to pass to the template
		template_values = {
		'url' : url,
		'url_string' : url_string,
		'user' : user,
		'welcome' : welcome,
		'userd' : userd,
		'showList' : list
		}

		# pull the template file and ask jinja to render
		# it with the given template values
		template = JINJA_ENVIRONMENT.get_template('search.html')
		#template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = "text/html"
		if self.request.get('button') =="SEARCH":
			url = ''
			url_string = ''
			welcome = 'Welcome back'
			userd = ''
			name=''
			name1=''
			email_address=''

			template_values=''

			user = users.get_current_user()

			if user:
				url = users.create_logout_url(self.request.uri)
				url_string = 'logout'
				# user_key = ndb.Key('User', user.user_id())
				# userd = user_key.get()
				welcome = ''

				#userd = User(email_address=user.email())

				if(self.request.get('name').strip() != '' and self.request.get('name').strip() != None):
					name = self.request.get('name').strip()
				if(self.request.get('email_address').strip() != '' and self.request.get('email_address').strip() != None):
					email_address = self.request.get('email_address').strip()

				#list1= cost
				list1 = User.query().filter(User.email_address==user.email()).fetch()
				for lst in list1:
					name1=lst.name

				if( name==''and email_address ==''):
					list = ''
					welcome = 'You have not enter any search crateria'
				elif(name1 == name or email_address == user.email()):
					list = ''
					welcome ="Can Not search Self"
				else:
					list =  User.query().filter(ndb.OR(User.name == name,User.email_address == email_address)).fetch()
			else:
				url = users.create_login_url(self.request.uri)
				url_string = 'login'


			template_values={
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'showList' : list,
			}

			template = JINJA_ENVIRONMENT.get_template('search.html')
			self.response.write(template.render(template_values))
