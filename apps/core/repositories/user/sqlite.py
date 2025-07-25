# apps/core/repositories/user/sqlite.py
import sqlite3
import uuid
import datetime
import logging
from typing import Optional, List, Union
import asyncio
import base64
import os

from apps.core.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from apps.core.repositories.user.base import AbstractUserRepository


def parse_date_or_none(value: Optional[str]) -> Optional[datetime.date]:
    try:
        return datetime.date.fromisoformat(value) if value else None
    except Exception:
        return None

def parse_datetime_or_none(value: Optional[str]) -> Optional[datetime.datetime]:
    try:
        return datetime.datetime.fromisoformat(value) if value else None
    except Exception:
        return None

class SqliteUserRepository(AbstractUserRepository):
    EXTRA_COLUMNS = [
        'phone_number', 'address', 'date_of_birth',
        'date_joined', 'last_login', 'is_verified',
        'role', 'role_display'
    ]
    ALLOWED_UPDATE = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'username', 'role']

    def __init__(self, db_path="db.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                address TEXT,
                date_of_birth TEXT,
                date_joined TEXT,
                last_login TEXT,
                is_verified TEXT DEFAULT '0',
                role TEXT,
                profile_picture TEXT,
                role_display TEXT,
                is_superuser TEXT DEFAULT '0',
                is_staff TEXT DEFAULT '0',
                is_active TEXT DEFAULT '1'
            )
            """)
            conn.commit()

            cursor.execute("PRAGMA table_info(core_user)")
            existing = [row["name"] for row in cursor.fetchall()]
            for col in self.EXTRA_COLUMNS:
                if col not in existing:
                    try:
                        default = " DEFAULT '0'" if col in ["is_verified", "is_superuser"] else ""
                        cursor.execute(f"ALTER TABLE core_user ADD COLUMN {col} TEXT{default}")
                        conn.commit()
                    except sqlite3.OperationalError as e:
                        print(f"Failed to add column {col}: {e}")

    async def create_user(self, data: UserCreateSchema) -> dict:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._create_user_sync, data)

    def _create_user_sync(self, data: UserCreateSchema) -> dict:
        with self._connect() as conn:
            cursor = conn.cursor()
            now = datetime.datetime.utcnow().isoformat()
            profile_picture = getattr(data, "profile_picture", None)
            if profile_picture:
                # Nếu profile_picture bắt đầu với /media/ thì bỏ đi
                if profile_picture.startswith("/media/"):
                    relative_path = profile_picture[len("/media/"):]
                else:
                    relative_path = profile_picture
            else:
                relative_path = None
            cursor.execute("""
                INSERT INTO core_user
                (username,email,password,first_name,last_name,
                date_joined,is_verified,role,is_superuser,is_staff,is_active, profile_picture)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                data.username, data.email, data.password,
                data.first_name or "", data.last_name or "",
                now, "0", "user", "0", "0", "1",relative_path
            ))
            conn.commit()
            return self._get_by_id_sync(cursor.lastrowid)

    async def get_by_id(self, user_id: Union[int, str]) -> Optional[dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_by_id_sync, user_id)

    def _get_by_id_sync(self, user_id: Union[int, str]) -> Optional[dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM core_user WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                print(f"User ID {user_id} not found")
                return None
            return {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone_number": row["phone_number"],
                "address": row["address"],
                "date_of_birth": parse_date_or_none(row["date_of_birth"]),
                "date_joined": parse_datetime_or_none(row["date_joined"]),
                "last_login": parse_datetime_or_none(row["last_login"]),
                "is_verified": row["is_verified"] == "1" if row["is_verified"] else False,
                "role": row["role"] or "user",
                "role_display": row["role_display"] or "",
                "profile_picture": f"/media/{row['profile_picture']}" if row["profile_picture"] else "",
                "farms": [],
                "current_farm": None,
            }

    async def get_by_username(self, username: str) -> Optional[dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_simple_user_sync, ("username", username))

    async def get_by_email(self, email: str) -> Optional[dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_simple_user_sync, ("email", email))

    def _get_simple_user_sync(self, by: tuple) -> Optional[dict]:
        key, value = by
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT id, username, email, first_name, last_name FROM core_user WHERE {key} = ?",
                (value,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def update_user(self, user_id: Union[int, str], data: UserUpdateSchema) -> dict:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._update_user_sync, user_id, data)

    def _update_user_sync(self, user_id: Union[int, str], data: UserUpdateSchema) -> dict:
        user_id = int(user_id)
        ud = data.dict(exclude_unset=True)
        fields, values = [], []
        PROFILE_PICTURE_FOLDER = os.path.join("media", "profile_pictures")
        os.makedirs(PROFILE_PICTURE_FOLDER, exist_ok=True)
        profile_picture = ud.pop("profile_picture", None)
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT profile_picture FROM core_user WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if profile_picture:
                if hasattr(profile_picture, "read") and hasattr(profile_picture, "name"):
                    ext = os.path.splitext(profile_picture.name)[-1] or ".jpg"
                    filename = f"{uuid.uuid4().hex}{ext}"
                    filepath = os.path.join(PROFILE_PICTURE_FOLDER, filename)
                    with open(filepath, "wb") as f:
                        f.write(profile_picture.read())
                    relative_path = f"profile_pictures/{filename}"
                    fields.append("profile_picture = ?")
                    values.append(relative_path)
                elif isinstance(profile_picture, str):
                    relative_path = profile_picture.lstrip("/media/")
                    fields.append("profile_picture = ?")
                    values.append(relative_path)
                else:
                    raise ValueError("profile_picture phải là file hoặc chuỗi đường dẫn hợp lệ")
            for k in self.ALLOWED_UPDATE:
                if k in ud:
                    val = ud[k]
                    if isinstance(val, (datetime.date, datetime.datetime)):
                        val = val.isoformat()
                    fields.append(f"{k} = ?")
                    values.append(val)
            if not fields:
                raise ValueError("No valid fields to update")
            values.append(user_id)
            cursor.execute(f"UPDATE core_user SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
            return self._get_by_id_sync(user_id)

    async def delete_user(self, user_id: Union[int, str]) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._delete_user_sync, user_id)

    def _delete_user_sync(self, user_id: Union[int, str]) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM core_user WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    async def change_password(self, user_id: Union[int, str], new_password: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._change_password_sync, user_id, new_password)

    def _change_password_sync(self, user_id: Union[int, str], new_password: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE core_user SET password = ? WHERE id = ?", (new_password, user_id))
            conn.commit()
            return cursor.rowcount > 0

    async def initiate_password_reset(self, email: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._initiate_password_reset_sync, email)

    def _initiate_password_reset_sync(self, email: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM core_user WHERE email = ?", (email,))
            row = cursor.fetchone()
            if not row:
                return False
            user_id = row["id"]
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reset_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    expires_at DATETIME NOT NULL
                )
            """)
            conn.commit()
            token = str(uuid.uuid4())
            expires_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat()
            cursor.execute(
                "INSERT INTO reset_tokens (user_id, token, expires_at) VALUES (?,?,?)",
                (user_id, token, expires_at)
            )
            conn.commit()
            print(f"Reset token for {email}: {token}")
            return True

    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._confirm_password_reset_sync, token, new_password)

    def _confirm_password_reset_sync(self, token: str, new_password: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            now = datetime.datetime.utcnow().isoformat()
            cursor.execute(
                "SELECT user_id FROM reset_tokens WHERE token = ? AND expires_at > ?",
                (token, now)
            )
            row = cursor.fetchone()
            if not row:
                return False
            user_id = row["user_id"]
            cursor.execute("UPDATE core_user SET password = ? WHERE id = ?", (new_password, user_id))
            cursor.execute("DELETE FROM reset_tokens WHERE token = ?", (token,))
            conn.commit()
            return True

    async def get_password_hash(self, user_id: Union[int, str]) -> Optional[str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_password_hash_sync, user_id)

    def _get_password_hash_sync(self, user_id: Union[int, str]) -> Optional[str]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM core_user WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return row["password"] if row else None

    async def list_users(self) -> List[dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._list_users_sync)

    def _list_users_sync(self) -> List[dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, first_name, last_name,
                    phone_number, address, date_of_birth, profile_picture,
                    role, is_verified, date_joined, last_login, is_superuser
                FROM core_user
            """)
            users = []
            for row in cursor.fetchall():
                user = dict(row)
                if user["profile_picture"]:
                    user["profile_picture"] = f"/media/{user['profile_picture']}" if user["profile_picture"] else ""
                else:
                    user["profile_picture"] = ""
                users.append(user)
            return users

    async def list_free_users(self, farm_id: Union[int, str]) -> List[dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._list_free_users_sync, farm_id)

    def _list_free_users_sync(self, farm_id: Union[int, str]) -> List[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, first_name, last_name
                FROM core_user WHERE id NOT IN (
                    SELECT user_id FROM farm_farmmembership WHERE farm_id = ?
                )
            """, (farm_id,))
            return [dict(row) for row in cursor.fetchall()]

    
    async def save_password_reset_token(self, user_id: int, token: str) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._save_password_reset_token_sync, user_id, token)

    def _save_password_reset_token_sync(self, user_id: int, token: str) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            # Tạo bảng token nếu chưa có
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reset_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    expires_at DATETIME NOT NULL
                )
            """)
            cursor.execute("DELETE FROM reset_tokens WHERE user_id = ?", (user_id,))
            expires_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat()
            cursor.execute(
                "INSERT INTO reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
                (user_id, token, expires_at)
            )
            conn.commit()


