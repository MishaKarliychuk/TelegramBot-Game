import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('participant.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS participant')
    c. execute("""
    CREATE TABLE IF NOT EXISTS participant(
        id INTEGER PRIMARY KEY,
        id_game INTEGER NOT NULL,
        user_id INT,
        oponent INT,
        score TEXT,
        test_score TEXT,
        choice TEXT,
        round INT,
        code INT,
        gen_round INT,
        last_sms INT
    )""")
    conn.commit()

init_db()

def add_part(id_game,user_id,oponent):
    conn = get_connection()
    c = conn.cursor()
    sc = '0,0'
    c.execute(f'INSERT INTO participant (id_game, user_id, oponent, score,test_score,choice,round,gen_round) VALUES ({id_game},{user_id},{oponent}, "{sc}", 0, 0,1,1)')
    conn.commit()

def participant(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM participant WHERE user_id = ?',([id]))
    return c.fetchone()

def participant_all():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM participant')
    return c.fetchall()


def upd_choice(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET choice = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_last_sms(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET last_sms = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_round(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET round = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_gen_round(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET gen_round = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_score_user(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET score = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_test_score(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET test_score = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_code(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE participant SET code = ? WHERE user_id = ?',(info, id))
    conn.commit()

def delete(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM participant WHERE user_id=?',(id,))
    conn.commit()