from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_user import UserManager, UserMixin, login_required, SQLAlchemyAdapter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.py'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['USER_APP_NAME'] = 'The Realest'
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_USERNAME'] = True
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    
    
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
    