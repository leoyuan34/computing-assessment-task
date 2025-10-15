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
    


def create_post(username, title, content, image_path=None):
    """Create a new post."""
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''
            INSERT INTO posts (username, title, content, image_path, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (username, title, content, image_path))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error creating post: {e}")
        return False

def get_user_posts(username):
    """Get all posts by a specific user."""
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM posts 
        WHERE username = ? 
        ORDER BY created_at DESC
    ''', (username,))
    posts = cur.fetchall()
    con.close()
    return posts

def get_all_posts():
    """Get all posts for the feed."""
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM posts 
        ORDER BY created_at DESC
    ''')
    posts = cur.fetchall()
    con.close()
    return posts

def delete_post(post_id, username):
    """Delete a post (only if it belongs to the user)."""
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''
            DELETE FROM posts 
            WHERE id = ? AND username = ?
        ''', (post_id, username))
        con.commit()
        con.close()
        return True
    except:
        return False

def init_posts_table():
    """Initialize the posts table if it doesn't exist."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    con.commit()
    con.close()

init_posts_table()

def like_post(post_id, username):
    """Toggle like on a post."""
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        
        cur.execute('''
            SELECT * FROM likes 
            WHERE post_id = ? AND username = ?
        ''', (post_id, username))
        
        existing_like = cur.fetchone()
        
        if existing_like:
            cur.execute('''
                DELETE FROM likes 
                WHERE post_id = ? AND username = ?
            ''', (post_id, username))
        else:
            cur.execute('''
                INSERT INTO likes (post_id, username, created_at)
                VALUES (?, ?, datetime('now'))
            ''', (post_id, username))
        
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error toggling like: {e}")
        return False

def get_post_likes(post_id):
    """Get number of likes for a post."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,))
    count = cur.fetchone()[0]
    con.close()
    return count

def has_user_liked(post_id, username):
    """Check if user has liked a post."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM likes 
        WHERE post_id = ? AND username = ?
    ''', (post_id, username))
    liked = cur.fetchone() is not None
    con.close()
    return liked

def add_comment(post_id, username, comment_text):
    """Add a comment to a post."""
    try:
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''
            INSERT INTO comments (post_id, username, comment_text, created_at)
            VALUES (?, ?, ?, datetime('now'))
        ''', (post_id, username, comment_text))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error adding comment: {e}")
        return False

def get_post_comments(post_id):
    """Get all comments for a post."""
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM comments 
        WHERE post_id = ? 
        ORDER BY created_at DESC
    ''', (post_id,))
    comments = cur.fetchall()
    con.close()
    return comments

def get_comment_count(post_id):
    """Get number of comments for a post."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM comments WHERE post_id = ?', (post_id,))
    count = cur.fetchone()[0]
    con.close()
    return count

def init_likes_and_comments_tables():
    """Initialize the likes and comments tables."""
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(post_id, username)
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    con.commit()
    con.close()

init_likes_and_comments_tables()