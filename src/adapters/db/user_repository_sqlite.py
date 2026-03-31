import sqlite3
from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository

from .database import get_connection
from .mappers import row_to_user, user_to_row


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, user: User) -> User:
        """INSERT OR REPLACE INTO users"""
        row = user_to_row(user)
        conn = get_connection(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT OR REPLACE INTO users (id, username, is_agent, is_admin)
                VALUES (:id, :username, :is_agent, :is_admin)
                """,
                row,
            )
            conn.commit()
        finally:
            conn.close()
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        """SELECT * FROM users WHERE id = ?"""
        conn = get_connection(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, is_agent, is_admin FROM users WHERE id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                # sqlite3.Row -> dict-like or tuple depending on row_factory
                # Normalize to dict for row_to_user which expects dict
                # If using Row, convert using keys
                if isinstance(row, sqlite3.Row):
                    row_dict = {k: row[k] for k in row.keys()}
                else:
                    row_dict = {
                        "id": row[0],
                        "username": row[1],
                        "is_agent": row[2],
                        "is_admin": row[3],
                    }
                return row_to_user(row_dict)
            return None
        finally:
            conn.close()

    def find_by_username(self, username: str) -> Optional[User]:
        """SELECT * FROM users WHERE username = ?"""
        conn = get_connection(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, is_agent, is_admin FROM users WHERE username = ?",
                (username,),
            )
            row = cur.fetchone()
            if row:
                if isinstance(row, sqlite3.Row):
                    row_dict = {k: row[k] for k in row.keys()}
                else:
                    row_dict = {
                        "id": row[0],
                        "username": row[1],
                        "is_agent": row[2],
                        "is_admin": row[3],
                    }
                return row_to_user(row_dict)
            return None
        finally:
            conn.close()

    def list_all(self) -> list[User]:
        """SELECT * FROM users"""
        conn = get_connection(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, username, is_agent, is_admin FROM users")
            rows = cur.fetchall()
            users = []
            for row in rows:
                if isinstance(row, sqlite3.Row):
                    row_dict = {k: row[k] for k in row.keys()}
                else:
                    row_dict = {
                        "id": row[0],
                        "username": row[1],
                        "is_agent": row[2],
                        "is_admin": row[3],
                    }
                users.append(row_to_user(row_dict))
            return users
        finally:
            conn.close()
