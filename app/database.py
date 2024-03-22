import sqlite3

# Open database
conn = sqlite3.connect('openu.db')

# Create tables
conn.execute('''CREATE TABLE user (
    id TEXT PRIMARY KEY UNIQUE NOT NULL,
    name VARCHAR(20),
    username VARCHAR(20) NOT NULL,
    emailAddr VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
)''')

conn.execute('''CREATE TABLE blogPosts (
    id INTEGER PRIMARY KEY NOT NULL,
    userID TEXT,
    authorname VARCHAR(20),
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL, 
    imagepath VARCHAR(255),
    publish BOOLEAN,
    FOREIGN KEY(userID) REFERENCES user(id)
)''')


#conn.execute('''CREATE TABLE notifications (
#    id INTEGER PRIMARY KEY NOT NULL,
#    nameProd VARCHAR(100) NOT NULL,
#    priceProd FLOAT NOT NULL,
#    description TEXT NOT NULL,
#    sellerID INTEGER,
#    FOREIGN KEY(sellerID) REFERENCES seller(id)
#)''')

# Close the connection
conn.close()
