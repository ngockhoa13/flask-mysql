from app.extensions import socketio, db
from flask_socketio import join_room
from app.model import Notification, User, Chat, ChatMessage

@socketio.on("add_stack_noti")
def handle_add_stack_noti(data):
    try:
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
    except Exception as e:
        print(f"Error adding notification: {str(e)}")

@socketio.on("join-chat")
def join_private_chat(data):
    try:
        room = data["rid"]
        myid = data["myid"]
        join_room(room=room)

        # Lấy thông tin về người dùng trong phòng chat từ PostgreSQL
        chat = Chat.query.filter_by(id=room).first()
        if not chat:
            return

        id1, id2 = chat.userID1, chat.userID2
        add_friend_info = User.query.filter_by(id=id2).first().username if myid == id1 else User.query.filter_by(id=id1).first().username

        arr_data = [add_friend_info, room]
        socketio.emit("joined-chat", arr_data, room=data["rid"])
    except Exception as e:
        print(f"Error joining chat: {str(e)}")

@socketio.on("outgoing")
def chatting_event(data):
    try:
        room_id = data["rid"]
        timestamp = data["timestamp"]
        message = data["message"]
        sender_id = data["sender_id"]
        sender_username = data["sender_username"]

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

        # Kiểm tra thông báo
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

        # Phát tin nhắn tới các người dùng khác trong phòng
        join_room(room=room_id)
        socketio.emit("message", data, room=room_id, include_self=False)

    except Exception as e:
        print(f"Error sending message: {str(e)}")
