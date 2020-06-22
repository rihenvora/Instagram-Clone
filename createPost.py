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
    autoescape=True
)

class createPost(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        # pull the current user from the request
        user = users.get_current_user()
        userd=''
        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            welcome = 'Hellow'
            list = User.query(User.email_address == user.email()).fetch()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'list' : list,
            'link' : blobstore.create_upload_url('/uploadPost'),
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('createPost.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))
