from connection import *
import session

class User:
    def __init__(self):
        self

    @staticmethod
    def login(val1, val2):
        sql = "SELECT level FROM user WHERE username = %s AND password = %s"
        val = (val1, val2)
        mycursor.execute(sql, val)
        level = mycursor.fetchone()
        return str(level[0])

    def get_nama_ptg(username):
        sql = "SELECT nama FROM user WHERE username = %s"
        val = (username, )
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        session.current_user = myresult[0]
        return session.current_user



    @staticmethod
    def select_all_data():
        sql = "SELECT * FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult 
        
    @staticmethod
    def select_data_by_username2(keyword):
        sql = "SELECT * FROM user WHERE username LIKE %s" 
        val = f"%{keyword}%"
        mycursor.execute(sql, (val,))
        myresult = mycursor.fetchall()
        return myresult

    @staticmethod
    def select_data_by_username(val1):
        sql = "SELECT username,nama,password,level FROM user WHERE username = %s"
        val = (val1, )
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        return myresult

    @staticmethod
    def insert_data(val1, val2, val3, val4):
        try:
            sql = "INSERT INTO user (username, nama, password, level) VALUES (%s, %s, %s, %s)"
            val = (val1, val2, val3, val4)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Data berhasil ditambahkan...")
        except Exception as e:
            print("Terjadi error saat menambahkan data:", e)

    @staticmethod
    def update_data(val1, val2, val3, val4):
        try:
            sql = "UPDATE user SET nama = %s, password =  %s, level = %s WHERE username = %s"
            val = (val2, val3, val4, val1)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Data berhasil diupdate...")
        except Exception as e:
            print("Terjadi error saat mengupdate data:", e)

    @staticmethod
    def delete_data(val1):
        try:
            sql = "DELETE FROM user WHERE username = %s"
            val = (val1, )
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Data berhasil dihapus...")
        except Exception as e:
            print("Terjadi error saat menghapus data:", e)

    @staticmethod
    def select_data():
        sql = "SELECT * FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    
    @staticmethod
    def search(keyword):
        sql = """
            SELECT nama, username, password, level
            FROM user
            WHERE username LIKE %s
        """
        val = ("%" + keyword + "%", )
        mycursor.execute(sql, val)
        return mycursor.fetchall()
    @staticmethod
    def get_user_by_username(username):
        sql = "SELECT nama, username, password, level FROM user WHERE username = %s"
        val = (username,)
        try:
            cursor = mydb.cursor()
            cursor.execute(sql, val)
            user = cursor.fetchone()
            return user
        finally:
            try:
                cursor.close()
            except Exception:
                pass
