import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "data_source.db"

def listExtension():
  con = sql.connect("data_source.db")
  cur = con.cursor()
  data = cur.execute('SELECT * FROM extension').fetchall()
  con.close()
  return data

def add_user(username, age, email, password):
    """Add a new user to the database."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    hashed_pw = generate_password_hash(password)
    cur.execute(
        "INSERT INTO extension (username, user_age, password, email) VALUES (?, ?, ?, ?)",
        (username, age, hashed_pw, email),
    )
    con.commit()
    con.close()

def get_user_by_email(email):
    """Fetch a user by email."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM extension WHERE email = ?", (email,))
    user = cur.fetchone()
    con.close()
    return user

def get_user_by_username(username):
    """Fetch a user by username."""
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM extension WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    return user

def verify_user(email, password):
    con = sql.connect("data_source.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM extension WHERE email = ?", (email,))
    user = cur.fetchone()
    con.close()
    
    if user and check_password_hash(user['password'], password):
        return user
    return None

def update_username(old_username, new_username):
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''
            UPDATE extension 
            SET username = ? 
            WHERE username = ?
        ''', (new_username, old_username))
        con.commit()
        con.close()
        return True
    except:
        return False

def update_email(username, new_email):
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''
            UPDATE extension 
            SET email = ? 
            WHERE username = ?
        ''', (new_email, username))
        con.commit()
        con.close()
        return True
    except:
        return False

def update_password(username, new_password):
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        hashed_pw = generate_password_hash(new_password)
        cur.execute('''
            UPDATE extension 
            SET password = ? 
            WHERE username = ?
        ''', (hashed_pw, username))
        con.commit()
        con.close()
        return True
    except:
        return False