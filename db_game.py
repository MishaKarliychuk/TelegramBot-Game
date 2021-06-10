import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('games.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS games')
    c. execute("""
    CREATE TABLE IF NOT EXISTS games(
        id INTEGER PRIMARY KEY,
        ind_if INTEGER NOT NULL,
        user TEXT,
        start TEXT,
        bet INT,
        mark INT,
        win INT
    )""")
    conn.commit()

init_db()
##########

def upd_user_game(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE games SET user = ? WHERE id = ?',(info, id))
    conn.commit()

def upd_user_game_ind_if(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE games SET user = ? WHERE ind_if = ?',(info, id))
    conn.commit()

def add_game(ind_if,users,start,bet,win):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'INSERT INTO games (ind_if, user, start, bet,mark,win) VALUES ({ind_if},{users}, "{start}", {bet},0,{win})')
    conn.commit()

def all_game():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    return c.fetchall()

def one_game(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE ind_if = ?', ([id]))
    return c.fetchone()

def one_game_id(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE id = ?', ([id]))
    return c.fetchone()

def upd_mark_game(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE games SET mark = ? WHERE ind_if = ?',(info, id))
    conn.commit()

def delete_game(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM games WHERE ind_if=?',(id,))
    conn.commit()

def delete_all_game():
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM games')
    conn.commit()