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


class uploadUserInfo(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # self.response.headers['Content-Type']='text/html'
        # action = self.request.get('button')
        #
        # if action == 'SAVE':
        userid=int(self.request.get("userid"))
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename
        user = users.get_current_user()
        userd=''
        user_key = ndb.Key('User',userid)
        userd = user_key.get()
        userd.name=self.request.get('name')
        userd.bio = self.request.get('bio')
        userd.userpicname=filename
        userd.userpic=upload.key()
        userd.put()
        self.redirect('/')
