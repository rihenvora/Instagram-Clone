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

class addComment(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        # pull the current user from the request
        user=''
        user = users.get_current_user()
        post_id=self.request.get('key')
        img=''
        post=''
        comments = []
        comments_by = []
        lt = ''
        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            post = ndb.Key('Post', int(post_id)).get()
            img = images.get_serving_url(post.post)
            comnt = reversed(post.comments)

            for cm in comnt:
                cmt = cm.get()
                usr = ndb.Key('User',int(cmt.user_id)).get()
                comments.append(cmt.comment)
                comments_by.append(usr.name)

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'post' : post,
            'img' : img,
            'post_id': post_id,
            'comments' : comments,
            'comments_by' :comments_by,
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('addComment.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') =="ADD":
            postid= self.request.get("postid")
            comment=''
            post=''
            userid=''
            user = users.get_current_user()
            list = User.query().filter(User.email_address==user.email()).fetch()
            for lst in list:
                userid=lst.key.id()
            comment_key = ndb.Key('Comment',user.user_id())
            comment = comment_key.get()
            comment = Comment(
                postid = postid,
                comment = self.request.get("comment").strip(),
                user_id = userid,
                created_by = user.email())

            comment.put()
            post = ndb.Key('Post', int(postid)).get()
            post.comments.append(comment.key)
            post.put()

        self.redirect('/addComment?key='+postid)
