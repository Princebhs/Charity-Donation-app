from database.db_connection import get_db
from datetime import datetime

class Volunteer:
    def __init__(self, volunteer_id=None, first_name=None, surname=None,
                 phone_number=None, email=None, join_date=None):
        self.volunteer_id = volunteer_id
        self.first_name = first_name
        self.surname = surname
        self.phone_number = phone_number
        self.email = email
        self.join_date = join_date

    @staticmethod
    def create(first_name, surname, phone_number, email, join_date=None):
        if join_date is None:
            join_date = datetime.now().strftime('%Y-%m-%d')
            
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO volunteers (first_name, surname, phone_number, email, join_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, surname, phone_number, email, join_date))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM volunteers')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(volunteer_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM volunteers WHERE volunteer_id = ?', (volunteer_id,))
            return cursor.fetchone()

    @staticmethod
    def update(volunteer_id, first_name, surname, phone_number, email):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE volunteers 
                SET first_name=?, surname=?, phone_number=?, email=?
                WHERE volunteer_id=?
            ''', (first_name, surname, phone_number, email, volunteer_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(volunteer_id):
        with get_db() as conn:
            cursor = conn.cursor()
            # Check if volunteer has any associated donations or events
            cursor.execute('''
                SELECT COUNT(*) FROM 
                (SELECT collected_by FROM donations WHERE collected_by = ?
                 UNION
                 SELECT organizer_id FROM events WHERE organizer_id = ?
                 UNION
                 SELECT volunteer_id FROM event_volunteers WHERE volunteer_id = ?)
            ''', (volunteer_id, volunteer_id, volunteer_id))
            
            if cursor.fetchone()[0] > 0:
                return False  # Can't delete volunteer with associated records
            
            cursor.execute('DELETE FROM volunteers WHERE volunteer_id = ?', (volunteer_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search(term):
        with get_db() as conn:
            cursor = conn.cursor()
            search_term = f'%{term}%'
            cursor.execute('''
                SELECT * FROM volunteers 
                WHERE first_name LIKE ? 
                OR surname LIKE ? 
                OR email LIKE ?
            ''', (search_term, search_term, search_term))
            return cursor.fetchall()
