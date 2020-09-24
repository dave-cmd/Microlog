from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager, current_user
from app import db, app

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from time import time
import jwt

from flask_babel import gettext

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = gettext('Login to access page.')

admin = Admin(app)


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('people.id'))
)

class People(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(120), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), index=True)
    image = db.Column(db.String(20), nullable= False, default='default1.jpg')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    followed = db.relationship('People', secondary=followers,
                              primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=
                               (followers.c.followed_id == id),
                               backref =
                               db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    # follows/unfolows
    
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            
    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    #user and following posts
    def followed_posts(self):
        followed = Post.query.join(followers,(followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    #string representation of the object
    def __repr__(self):
        return f"{self.username}"
    
    #Hashing passwords from input 
    def set_password(self, password):
        if password == None:
            password = "";
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #sending reset password tokens
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return People.query.get(id)
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    language = db.Column(db.String(100))

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and check_password_hash(current_user.password_hash, 'master')

    
admin.add_view(MyModelView(People, db.session))
#admin.add_view(MyModelView(Post, db.session))
   
    
@login_manager.user_loader
def load_user(user_id):
    return People.query.get(int(user_id))
    

    
    
    

