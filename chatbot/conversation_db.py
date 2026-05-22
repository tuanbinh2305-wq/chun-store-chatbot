"""
SQLite — lưu lịch sử hội thoại để Claude AI có context.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "conversations.db"
MAX_HISTORY = 10  # Số tin nhắn gần nhất giữ lại per sender


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Tạo bảng nếu chưa có."""
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id   TEXT    NOT NULL,
                role        TEXT    NOT NULL CHECK(role IN ('user', 'assistant')),
                content     TEXT    NOT NULL,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sender_time
            ON messages (sender_id, created_at DESC)
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_info (
                sender_id   TEXT PRIMARY KEY,
                data        TEXT NOT NULL,
                updated_at  TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """)
        conn.commit()


def save_message(sender_id: str, role: str, content: str) -> None:
    """Lưu 1 tin nhắn vào DB."""
    with _conn() as conn:
        conn.execute(
            "INSERT INTO messages (sender_id, role, content) VALUES (?, ?, ?)",
            (sender_id, role, content),
        )
        conn.commit()


def get_history(sender_id: str) -> list[dict]:
    """
    Lấy lịch sử MAX_HISTORY tin nhắn gần nhất.
    Trả về list [{role, content}] theo thứ tự cũ → mới.
    """
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT role, content FROM messages
            WHERE sender_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (sender_id, MAX_HISTORY),
        ).fetchall()
    # Đảo ngược để có thứ tự cũ → mới
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


def clear_history(sender_id: str) -> None:
    """Xóa lịch sử hội thoại (khi KH đặt hàng xong hoặc yêu cầu)."""
    with _conn() as conn:
        conn.execute("DELETE FROM messages WHERE sender_id = ?", (sender_id,))
        conn.commit()


def save_order_info(sender_id: str, data: dict) -> None:
    """Lưu thông tin đặt hàng đang thu thập."""
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO order_info (sender_id, data, updated_at)
            VALUES (?, ?, datetime('now','localtime'))
            ON CONFLICT(sender_id) DO UPDATE SET
                data = excluded.data,
                updated_at = excluded.updated_at
            """,
            (sender_id, json.dumps(data, ensure_ascii=False)),
        )
        conn.commit()


def get_order_info(sender_id: str) -> dict:
    """Lấy thông tin đặt hàng đang thu thập."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT data FROM order_info WHERE sender_id = ?", (sender_id,)
        ).fetchone()
    return json.loads(row["data"]) if row else {}


def clear_order_info(sender_id: str) -> None:
    """Xóa thông tin đặt hàng sau khi xác nhận."""
    with _conn() as conn:
        conn.execute("DELETE FROM order_info WHERE sender_id = ?", (sender_id,))
        conn.commit()
