import mysql.connector

def dbConnect():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ithertzwhenIP#1984',
            database='nursingHomeDB'
        )
    except ConnectionError as ex:
        print(ex)
        return None
    
    return db