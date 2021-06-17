import sqlite3
import datetime

db_name = r'db/tbot.db'


class User:
    def add(self, data):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute("select * from users where userid =" + str(data[0]) + ";")
        result = cur.fetchone()

        if result is None:
            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", data)
            conn.commit()
        else:
            print("Юзер уже есть")


    # проверка есть ли подписка и не кончилась ли она
    # select * from users where userid=0000 and access=1 AND sub_end_date >= "2021-06-25"
    def paid(self, data):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute("select * from users where userid=" + str(data) + " AND access=1 AND sub_end_date >=\"" + str(datetime.date.today()) + "\";")
        result = cur.fetchone()

        if result is None:
            return False
        else:
            return True

        return False


    def check_sub(self, data):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute("select * from users where userid=" + str(data) + " and access=1;")
        result = cur.fetchone()

        if result is None:
            return {"status_sub": False, "sub_end": ""}
        else:
            return {"status_sub": True, "sub_end": result[6]}

        return {"status_sub": False, "sub_end": ""}

def init_db():
    conn = sqlite3.connect(db_name)  # создание/инициализация БД

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       userid INT PRIMARY KEY,
       name TEXT,
       email TEXT,
       access INT,
       reg_date TEXT,
       sub_start_date TEXT,
       sub_end_date TEXT);
    """)
    conn.commit()
