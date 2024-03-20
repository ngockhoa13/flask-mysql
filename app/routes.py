from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory, session
from app import app
import os
import sqlite3  
import bcrypt
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
#Import required library




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

                # Create sessions
                session['loggedin'] = True
                session['id'] = id


                # Adding data to db
                query = "INSERT INTO user (id, username, emailAddr, password) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (id, username, emailAddr, hashed_password))
                conn.commit()

                # Create folder to save user's uploads
                user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
                if not os.path.exists(user_upload_folder):
                    os.makedirs(user_upload_folder)

                message = "Registration successful"
                return redirect('/home')
    # Catch error
    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "You broke the server :(", 400

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
        return "You broke the server :(", 400

@app.route("/")
@app.route("/home")
def home():
    if session.get('loggedin') == True:
        cursor, conn = getDB()
        id = session['id']
        id = cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
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



@app.route('/settings', methods=["GET", "POST"])
def settings():
    id = session.get('id')
    if not id:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    # Retrieve data
    cursor, conn = getDB()
    user_info = cursor.execute("SELECT name, username, emailAddr FROM user WHERE id = ?", (id,)).fetchone()

    # Setting the data of user to output to screen
    name, username, emailAddr = user_info


    profile_pic = None

    # Change the upload folder to inside the user id
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)

    if request.method == "POST":
        
        # Check if the user sent updated information for name, username, or email
        if 'name' in request.form:
            new_name = request.form['name']
            cursor.execute("UPDATE user SET name = ? WHERE id = ?", (new_name, id))
            conn.commit()
            name = new_name

        if 'username' in request.form:
            new_username = request.form['username']
            cursor.execute("UPDATE user SET username = ? WHERE id = ?", (new_username, id))
            conn.commit()
            username = new_username

        if 'email' in request.form:
            new_email = request.form['email']
            cursor.execute("UPDATE user SET emailAddr = ? WHERE id = ?", (new_email, id))
            conn.commit()
            emailAddr = new_email

        if 'password' in request.form:
            new_password = request.form['password']
            new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE user SET password = ? WHERE id = ?", (new_hashed_password, id))
            conn.commit()
            password = new_hashed_password
    

        # Check if the user upload a requests with a profile pic
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename('avatar.jpg')
            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)
            profile_pic = id + '/' + filename
            print(profile_pic)

            flash('File uploaded successfully')
            return render_template('settings.html', name=name, username=username, email=emailAddr, profile_pic=profile_pic)  # Redirect to the settings page
        
        else:
            flash('Invalid file format.')
            return redirect(request.url)
        

    avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], id)
    avatar_path_full = avatar_path + '/avatar.jpg'
    print(avatar_path_full)     
    if os.path.exists(avatar_path):
        profile_pic = id + '/' + 'avatar.jpg'

    # Render the page with the user info that we retrieve
    return render_template('settings.html', name=name, username=username, email=emailAddr, profile_pic=profile_pic)


@app.route('/logout')
def logout():
    session.pop('loggedin')
    session.pop('id')
    return redirect('/login')
