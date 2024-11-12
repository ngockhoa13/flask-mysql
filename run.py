import os
from flask import Flask
from app.extensions import db, migrate, csrf, socketio  # Import các tiện ích mở rộng từ extensions.py
from app import socket_events  # Import file chứa các event handler của SocketIO
import app.routes  # Import các route

# Khởi tạo ứng dụng Flask
app = Flask(__name__, static_folder='app/assests')

# Cấu hình môi trường
if 'WEBSITE_HOSTNAME' not in os.environ:
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Liên kết các tiện ích mở rộng với app
db.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
