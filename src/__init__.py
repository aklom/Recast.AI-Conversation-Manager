from flask import Flask
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm, CSRFProtect
from flask_login import LoginManager
from flask_pymongo import PyMongo
from .utils import Utils
import pusher

app = Flask(__name__)
app.config['WTF_CSRF_CHECK_DEFAULT']= False
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)

login = LoginManager(app)


pusher_client = pusher.Pusher(
  app_id= Utils.PUSHER_APP_ID,
  key= Utils.PUSHER_KEY,
  secret= Utils.PUSHER_SECRET,
  cluster='eu',
  ssl=True
)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = "your-secret-app-key"
csrf = CSRFProtect(app)



from src.recast_webhooks.routes import apimod
from src.web_application.routes import base_bp
from src.web_application.inbox.routes import inbox_bp
from src.web_application.authentication.routes import auth_bp
from src.web_application.settings.routes import settings_bp
from src.web_application.groups.routes import groups_bp

app.register_blueprint(base_bp)
app.register_blueprint(inbox_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(settings_bp)

app.register_blueprint(apimod, url_prefix="/api")

