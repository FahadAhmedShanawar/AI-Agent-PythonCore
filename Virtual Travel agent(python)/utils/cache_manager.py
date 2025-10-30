import sqlite3
import json
import os
from datetime import datetime, timedelta
import logging

class CacheManager:
    def __init__(self, db_path='cache/cache.db', expiry_hours=24):
        self.db_path = db_path
        self.expiry_hours = expiry_hours
        self._ensure_cache_dir()
        self._init_db()

    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        cache_dir = os.path.dirname(self.db_path)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _init_db(self):
        """Initialize SQLite database for caching"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp TEXT
                )
            ''')

    def set(self, key, value, expiry_hours=None):
        """Store value in cache"""
        if expiry_hours is None:
            expiry_hours = self.expiry_hours

        expiry_time = datetime.now() + timedelta(hours=expiry_hours)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)',
                (key, json.dumps(value), expiry_time.isoformat())
            )

    def get(self, key):
        """Retrieve value from cache if not expired"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute(
                'SELECT value, timestamp FROM cache WHERE key = ?',
                (key,)
            ).fetchone()

        if result:
            value, timestamp = result
            expiry_time = datetime.fromisoformat(timestamp)

            if datetime.now() < expiry_time:
                return json.loads(value)
            else:
                # Remove expired entry
                self.delete(key)

        return None

    def delete(self, key):
        """Remove entry from cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM cache WHERE key = ?', (key,))

    def clear_expired(self):
        """Remove all expired entries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'DELETE FROM cache WHERE timestamp < ?',
                (datetime.now().isoformat(),)
            )

    def get_stats(self):
        """Get cache statistics"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute('SELECT COUNT(*) FROM cache').fetchone()[0]
            expired = conn.execute(
                'SELECT COUNT(*) FROM cache WHERE timestamp < ?',
                (datetime.now().isoformat(),)
            ).fetchone()[0]

        return {
            'total_entries': total,
            'expired_entries': expired,
            'active_entries': total - expired
        }
