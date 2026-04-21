import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ithertzwhenIP#1984',
    database='nursingHomeDB'
)

cursor = db.cursor()
cursor.execute("SELECT f.facultyLastName, ft.facultyType FROM faculty f JOIN faculty_type ft WHERE f.facultyTypeID = ft.facultyTypeID")

for x in cursor:
    print(x)