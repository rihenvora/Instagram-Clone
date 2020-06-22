import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os
import urlparse
from google.appengine.api import images

from instagramdb import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class details(webapp2.RequestHandler):
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
        followers=0
        follows=0
        post=0
        list=''
        img=''
        action=''
        muserid=''
        name=''
        bio=''
        posting=[]
        poctcmntcnt=[]
        postseen=[]
        revpost = []
        list1=[]
        postids=[]
        userid=self.request.get("key")
        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()

            welcome = 'Welcome Back'
            userd = User(email_address=user.email())
            user_key = ndb.Key('User',int(userid))
            userd = user_key.get()
            list = User.query(User.email_address == user.email()).fetch()

            for lst in list:
                muserid = lst.key.id()
                if userid in lst.folows:
                    action = 1
                else:
                    action = 0
            list1=userd
            #for lst in list1:
            name=list1.name
            bio=list1.bio
            follows = len(list1.folows)
            followers = len(list1.fllower)
            post = len(list1.post)
            if list1.userpic:
                img = images.get_serving_url(list1.userpic)
            revpost = reversed(list1.post)
            for pst in revpost:
                posts=pst.get()
                postids.append(posts.key.id())
                posting.append(images.get_serving_url(posts.post))
                poctcmntcnt.append(len(posts.comments))
                postseen.append(len(posts.seen_by))

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'folows' : follows,
            'followers' : followers,
            'post' : post,
            'list' : userd,
            'name' : name,
            'userid' : userid,
            'bio' : bio,
            'thumbnail' : img,
            'posting' : posting,
            'poctcmntcnt' : poctcmntcnt,
            'postseen' : postseen,
            'action' : action,
            'muserid' : muserid,
            'postids' : postids,
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('details.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))
