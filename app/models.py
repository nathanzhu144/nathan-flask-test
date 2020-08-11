# Helpful links
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html    (About defining diff types of relationships)
# https://stackoverflow.com/questions/19598578/how-do-primaryjoin-and-secondaryjoin-work-for-many-to-many-relationship-in-s
# 

from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

followers = db.Table('followers', 
db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User', secondary=followers, 
                                       primaryjoin=(followers.c.follower_id == id),
                                       secondaryjoin=(followers.c.followed_id == id),
                                       backref=db.backref('followers', lazy='dynamic'), 
                                       lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return  'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # Returns a SQLAlchemy query object configud to grab the posts user is interested in from db,
    # calling all() on this query triggers its execution, with the return value a list of all its results.
    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
        
    def get_reset_password_token(self, expires_in=600):
        content = {
            'reset_password': self.id,
            'exp': time() + expires_in,
        }
        # jwt.encode() func returns token as a byte equence, but we want it as a str
        # so we decode('utf-8)
        return jwt.encode(content,
                          app.config['SECRET_KEY'],
                          algorithm='HS256'
                         ).decode('utf-8')

    # Takens a token -> Returns None if token is outdated or invalid
    #                -> Returns User object that made this token otherwise
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, 
                            app.config['SECRET_KEY'],
                            algorithm=['HS256'])['reset_password']
                            
        # exception thrown when signature is unable to be verified OR
        # time runs out to reset.
        except:
            return None
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)




# Because Flask-Login knows nothing about databases, 
# it needs the application's help in loading a user. 
# For that reason, the extension expects that the 
# application will configure a user loader function,
# that can be called to load a user given the ID. 
# This function can be added in the app/models.py 
# module:
#
# id is a string, so need to cast to string
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

