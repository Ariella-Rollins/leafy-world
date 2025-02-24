from flask_app.config.mysql_connection import connect_to_mysql

# Connect to MySQL
conn = connect_to_mysql.connect(host='localhost', user='root', password='root', database='plant_quiz')
cursor = conn.cursor()

# Open the file in binary mode
with open('flask_app/static/images/herbs/1.jpg', 'rb') as file:
    binary_data = file.read()

# Insert binary data. rb means read-binary
cursor.execute("""INSERT INTO plants (common_name, latin_name, pic_A) 
            VALUES ("Allium scallion", "Scallion/green onion" """, ('Sample File', binary_data))
conn.commit()

cursor.close()
conn.close()
