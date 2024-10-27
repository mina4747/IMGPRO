from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("images.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT  ,
        img BLOB NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Function to insert image into the database
def insert_to_db(name , image_data):
    conn = sqlite3.connect("images.db")
    c = conn.cursor()
    c.execute('INSERT INTO images ( name ,img) VALUES (? , ?)', ( name ,image_data))
    conn.commit()
    conn.close()

def refrechList():
    conn = sqlite3.connect("images.db")
    c = conn.cursor()
    c.execute("SELECT name FROM images")
    list = c.fetchall()
    conn.close()
    return list

@app.route('/')
def home():
    list= refrechList()
    return render_template('index.html' , list = list)

@app.route('/add', methods=['POST'])
def add():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    # Read the file as binary
    image_data = file.read()
    name = file.filename
    # Insert the image data into the database
    insert_to_db(name , image_data)

    print("File uploaded and saved to the database successfully!")
    list = refrechList()
    return render_template('index.html' , list = list)

@app.route('/choose', methods=['POST'])
def convert():
    selected = request.form.get('options') if request.form.get('options') else "nothing niga"
    print(selected)
    conn = sqlite3.connect('images.db')
    c= conn.cursor()
    list= refrechList()
    c.execute('SELECT img FROM images WHERE name = ?' , (selected,))
    data = c.fetchone()
    with open( selected , 'wb') as file:
        file.write(data[0])
    conn.commit()
    conn.close()
     
    return render_template('index.html', list = list , img = selected)



if __name__ == '__main__':

    init_db()  # Initialize the database
    app.run(debug=True)




    
