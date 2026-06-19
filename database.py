"""Database operations for the finance tracker app.

Pure logic layer — does not depend on Streamlit.
All functions accept and return plain Python types.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Optional

DB_PATH = Path(__file__).parent / "finance.db"

CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "其他"]


def get_conn():
    """Return a SQLite connection with row_factory set."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the transactions table if it does not exist."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id       INTEGER PRIMARY KEY,
                amount   REAL    NOT NULL,
                category TEXT    NOT NULL,
                date     TEXT    NOT NULL,
                notes    TEXT    DEFAULT ''
            )
        """)


def add_transaction(amount: float, category: str, date: str, notes: str) -> int:
    """Insert a new transaction. Returns the new row ID."""
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transactions (amount, category, date, notes) VALUES (?, ?, ?, ?)",
            (amount, category, date, notes),
        )
        return cursor.lastrowid


def get_transactions(month: Optional[str] = None, category: Optional[str] = None) -> list[dict]:
    """Return transactions, optionally filtered by month (YYYY-MM) or category.

    Args:
        month:  e.g. "2026-06" or None for all months.
        category: one of CATEGORIES or None for all categories.

    Returns:
        List of dicts ordered by date descending.
    """
    conditions = []
    params = []

    if month:
        conditions.append("strftime('%Y-%m', date) = ?")
        params.append(month)
    if category:
        conditions.append("category = ?")
        params.append(category)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    query = f"SELECT * FROM transactions {where} ORDER BY date DESC"

    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def delete_transaction(tid: int) -> int:
    """Delete a transaction by ID, then renumber subsequent IDs to fill the gap.

    Example: delete ID 2 → old IDs [1,2,3,4] become [1,2,3] with old 3→2, 4→3.
    """
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM transactions WHERE id = ?", (tid,))
        affected = cursor.rowcount
        if affected > 0:
            # Shift all higher IDs down by 1
            conn.execute("UPDATE transactions SET id = id - 1 WHERE id > ?", (tid,))
        return affected


def get_stats() -> list[dict]:
    """Return per-category aggregates: total amount and count, ordered by total desc."""
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT category,
                   SUM(amount)  AS total,
                   COUNT(*)     AS count
            FROM transactions
            GROUP BY category
            ORDER BY total DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_months() -> list[str]:
    """Return distinct year-month strings (YYYY-MM) from the database, newest first."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT strftime('%Y-%m', date) AS month FROM transactions ORDER BY month DESC"
        ).fetchall()
    return [row["month"] for row in rows]
