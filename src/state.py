import sqlite3
import os
from pathlib import Path

class CrawlStateTracker:
    def __init__(self, db_path: str = "crawl_state.db"):
        self.db_path = Path(db_path)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _execute(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _query(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def _query_one(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def init_db(self):
        self._execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                id TEXT PRIMARY KEY,
                slug TEXT NOT NULL,
                title TEXT NOT NULL,
                module_id TEXT,
                module_title TEXT,
                status TEXT DEFAULT 'PENDING',
                error_message TEXT,
                raw_file_path TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def upsert_lesson(self, lesson_id: str, slug: str, title: str, module_id: str, module_title: str):
        self._execute("""
            INSERT INTO lessons (id, slug, title, module_id, module_title, status)
            VALUES (?, ?, ?, ?, ?, COALESCE((SELECT status FROM lessons WHERE id = ?), 'PENDING'))
            ON CONFLICT(id) DO UPDATE SET
                slug = excluded.slug,
                title = excluded.title,
                module_id = excluded.module_id,
                module_title = excluded.module_title,
                updated_at = CURRENT_TIMESTAMP
        """, (lesson_id, slug, title, module_id, module_title, lesson_id))

    def set_status(self, lesson_id: str, status: str, error_message: str = None, raw_file_path: str = None):
        self._execute("""
            UPDATE lessons
            SET status = ?, error_message = ?, raw_file_path = COALESCE(?, raw_file_path), updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, error_message, raw_file_path, lesson_id))

    def get_lesson(self, lesson_id: str):
        return self._query_one("SELECT * FROM lessons WHERE id = ?", (lesson_id,))

    def get_all_lessons(self):
        return self._query("SELECT * FROM lessons")

    def get_pending_lessons(self):
        return self._query("SELECT * FROM lessons WHERE status IN ('PENDING', 'FAILED')")

    def get_stats(self):
        rows = self._query("""
            SELECT status, COUNT(*) as count
            FROM lessons
            GROUP BY status
        """)
        return {row["status"]: row["count"] for row in rows}

    def reset_failed(self):
        self._execute("UPDATE lessons SET status = 'PENDING', error_message = NULL WHERE status = 'FAILED'")
