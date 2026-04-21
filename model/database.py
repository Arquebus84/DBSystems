import mysql.connector
from flask import Flask

app = Flask(__name__)

def check_connection():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ithertzwhenIP#1984',
            database='nursingHomeDB'
        )
        return True
    except mysql.connector.Error as e:
        print(e)
        return False

@app.route('/')
def index():
    is_connected = check_connection()
    if(is_connected):
        return '<h4>Connected Successfully<h4>'
    else:
        return '<h4>Not Connected<h4>'
    
# if(__name__ == '__main__'):
#     app.run(debug=True)

# cursor = db.cursor()
# cursor.execute("SELECT f.facultyLastName, ft.facultyType FROM faculty f JOIN faculty_type ft WHERE f.facultyTypeID = ft.facultyTypeID")

# for x in cursor:
#     print(x)