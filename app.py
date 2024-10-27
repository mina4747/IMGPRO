from flask import Flask, request, render_template
import sqlite3
import os
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance

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
    selected = request.form.get('options')
    Filter = request.form.get('Filter')
    if selected and Filter:
        print(selected)
        conn = sqlite3.connect('images.db')
        c= conn.cursor()
        list= refrechList()
        c.execute('SELECT img FROM images WHERE name = ?' , (selected,))
        data = c.fetchone()
        with open( "static/hankhanka.jpeg" , 'wb') as file:
            file.write(data[0])
        conn.commit()
        conn.close()
        if Filter == "cont":
            adjust_contrast("static/hankhanka.jpeg", "static/hankhanka.jpeg")
        elif Filter =="sat":
            adjust_saturation("static/hankhanka.jpeg","static/hankhanka.jpeg")
        elif Filter =="gray":
            convert_to_grayscale("static/hankhanka.jpeg","static/hankhanka.jpeg")
        elif Filter == "blur":
            apply_blur("static/hankhanka.jpeg","static/hankhanka.jpeg")
        else:
            return render_template('index.html', list = list , img = selected)
               
    return render_template('index.html', list = list , img = selected)

def adjust_saturation(image_path, output_path, factor=1.5):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Color(image)
    saturated_image = enhancer.enhance(factor)
    saturated_image.save(output_path)


def adjust_contrast(image_path, output_path, factor=1.5):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    contrasted_image = enhancer.enhance(factor)
    contrasted_image.save(output_path)


def apply_blur(image_path, output_path, radius=5):
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    blurred_image.save(output_path)

def convert_to_grayscale(image_path, output_path):
    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    grayscale_image.save(output_path)

if __name__ == '__main__':

    init_db()  # Initialize the database
    app.run(debug=True)




    
