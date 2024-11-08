from sqlalchemy import create_engine, Column, String, Integer, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

# Tạo URI kết nối MySQL
DATABASE_USER = os.getenv("DB_USER", "your_mysql_username")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "your_mysql_password")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")  # Hoặc địa chỉ IP server MySQL
DATABASE_NAME = os.getenv("DB_NAME", "openu_db")

DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# Khởi tạo engine SQLAlchemy và session
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Khởi tạo base model
Base = declarative_base()

# Định nghĩa bảng User
class User(Base):
    __tablename__ = 'user'
    
    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    name = Column(String(20))
    username = Column(String(20), nullable=False)
    emailAddr = Column(String(150), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    
    blog_posts = relationship("BlogPost", back_populates="user")

# Định nghĩa bảng BlogPost
class BlogPost(Base):
    __tablename__ = 'blogPosts'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    userID = Column(String(36), ForeignKey("user.id"))
    authorname = Column(String(20))
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    imagepath = Column(String(255))
    publish = Column(Boolean, default=False)
    likes = Column(Integer, default=0)
    
    user = relationship("User", back_populates="blog_posts")
    comments = relationship("Comment", back_populates="blog_post")

# Định nghĩa bảng Comment
class Comment(Base):
    __tablename__ = 'commentsBlog'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), ForeignKey("blogPosts.title"), nullable=False)
    username = Column(String(20))
    comment = Column(Text, nullable=False)
    
    blog_post = relationship("BlogPost", back_populates="comments")

# Định nghĩa bảng Chat
class Chat(Base):
    __tablename__ = 'chat'
    
    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    userID1 = Column(String(36), ForeignKey("user.id"), nullable=False)
    userID2 = Column(String(36), ForeignKey("user.id"), nullable=False)

# Định nghĩa bảng Messages
class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(50), ForeignKey("chat.id"), unique=True, nullable=False)

# Định nghĩa bảng ChatMessage
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    sender_id = Column(Integer, nullable=False)
    sender_username = Column(String(50), nullable=False)
    room_id = Column(String(50), ForeignKey("messages.room_id"), nullable=False)

# Định nghĩa bảng Notification
class Notification(Base):
    __tablename__ = 'notification'
    
    count = Column(Integer, primary_key=True, autoincrement=True)
    myid = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    from_id = Column(String(50), nullable=False)
    ischat = Column(Boolean)

# Định nghĩa bảng LikedBlog
class LikedBlog(Base):
    __tablename__ = 'likedBlogs'
    
    title = Column(String(100), ForeignKey("blogPosts.title"), nullable=False)
    userID = Column(String(36), ForeignKey("user.id"), nullable=False)
    liked = Column(Boolean)

# Hàm khởi tạo database
def init_db():
    Base.metadata.create_all(bind=engine)
