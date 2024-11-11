import os
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import app, db
from model import Notification, Chat, ChatMessage, User  # Đảm bảo các model đã được định nghĩa trong file model.py

# Khởi tạo Flask-SocketIO
socketio = SocketIO(app)

@socketio.on("add_stack_noti")
def handle_add_stack_noti(data):
    to_id = data["to"]
    from_id = data["from"]
    time = data["timestamp"]
    content = data["message"]

    # Thêm thông báo mới vào cơ sở dữ liệu PostgreSQL
    new_notification = Notification(
        myid=to_id,
        content=content,
        timestamp=time,
        from_id=from_id,
        ischat=False
    )
    db.session.add(new_notification)
    db.session.commit()

@socketio.on("join-chat")
def join_private_chat(data):
    room = data["rid"]
    myid = data["myid"]
    join_room(room=room)

    # Lấy thông tin về người dùng trong phòng chat từ PostgreSQL
    chat = Chat.query.filter_by(id=room).first()
    if not chat:
        return

    id1, id2 = chat.userID1, chat.userID2
    add_friend_info = None

    if myid == id1:
        add_friend_info = User.query.filter_by(id=id2).first().username
    else:
        add_friend_info = User.query.filter_by(id=id1).first().username

    arr_data = [add_friend_info, room]
    socketio.emit("joined-chat", arr_data, room=data["rid"])

@socketio.on("outgoing")
def chatting_event(data, methods=["GET", "POST"]):
    """
    Handles saving messages and sending messages to all clients
    """
    room_id = data["rid"]
    timestamp = data["timestamp"]
    message = data["message"]
    sender_id = data["sender_id"]
    sender_username = data["sender_username"]

    try:
        # Thêm tin nhắn mới vào bảng chat_messages
        new_message = ChatMessage(
            content=message,
            timestamp=timestamp,
            sender_id=sender_id,
            sender_username=sender_username,
            room_id=room_id
        )
        db.session.add(new_message)
        db.session.commit()

        chat = Chat.query.filter_by(id=room_id).first()
        if not chat:
            return

        des_id = chat.userID2 if chat.userID1 == sender_id else chat.userID1

        # Kiểm tra xem đã có thông báo từ người gửi chưa
        existing_notification = Notification.query.filter_by(myid=des_id, from_id=sender_id).first()
        if not existing_notification:
            new_notification = Notification(
                myid=des_id,
                content=message,
                timestamp=timestamp,
                from_id=sender_id,
                ischat=True
            )
            db.session.add(new_notification)
            db.session.commit()

    except Exception as e:
        print(f"Error saving message to the database: {str(e)}")

    # Phát tin nhắn tới các người dùng khác trong phòng
    join_room(room=room_id)
    socketio.emit("message", data, room=room_id, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
