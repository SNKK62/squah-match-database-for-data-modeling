import sqlite3
from typing import Final
from flask import g

DATABASE: Final[str] = 'database/gakuren.db'

def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # カラム名でアクセスできるよう設定変更
    return db

def close_db_connection() -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
