from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
csrf = CSRFProtect(app)

# Configurations
if 'WEBSITE_HOSTNAME' not in os.environ:
    app.config.from_object('azureproject.development')
else:
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Khởi tạo các extension
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
