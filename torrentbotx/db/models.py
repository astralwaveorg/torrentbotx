import sqlite3

from torrentbotx.db.connection import create_connection


def create_tables():
    """创建数据库表"""
    conn = create_connection()
    if conn is None:
        print("无法连接到数据库")
        return

    try:
        cursor = conn.cursor()

        # 创建种子表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS torrents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hash TEXT NOT NULL UNIQUE,
                category TEXT,
                state TEXT,
                added_on INTEGER,
                progress REAL,
                ratio REAL
            )
        ''')

        # 创建任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                torrent_id INTEGER,
                status TEXT,
                scheduled_time INTEGER,
                FOREIGN KEY (torrent_id) REFERENCES torrents(id)
            )
        ''')

        # 创建分类表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cate_id INTEGER,
                name TEXT
            )
        ''')

        # 提交更改并关闭连接
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite 错误: {e}")
