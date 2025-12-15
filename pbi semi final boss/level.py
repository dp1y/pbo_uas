from connection import *

class Level:
    def __init__(self):
        self

    def select_data():
        sql = "SELECT level FROM level"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        data = []
        for x in myresult:
            data.append(str(x).replace("(","")
                        .replace("'","")
                        .replace("'","")
                        .replace(")","")
                        .replace(",",""))
            print(x)
        return data
    
    def insert_data(val1):
        sql = "INSERT INTO level (level) VALUES (%s)"
        val = (val1,)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil ditambahkan...")


Level.select_data()