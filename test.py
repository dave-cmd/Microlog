from flask import Flask, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, logout_user, LoginManager, current_user, login_required


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///many_to_many.db"
app.config["SECRET_KEY"] = "mysecret"

db = SQLAlchemy(app)

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

ass_table = db.Table('Association_Table',
                             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                             db.Column('channel_id', db.Integer(), db.ForeignKey('channels.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70))
    age = db.Column(db.Integer)
    subscriptions = db.relationship('Channels', secondary=ass_table, backref=db.backref('subscribers', lazy='dynamic'))
    
class Channels(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    channel_name = db.Column(db.String())
    
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, user, **kwargs):
        return redirect(url_for("login"))
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True
        
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Channels, db.session))

@app.route("/login")
def login():
    user = User.query.get(1)
    session["username"] = user.username
    login_user(user)
    return f"<center><h2>{current_user.username} is now logged in</h2></center>"

@app.route("/logout")
@login_required
def logout():
    usr = session.get("username")
    logout_user()
    return f"<center><h2>{usr} is now logged out!!</h2></center>"
    
if __name__ =="__main__":
    app.run(debug=True)
