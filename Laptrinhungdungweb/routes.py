from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory
from Laptrinhungdungweb import app
import os
import sqlite3  
import bcrypt
import uuid





curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)


def getDB():
    conn = sqlite3.connect(os.path.join(curr_dir, "openu.db"))
    cursor = conn.cursor()
    return cursor, conn



@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        message = ""  # Initialize an empty message
        
        if request.method == "POST":
            emailAddr = request.form['email'].strip()
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            cursor, conn = getDB()
            rows = cursor.execute("SELECT username FROM user WHERE emailAddr = ?", (emailAddr,)).fetchall()

            if rows:
                message = "User already exists"
            else:
                id = str(uuid.uuid4())
                query = "INSERT INTO user (id, username, emailAddr, password) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (id, username, emailAddr, password))
                conn.commit()
                message = "Registration successful"  # Update the message

                return redirect('/home')

    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "You broke the server :(", 400

    return render_template("register.html", message=message)

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')