from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

# Khởi tạo các tiện ích mở rộng mà không liên kết với app
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
socketio = SocketIO(async_mode='eventlet')