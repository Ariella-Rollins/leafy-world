# 🌿 Leafy World is a Plant-loving Community
## 🌱 Here you can:
* Learn about plants
* Test your knowledge
* Connect with the community

## ✏️ Authors:
Ariella Rollins   https://github.com/Ariella-Rollins 

## 🌟 How to Use

        python server.py
        * Serving Flask app 'flask_app'
        * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment.
        Use a production WSGI server instead.
        * Running on http://localhost:5000

Run 'python server.py' in your terminal. Copy and paste http://localhost:5000 into your browser.

## ⬇️ Installation

        python pipenv install

First, install all the required packages with the code above. Then, run plant.sql in your MySQL local database software to save the database. Finally, change the user and password in lines 8 and 9 of flask_app/config/mysqlconnection.py to match your database credentials. See below for reference.

connection = pymysql.connect(host = 'localhost',
    user = 'root', # Line 8
    password = 'rootroot', # Line 9
    db = db,
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor,
    autocommit = False)