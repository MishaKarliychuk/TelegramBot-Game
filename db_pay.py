import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('pay_m.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS pay_m')
    c. execute("""
    CREATE TABLE IF NOT EXISTS pay_m(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        phone INT,
        summ INT
    )""")
    conn.commit()

init_db()

def take_user_pay(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pay_m WHERE user_id = ?',([id]))
    return c.fetchone()

def add_user_pay(idd,phone,summ):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'INSERT INTO pay_m (user_id, phone, summ) VALUES ({idd}, {phone}, {summ})')
    conn.commit()

def delete_pay(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM pay_m WHERE user_id=?',(id,))
    conn.commit()