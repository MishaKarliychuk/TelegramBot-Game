import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('users.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    c. execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        played_game INT,
        wallet INT,
        last_deposit INT,
        current_game INT,
        name TEXT
    )""")
    conn.commit()

init_db()
##########



def upd_current_game(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET current_game = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_wallet(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET wallet = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_played_game(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET played_game = ? WHERE user_id = ?',(info, id))
    conn.commit()

def add_user(idd,name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'INSERT INTO users (user_id, played_game, wallet, last_deposit,current_game,name) VALUES ({idd}, 0, 0, 0,0,"{name}")')
    conn.commit()

def current_game_user(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?',([id]))
    return c.fetchone()

def take_user(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?',([id]))
    return c.fetchone()

def take_user_all():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    return c.fetchall()


def waiting_second(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT contastent FROM battle WHERE game = ?',([id]))
    return c.fetchone()



