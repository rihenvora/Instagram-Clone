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

class uploadPost(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        userid=int(self.request.get("userid"))
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename
        user = users.get_current_user()
        userd=''
        user_key = ndb.Key('User',userid)
        userd = user_key.get()
        post_key = ndb.Key('Post',user.user_id())
        post = post_key.get()
        post=Post(
                post = upload.key(),
                post_name = filename,
                caption = self.request.get('caption'),
                created_by = user.email(),
                userid = str(userid) )
        post.put()

        userd.post.append(ndb.Key('Post',post.key.id()))
        userd.put()
        self.redirect('/')
