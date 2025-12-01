"""Database manager for all database operations."""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import os
from .models import (
    CREATE_USERS_TABLE,
    CREATE_SUBSCRIPTIONS_TABLE,
    CREATE_MESSAGES_TABLE,
    CREATE_UPLOAD_HISTORY_TABLE,
    CREATE_INDEXES,
)


class DatabaseManager:
    """Handles all database operations."""

    def __init__(self, db_path: str = "database/gym_management.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self._ensure_database_exists()
        self._create_tables()

    def _ensure_database_exists(self):
        """Create database directory if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        """Create all tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_SUBSCRIPTIONS_TABLE)
            cursor.execute(CREATE_MESSAGES_TABLE)
            cursor.execute(CREATE_UPLOAD_HISTORY_TABLE)

            for index_sql in CREATE_INDEXES:
                cursor.execute(index_sql)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # User operations
    def create_user(self, email: str, password_hash: str, gym_name: str) -> Optional[int]:
        """Create a new user. Returns user_id if successful."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash, gym_name) VALUES (?, ?, ?)",
                (email, password_hash, gym_name)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_last_login(self, user_id: int):
        """Update user's last login timestamp."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now(), user_id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # Subscription operations
    def save_subscriptions(self, subscriptions: List[Dict]) -> int:
        """Save multiple subscriptions. Returns count of saved records."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            for sub in subscriptions:
                cursor.execute(
                    """INSERT INTO subscriptions
                    (user_id, upload_batch_id, customer_name, phone_number,
                     subscription_start_date, subscription_end_date, days_remaining, cluster)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        sub['user_id'],
                        sub['upload_batch_id'],
                        sub['customer_name'],
                        sub['phone_number'],
                        sub['subscription_start_date'],
                        sub['subscription_end_date'],
                        sub['days_remaining'],
                        sub['cluster']
                    )
                )
            conn.commit()
            return len(subscriptions)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_subscriptions_by_batch(self, batch_id: str) -> List[Dict]:
        """Get all subscriptions for a batch."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM subscriptions WHERE upload_batch_id = ? ORDER BY cluster, days_remaining",
                (batch_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_subscriptions_by_cluster(self, batch_id: str, cluster: int) -> List[Dict]:
        """Get subscriptions for a specific cluster."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM subscriptions WHERE upload_batch_id = ? AND cluster = ? ORDER BY days_remaining",
                (batch_id, cluster)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def delete_subscriptions_by_batch(self, batch_id: str):
        """Delete all subscriptions for a batch."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM subscriptions WHERE upload_batch_id = ?", (batch_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # Message operations
    def save_messages(self, messages: List[Dict]) -> int:
        """Save multiple messages. Returns count of saved records."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            for msg in messages:
                cursor.execute(
                    """INSERT INTO messages (subscription_id, message_text, cluster)
                    VALUES (?, ?, ?)""",
                    (msg['subscription_id'], msg['message_text'], msg['cluster'])
                )
            conn.commit()
            return len(messages)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_messages_by_batch(self, batch_id: str) -> List[Dict]:
        """Get all messages for a batch with subscription details."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """SELECT m.*, s.customer_name, s.phone_number, s.subscription_end_date, s.days_remaining
                FROM messages m
                JOIN subscriptions s ON m.subscription_id = s.id
                WHERE s.upload_batch_id = ?
                ORDER BY m.cluster, s.days_remaining""",
                (batch_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # Upload history operations
    def save_upload_history(self, user_id: int, batch_id: str, filename: str,
                           total_rows: int, processed_rows: int) -> int:
        """Save upload history. Returns history_id."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """INSERT INTO upload_history (user_id, batch_id, filename, total_rows, processed_rows)
                VALUES (?, ?, ?, ?, ?)""",
                (user_id, batch_id, filename, total_rows, processed_rows)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_upload_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get upload history for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """SELECT * FROM upload_history
                WHERE user_id = ?
                ORDER BY upload_date DESC
                LIMIT ?""",
                (user_id, limit)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_latest_batch_id(self, user_id: int) -> Optional[str]:
        """Get the latest batch_id for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """SELECT batch_id FROM upload_history
                WHERE user_id = ?
                ORDER BY upload_date DESC
                LIMIT 1""",
                (user_id,)
            )
            row = cursor.fetchone()
            return row['batch_id'] if row else None
        finally:
            conn.close()

    def get_cluster_counts(self, batch_id: str) -> Dict[int, int]:
        """Get count of subscriptions per cluster for a batch."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """SELECT cluster, COUNT(*) as count
                FROM subscriptions
                WHERE upload_batch_id = ?
                GROUP BY cluster""",
                (batch_id,)
            )
            rows = cursor.fetchall()
            return {row['cluster']: row['count'] for row in rows}
        finally:
            conn.close()
