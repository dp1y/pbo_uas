from datetime import datetime
from connection import *


mycursor = mydb.cursor()
preferred_table = None

def get_table_name():
    global preferred_table
    if preferred_table:
        return preferred_table
    try:
        mycursor.execute("SHOW TABLES LIKE 'kendaraan'")
        if mycursor.fetchone():
            preferred_table = 'kendaraan'
            return preferred_table
        mycursor.execute("SHOW TABLES LIKE 'kendaraan_masuk'")
        if mycursor.fetchone():
            preferred_table = 'kendaraan_masuk'
            return preferred_table
    except Exception:
        pass
    preferred_table = 'kendaraan_masuk'
    return preferred_table


class Kendaraan:
    def __init__(self):
        self.nopol = ""
        self.waktu_masuk = None
        self.waktu_keluar = None
        self.status = "parkir"

    @staticmethod
    def is_nopol_exists(nopol):
        table = get_table_name()
        sql = f"SELECT COUNT(*) FROM {table} WHERE nopol = %s AND status != 'keluar'"
        mycursor.execute(sql, (nopol,))
        result = mycursor.fetchone()
        return result and result[0] > 0
    
    @staticmethod
    def get_kendaraan_detail(nopol):
        table = get_table_name()
        sql = f"SELECT nopol, waktu_masuk, waktu_keluar, status FROM {table} WHERE nopol = %s AND status != 'keluar' ORDER BY waktu_masuk DESC LIMIT 1"
        cursor = mydb.cursor()
        try:
            cursor.execute(sql, (nopol,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
    
    @staticmethod
    def hitung_tarif(waktu_masuk, waktu_keluar, tarif_per_jam):
        if waktu_masuk and waktu_keluar:
            durasi = waktu_keluar - waktu_masuk
            jam = durasi.total_seconds() / 3600
            if jam < 1:
                jam = 1
            subtotal = int(jam * tarif_per_jam)
            return subtotal, jam
        return 0, 0
    
    @staticmethod
    def hitung_tarif_bus(kapasitas):
        base_tarif = 10000
        if kapasitas <= 10:
            return base_tarif
        extra_penumpang = kapasitas - 10
        extra_tarif = (extra_penumpang // 5) * 2500
        return base_tarif + extra_tarif
    
    @staticmethod
    def get_all_kendaraan():
        table = get_table_name()
        sql = f"SELECT nopol, waktu_masuk,petugas_masuk, waktu_keluar,petugas_keluar, status FROM {table} ORDER BY waktu_masuk DESC"
        cursor = mydb.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            try:
                cursor.close()
            except Exception:
                pass
    
    @staticmethod
    def search_kendaraan(keyword):
        table = get_table_name()
        sql = f"SELECT nopol, waktu_masuk, waktu_keluar, status FROM {table} WHERE nopol LIKE %s ORDER BY waktu_masuk DESC"
        cursor = mydb.cursor()
        try:
            cursor.execute(sql, (f"%{keyword}%",))
            return cursor.fetchall()
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def get_detail_pribadi(nopol):
        try:
            cursor = mydb.cursor()
            sql = "SELECT tipe, tarif FROM kendaraan_pribadi WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            return cursor.fetchone()
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def get_detail_bus(nopol):
        try:
            cursor = mydb.cursor()
            sql = "SELECT kategori, kapasitas, tarif FROM bus WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            return cursor.fetchone()
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def get_jenis_kendaraan(nopol):
        try:
            cursor = mydb.cursor()
            sql = "SELECT tipe FROM kendaraan_pribadi WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            result = cursor.fetchone()
            if result:
                return result[0]
            
            sql = "SELECT kategori FROM bus WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            result = cursor.fetchone()
            if result:
                return result[0]
            
            return "Unknown"
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def get_tarif_per_jam(nopol):
        try:
            cursor = mydb.cursor()
            sql = "SELECT tarif FROM kendaraan_pribadi WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            result = cursor.fetchone()
            if result:
                return result[0]
            
            sql = "SELECT tarif FROM bus WHERE nopol = %s"
            cursor.execute(sql, (nopol,))
            result = cursor.fetchone()
            if result:
                return result[0]
            
            return 0
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def calculate_total_revenue():
        try:
            table = get_table_name()
            cursor = mydb.cursor()
            sql = f"""
                SELECT SUM(
                    CAST(
                        FLOOR((TIMESTAMPDIFF(SECOND, k.waktu_masuk, k.waktu_keluar) / 3600)) * COALESCE(
                            kp.tarif,
                            b.tarif,
                            0
                        ) AS UNSIGNED
                    )
                ) as total
                FROM {table} k
                LEFT JOIN kendaraan_pribadi kp ON k.nopol = kp.nopol
                LEFT JOIN bus b ON k.nopol = b.nopol
                WHERE DATE(k.waktu_masuk) = CURDATE() AND k.status = 'keluar' AND k.waktu_keluar IS NOT NULL
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result[0] else 0
        except Exception:
            return 0
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def get_all_kendaraan_with_jenis():
        try:
            table = get_table_name()
            cursor = mydb.cursor()
            sql = f"""
                SELECT 
                    k.nopol,
                    COALESCE(kp.tipe, b.kategori, 'Unknown') as jenis,
                    k.waktu_masuk,
                    k.petugas_masuk,
                    k.waktu_keluar,
                    k.petugas_keluar,
                    COALESCE(kp.tarif, b.tarif, 0) as tarif_per_jam,
                    k.status
                FROM {table} k
                LEFT JOIN kendaraan_pribadi kp ON k.nopol = kp.nopol
                LEFT JOIN bus b ON k.nopol = b.nopol
                ORDER BY k.waktu_masuk DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    @staticmethod
    def search_kendaraan_with_jenis(keyword, jenis_filter=None):
        try:
            table = get_table_name()
            cursor = mydb.cursor()
            
            if jenis_filter and jenis_filter != "Semua":
                sql = f"""
                    SELECT 
                        k.nopol,
                        COALESCE(kp.tipe, b.kategori, 'Unknown') as jenis,
                        k.waktu_masuk,
                        k.petugas_masuk,
                        k.waktu_keluar,
                        k.petugas_keluar,
                        COALESCE(kp.tarif, b.tarif, 0) as tarif_per_jam,
                        k.status
                    FROM {table} k
                    LEFT JOIN kendaraan_pribadi kp ON k.nopol = kp.nopol
                    LEFT JOIN bus b ON k.nopol = b.nopol
                    WHERE k.nopol LIKE %s AND (kp.tipe = %s OR b.kategori = %s)
                    ORDER BY k.waktu_masuk DESC
                """
                cursor.execute(sql, (f"%{keyword}%", jenis_filter, jenis_filter))
            else:
                sql = f"""
                    SELECT 
                        k.nopol,
                        COALESCE(kp.tipe, b.kategori, 'Unknown') as jenis,
                        k.waktu_masuk,
                        k.petugas_masuk,
                        k.waktu_keluar,
                        k.petugas_keluar,
                        COALESCE(kp.tarif, b.tarif, 0) as tarif_per_jam,
                        k.status
                    FROM {table} k
                    LEFT JOIN kendaraan_pribadi kp ON k.nopol = kp.nopol
                    LEFT JOIN bus b ON k.nopol = b.nopol
                    WHERE k.nopol LIKE %s
                    ORDER BY k.waktu_masuk DESC
                """
                cursor.execute(sql, (f"%{keyword}%",))
            
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def kendaraan_masuk(self, nopol, petugas):
        self.nopol = nopol
        self.waktu_masuk = datetime.now()    
        self.petugas = petugas

        table = get_table_name()
        sql = f"INSERT INTO {table} (nopol, waktu_masuk, status, petugas_masuk) VALUES (%s, %s, %s, %s)"
        val = (self.nopol, self.waktu_masuk, self.status, self.petugas)

        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"Data {self.nopol} berhasil ditambahkan.")
        except Exception as e:
            print(f"Gagal insert: {e}")
            mydb.rollback()
    
    def kendaraan_keluar(self, nopol, petugas):
        self.nopol = nopol
        self.waktu_keluar = datetime.now()
        self.petugas = petugas
        self.status = "keluar"


        table = get_table_name()
        try:
            cursor = mydb.cursor()
            sql = f"UPDATE {table} SET waktu_keluar = %s, status = %s , petugas_keluar = %s WHERE nopol = %s"
            cursor.execute(sql, (self.waktu_keluar, self.status, self.petugas, self.nopol))

            mydb.commit()
            cursor.close()
            print(f"Data {self.nopol} berhasil diupdate.")
        except Exception as e:
            print(f"Gagal update: {e}")
            try:
                mydb.rollback()
            except Exception:
                pass

class Kendaraan_pribadi(Kendaraan):
    def __init__(self):
        super().__init__()
        self.tipe = ""
        self.tarif = 0
    
    def kendaraan_masuk(self, nopol, tipe, tarif, petugas):
        super().kendaraan_masuk(nopol,petugas)
        self.nopol = nopol
        self.tipe = tipe
        self.tarif = tarif
        self.petugas = petugas

        sql = "INSERT INTO kendaraan_pribadi (nopol, tipe, tarif) VALUES (%s, %s, %s)"
        val = (self.nopol, self.tipe, self.tarif,)

        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"Data {self.nopol} berhasil ditambahkan.")
        except Exception as e:
            print(f"Gagal insert: {e}")
            mydb.rollback()

class Bus(Kendaraan):
    def __init__(self):
        super().__init__()
        self.kategori = ""
        self.kapasitas = 0
        self.tarif = 0

    def kendaraan_masuk(self, nopol, kategori, kapasitas, tarif, petugas):
        super().kendaraan_masuk(nopol,petugas)
        self.nopol = nopol
        self.kategori = kategori
        self.kapasitas = kapasitas
        self.tarif = tarif
        sql = "INSERT INTO bus (nopol, kategori, kapasitas, tarif) VALUES (%s, %s, %s, %s)"
        val = (self.nopol, self.kategori, self.kapasitas, self.tarif)

        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"Data {self.nopol} berhasil ditambahkan")
        except Exception as e:
            print(f"Gagal insert: {e}")
            mydb.rollback()