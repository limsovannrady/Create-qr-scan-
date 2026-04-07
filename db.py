import os
import sqlite3
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "")
SQLITE_PATH = "/tmp/bot_data.db"


def _use_pg():
    return bool(DATABASE_URL)


def get_conn():
    if _use_pg():
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    if _use_pg():
        import psycopg2
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     BIGINT PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                last_name   TEXT,
                first_seen  TEXT,
                last_seen   TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id          SERIAL PRIMARY KEY,
                user_id     BIGINT,
                username    TEXT,
                full_name   TEXT,
                action      TEXT,
                detail      TEXT,
                timestamp   TEXT
            )
        """)
        conn.commit()
        conn.close()
    else:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                last_name   TEXT,
                first_seen  TEXT,
                last_seen   TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                username    TEXT,
                full_name   TEXT,
                action      TEXT,
                detail      TEXT,
                timestamp   TEXT
            )
        """)
        conn.commit()
        conn.close()


def log_activity(user, action, detail=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = user.username or ""
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    conn = get_conn()
    c = conn.cursor()

    if _use_pg():
        c.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, first_seen, last_seen)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                username   = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name  = EXCLUDED.last_name,
                last_seen  = EXCLUDED.last_seen
        """, (user.id, username, first_name, last_name, now, now))
        c.execute("""
            INSERT INTO activities (user_id, username, full_name, action, detail, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user.id, username, full_name, action, detail, now))
    else:
        c.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username   = excluded.username,
                first_name = excluded.first_name,
                last_name  = excluded.last_name,
                last_seen  = excluded.last_seen
        """, (user.id, username, first_name, last_name, now, now))
        c.execute("""
            INSERT INTO activities (user_id, username, full_name, action, detail, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user.id, username, full_name, action, detail, now))

    conn.commit()
    conn.close()


def _fetchall_as_dicts(cursor, rows):
    if _use_pg():
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, row)) for row in rows]
    else:
        return [dict(r) for r in rows]


def get_stats():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM activities")
    total_actions = c.fetchone()[0]
    conn.close()
    return total_users, total_actions


def get_recent_activities(limit=50):
    conn = get_conn()
    c = conn.cursor()
    if _use_pg():
        c.execute("""
            SELECT username, full_name, action, detail, timestamp
            FROM activities ORDER BY id DESC LIMIT %s
        """, (limit,))
    else:
        c.execute("""
            SELECT username, full_name, action, detail, timestamp
            FROM activities ORDER BY id DESC LIMIT ?
        """, (limit,))
    rows = c.fetchall()
    result = _fetchall_as_dicts(c, rows)
    conn.close()
    return result


def get_users():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT user_id, username, first_name, last_name, first_seen, last_seen
        FROM users ORDER BY last_seen DESC
    """)
    rows = c.fetchall()
    result = _fetchall_as_dicts(c, rows)
    conn.close()
    return result
