from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory, session
from app import app
import os
import sqlite3  
import bcrypt
import uuid
from werkzeug.utils import secure_filename
from PIL import Image





# Settings the utils
curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)

# Checks file extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ConnectDB
def getDB():
    conn = sqlite3.connect(os.path.join(curr_dir, "openu.db"))
    cursor = conn.cursor()
    return cursor, conn


# Register route
@app.route("/")
def lmao():
    if session.get("loggedin")==True:
        cursor= getDB()
        id = cursor.execute("SELECT id from user WHERE id = ?",(session.get('id'),)).fetchone()
        if id:
            return redirect('/home')
        return redirect('/login')
    return redirect('/login')
    



@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    try:
        if request.method == "POST":
            emailAddr = request.form['email'].strip()
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            cursor, conn = getDB()
            rows = cursor.execute("SELECT username FROM user WHERE emailAddr = ?", (emailAddr,)).fetchall()

            if rows:
                message = "User already exists"
            else:
                # Generate ID and hash password
                id = str(uuid.uuid4())
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                print(hashed_password)

                # Adding data to db
                query = "INSERT INTO user (id, username, emailAddr, password) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (id, username, emailAddr, hashed_password))
                conn.commit()

                # Create folder to save user's uploads
                user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
                if not os.path.exists(user_upload_folder):
                    os.makedirs(user_upload_folder)

                message = "Registration successful"
                return redirect('/login')
    # Catch error
    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return render_template("login.html", message = "Error!!!")
    
    return render_template("register.html", message=message)



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if (request.method == "POST"):

            emailAddr = request.form['email'].strip()
            password = request.form['password'].strip()

            # Get user data
            cursor, conn = getDB()
            user_info = cursor.execute("SELECT id, password FROM user WHERE emailAddr = ?",(emailAddr,)).fetchone()

            if user_info:
                id, hashed_password = user_info

                # Check if password is equal to hash
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['loggedin'] = True
                    session['id'] = id
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],session.get('id'))
                    #notes_list = os.listdir(file_path)

                    return redirect('/home')   
                else:
                     return render_template('login.html', message="Wrong Email or Password")
            
            return render_template('login.html', message="Wrong Email or Password")
        return render_template("login.html")
    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return render_template("login.html", message = "Error!!!")


@app.route("/home")
def home():
    if session.get('loggedin') == True:
        cursor = getDB()
        id = cursor.execute("SELECT id FROM user WHERE id = ?",(session.get('id'),)).fetchone()
        if id:        
            return render_template('index.html')
        return redirect('/login')
    else:
        return redirect('/login')

@app.route('/profile')
def profile():
    if session.get('loggedin') == True:
        cursor = getDB()
        id = cursor.execute("SELECT id FROM user WHERE id = ?",(session.get('id'),)).fetchone()
        if id:        
            return render_template('profile.html')
        return redirect('/login')
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('loggedin')
    session.pop('id')
    return redirect('/login')


@app.route('/settings', methods=["GET", "POST"])
def settings():
    id = session['id']
    print(id)
    cursor, conn = getDB()
    user_info = cursor.execute("SELECT name, username, password, emailAddr FROM user WHERE id = ?",(id,)).fetchone()
    
        
    name, username, hashed_password, emailAddr = user_info

    if request.method == "GET":
        return render_template('settings.html', name=name, username=username, email=emailAddr)
    
    elif request.method == "POST":

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Resize the image

            # Add code to update the user's profile picture in the database (if needed)
            flash('File uploaded successfully')
            return render_template('settings.html', profile_pic= filename)  # Redirect to the settings page
        
        else:
            flash('Invalid file format.')
            return redirect(request.url)