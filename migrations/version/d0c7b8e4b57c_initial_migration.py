from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_postgresql_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Tạo bảng user
    op.create_table('user',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=20)),
        sa.Column('username', sa.String(length=20), nullable=False),
        sa.Column('emailAddr', sa.String(length=150), unique=True, nullable=False),
        sa.Column('password', sa.String(length=60), nullable=False)
    )

    # Tạo bảng blogPosts
    op.create_table('blogPosts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('userID', sa.String(length=36), sa.ForeignKey("user.id")),
        sa.Column('authorname', sa.String(length=20)),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('imagepath', sa.String(length=255)),
        sa.Column('publish', sa.Boolean, default=False),
        sa.Column('likes', sa.Integer, default=0)
    )

    # Tạo bảng commentsBlog
    op.create_table('commentsBlog',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=100), sa.ForeignKey("blogPosts.title"), nullable=False),
        sa.Column('username', sa.String(length=20)),
        sa.Column('comment', sa.Text, nullable=False)
    )

    # Tạo bảng chat
    op.create_table('chat',
        sa.Column('id', sa.String(length=36), primary_key=True, unique=True, nullable=False),
        sa.Column('userID1', sa.String(length=36), sa.ForeignKey("user.id"), nullable=False),
        sa.Column('userID2', sa.String(length=36), sa.ForeignKey("user.id"), nullable=False)
    )

    # Tạo bảng messages
    op.create_table('messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('room_id', sa.String(length=50), sa.ForeignKey("chat.id"), unique=True, nullable=False)
    )

    # Tạo bảng chat_messages
    op.create_table('chat_messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, nullable=False),
        sa.Column('sender_id', sa.Integer, nullable=False),
        sa.Column('sender_username', sa.String(length=50), nullable=False),
        sa.Column('room_id', sa.String(length=50), sa.ForeignKey("messages.room_id"), nullable=False)
    )

    # Tạo bảng notification
    op.create_table('notification',
        sa.Column('count', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('myid', sa.Integer, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, nullable=False),
        sa.Column('from_id', sa.String(length=50), nullable=False),
        sa.Column('ischat', sa.Boolean)
    )

    # Tạo bảng likedBlogs
    op.create_table('likedBlogs',
        sa.Column('title', sa.String(length=100), sa.ForeignKey("blogPosts.title"), nullable=False),
        sa.Column('userID', sa.String(length=36), sa.ForeignKey("user.id"), nullable=False),
        sa.Column('liked', sa.Boolean)
    )

def downgrade():
    # Xóa bảng khi rollback
    op.drop_table('likedBlogs')
    op.drop_table('notification')
    op.drop_table('chat_messages')
    op.drop_table('messages')
    op.drop_table('chat')
    op.drop_table('commentsBlog')
    op.drop_table('blogPosts')
    op.drop_table('user')
