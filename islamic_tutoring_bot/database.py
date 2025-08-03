import sqlite3
import logging
from datetime import datetime

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name='bot.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        # Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            streak INTEGER DEFAULT 0,
            daily_requests INTEGER DEFAULT 0,
            monthly_requests INTEGER DEFAULT 0,
            last_active TEXT,
            role TEXT DEFAULT 'student'
        )
        ''')
        
        # Courses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        )
        ''')
        
        # Certificates table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            cert_id TEXT PRIMARY KEY,
            user_id INTEGER,
            course_id INTEGER,
            score REAL,
            issue_date TEXT,
            file_id TEXT
        )
        ''')
        
        self.conn.commit()
    
    def create_user(self, user_id, full_name):
        try:
            self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, full_name, last_active)
            VALUES (?, ?, ?)
            ''', (user_id, full_name, datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    def create_certificate(self, cert_data):
        try:
            self.cursor.execute('''
            INSERT INTO certificates (cert_id, user_id, course_id, score, issue_date, file_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                cert_data['cert_id'],
                cert_data['user_id'],
                cert_data['course_id'],
                cert_data['score'],
                datetime.now().isoformat(),
                cert_data['file_id']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating certificate: {e}")
            return False

# Initialize database
db = Database()
