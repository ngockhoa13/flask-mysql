from app import app, socket
import os
from flask_socketio import emit, join_room, leave_room
import sqlite3  

curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)
# ConnectDB
def getDB():
    conn = sqlite3.connect(os.path.join(curr_dir, "app/openu.db"))
    cursor = conn.cursor()
    return cursor, conn



# Join room using flask_sockerIO by adding user in room and return messages
@socket.on("join-chat")
def join_private_chat(data):
    room = data["rid"]
    join_room(room=room)
    socket.emit(
        "joined-chat",
        {"msg": f"{room} is now online."},
        room=room,
        # include_self=False,
    )
# Outgoing event handler
@socket.on("outgoing")
def chatting_event(json, methods=["GET", "POST"]):
    """
    handles saving messages and sending messages to all clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    room_id = json["rid"]
    timestamp = json["timestamp"]
    message = json["message"]
    sender_id = json["sender_id"]
    sender_username = json["sender_username"]

    try:
        # Thêm tin nhắn mới vào bảng chat_messages
        cursor, conn = getDB()
        cursor.execute(
                """
                INSERT INTO chat_messages (content, timestamp, sender_id, sender_username, room_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (message, timestamp, sender_id, sender_username, room_id)
            )
        conn.commit()
        # Lưu tin nhắn mới vào cơ sở dữ liệu
        # (Do bạn không sử dụng SQLAlchemy, nên phần này không cần thiết)

    except Exception as e:
        # Xử lý lỗi cơ sở dữ liệu, ví dụ: ghi log lỗi hoặc gửi phản hồi lỗi cho client.
        print(f"Error saving message to the database: {str(e)}")

    # Phát tin nhắn đã gửi tới các người dùng khác trong phòng
    join_room(room=room_id)
    socket.emit(
        "message",
        json,
        room=room_id,
        include_self=False,
    )


if __name__ == "__main__":
    socket.run(app, allow_unsafe_werkzeug=True, debug=True)

# @socket.on("outgoing")
# def chatting_event(json, methods=["GET", "POST"]):
#     """
#     handles saving messages and sending messages to all clients
#     :param json: json
#     :param methods: POST GET
#     :return: None
#     """
#     cursor, conn = getDB()



#     room_id = json["rid"]
#     timestamp = json["timestamp"]
#     message = json["message"]
#     sender_id = json["sender_id"]
#     sender_username = json["sender_username"]

#     # Get the message entry for the chat room
#     # Liệu có cần trong code cũ ko vì nó dựa vào mối quan hệ nên mới phải query ------------------
#     message_entry =  cursor.execute("SELECT id, userID1, userID2 FROM chat WHERE userID1 = ? OR userID2 = ?", (id, id)).fetchall()
#     print(message_entry)
#     #---------------------------------------------------------------------------------------------

#     # Add the new message to the conversation
#     '''
#     chat_message = ChatMessage(
#         content=message,
#         timestamp=timestamp,
#         sender_id=sender_id,
#         sender_username=sender_username,
#         room_id=room_id,
#     )
#     '''
#     try:
#         query = "INSERT INTO chat_messages (content, timestamp, sender_id, sender_username, room_id) VALUES (?, ?, ?, ?)"
#         cursor.execute(query, (message, timestamp, sender_id, sender_username, room_id))
#         conn.commit()
#     except Exception as e:
#         # Handle the database error, e.g., log the error or send an error response to the client.
#         print(f"Error saving message to the database: {str(e)}")
# # Đoạn này cần check lại có thể sẽ ko cần -----------------------------------------------------------------------
#     # Add the new chat message to the messages relationship of the message
#     #message_entry.messages.append(chat_message)
#     #query = "INSERT INTO chat_messages (content, timestamp, sender_id, sender_username, room_id) VALUES (?, ?, ?, ?)"
#     #cursor.execute(query, (message, timestamp, sender_id, sender_username, room_id))
#     #conn.commit()

#     # Updated the database with the new message
#     #try:
#     #    chat_message.save_to_db()
#     #    message_entry.save_to_db()
#     #except Exception as e:
#     #    # Handle the database error, e.g., log the error or send an error response to the client.
#     #    print(f"Error saving message to the database: {str(e)}")
#     #    db.session.rollback()
# #---------------------------------------------------------------------------------------------------------------
#     # Emit the message(s) sent to other users in the room
#     socket.emit(
#         "message",
#         json,
#         room=room_id,
#         include_self=False,
#     )
# #--------------------------------------------------------------------------------------------------------