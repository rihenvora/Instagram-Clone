from google.appengine.ext import ndb


class Post(ndb.Model):
    post = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    post_name = ndb.StringProperty()
    created_by = ndb.StringProperty()
    userid = ndb.StringProperty()
    created_date=ndb.DateTimeProperty(auto_now_add=True)
    seen_by=ndb.StringProperty(repeated=True)
    #comment_by=ndb.StringProperty(repeated=True)
    comments=ndb.KeyProperty(kind='Comment', repeated=True)

class Comment(ndb.Model):
    #task_id = ndb.IntegerProperty()
    user_id = ndb.IntegerProperty()
    created_by=ndb.StringProperty()
    postid=ndb.StringProperty()
    comment=ndb.StringProperty()
    created_date=ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    email_address = ndb.StringProperty()
    name = ndb.StringProperty()
    userpic = ndb.BlobKeyProperty()
    userpicname = ndb.StringProperty()
    bio = ndb.StringProperty()
    fllower = ndb.StringProperty(repeated=True)
    folows = ndb.StringProperty(repeated=True)
    post = ndb.KeyProperty(kind='Post', repeated=True)
