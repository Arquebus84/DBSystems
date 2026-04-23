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
        cursor = db.cursor()
        #region first test
        # ID = None
        # query1= 'Select paymentID, price, tax from payment_system'
        # query2 = 'SELECT paymentID FROM payment_system WHERE price = %s AND tax = %s'
        # values = ('10.5', '1.64')
        # cursor.execute(query2, values)
        # # cursor.fetchall()
        # for x in cursor:
        #     ID = str(x[0])
        #     print(ID)
        # if ID is None:
        #     cursor.fetchall()
        #     query3 = 'Insert IGNORE into payment_system (price, tax) values (%s, %s)'
        #     cursor.execute(query3, values)
        #     cursor.fetchall()
        #     cursor.execute(query1)
        #     for n in cursor:
        #         ID = str(n[0])
        #         print(ID, str(n[1]), str(n[2]))
        # print(ID)
        # for x in cursor:
        #     print(x)
        # db.commit()
        # endregion
        
        numberID = None
        query0 = 'SELECT numberID from phone_number'
        query1 = 'SELECT numberID from phone_number WHERE phone_number.phoneNumber = %s'
        value = ['912-210-4218']
        cursor.execute(query1, value)
        # cursor.fetchall()
        for x in cursor:
            numberID = str(x[0])
        if (numberID is None):
            cursor.fetchall()
            query2 = 'INSERT IGNORE INTO phone_number (phoneNumber) VALUES (%s)'
            cursor.execute(query2, value)
            for n in cursor:
                numberID = str(n[0])
        cursor.fetchall()
        # print(numberID)
        query3 = 'INSERT IGNORE INTO trusted_family (familyLastName, phoneNumberID) VALUES (%s, %s)'
        value2 = ['Ventura', numberID]
        cursor.execute(query3, value2)
        cursor.fetchall()
        cursor.execute('SELECT familyLastName, phoneNumberID from trusted_family')
        for x in cursor:
            print(x)
        db.commit()

        return 'Valid'
    except mysql.connector.Error as e:
        print(e)
        return "Not valid"

check_connection()

# @app.route('/')
# def index():
#     is_connected = check_connection()
#     if(is_connected):
#         return '<h4>Connected Successfully<h4>'
#     else:
#         return '<h4>Not Connected<h4>'
    
# if(__name__ == '__main__'):
#     app.run(debug=True)

# cursor = db.cursor()
# cursor.execute("SELECT f.facultyLastName, ft.facultyType FROM faculty f JOIN faculty_type ft WHERE f.facultyTypeID = ft.facultyTypeID")

# for x in cursor:
#     print(x)