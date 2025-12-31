from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('MYSQL_URL')[8:]
db_url = 'mysql+pymysql://' + url

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


login_manager.login_view = 'login'
# login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


login_manager.init_app(app)
db.init_app(app)
bcrypt.init_app(app)


from APP import routes