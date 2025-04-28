from database.db_connection import get_db
from datetime import datetime

class Event:
    def __init__(self, event_id=None, event_name=None, room_name=None,
                 booking_date=None, booking_time=None, cost=None, organizer_id=None):
        self.event_id = event_id
        self.event_name = event_name
        self.room_name = room_name
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.cost = cost
        self.organizer_id = organizer_id

    @staticmethod
    def create(event_name, room_name, booking_date, booking_time, cost, organizer_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (event_name, room_name, booking_date, 
                                  booking_time, cost, organizer_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (event_name, room_name, booking_date, booking_time, cost, organizer_id))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.*, v.first_name || ' ' || v.surname as organizer_name 
                FROM events e 
                LEFT JOIN volunteers v ON e.organizer_id = v.volunteer_id
            ''')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(event_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.*, v.first_name || ' ' || v.surname as organizer_name 
                FROM events e 
                LEFT JOIN volunteers v ON e.organizer_id = v.volunteer_id
                WHERE e.event_id = ?
            ''', (event_id,))
            return cursor.fetchone()

    @staticmethod
    def update(event_id, event_name, room_name, booking_date, booking_time, cost, organizer_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE events 
                SET event_name=?, room_name=?, booking_date=?, 
                    booking_time=?, cost=?, organizer_id=?
                WHERE event_id=?
            ''', (event_name, room_name, booking_date, booking_time, 
                 cost, organizer_id, event_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(event_id):
        with get_db() as conn:
            cursor = conn.cursor()
            # Check if event has any donations
            cursor.execute('SELECT COUNT(*) FROM donations WHERE event_id = ?', (event_id,))
            if cursor.fetchone()[0] > 0:
                return False  # Can't delete event with donations
            
            # Delete event volunteers first (due to foreign key constraint)
            cursor.execute('DELETE FROM event_volunteers WHERE event_id = ?', (event_id,))
            
            # Delete the event
            cursor.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search(term):
        with get_db() as conn:
            cursor = conn.cursor()
            search_term = f'%{term}%'
            cursor.execute('''
                SELECT e.*, v.first_name || ' ' || v.surname as organizer_name 
                FROM events e 
                LEFT JOIN volunteers v ON e.organizer_id = v.volunteer_id
                WHERE e.event_name LIKE ? 
                OR e.room_name LIKE ?
                OR v.first_name || ' ' || v.surname LIKE ?
            ''', (search_term, search_term, search_term))
            return cursor.fetchall()

    @staticmethod
    def assign_volunteer(event_id, volunteer_id, role):
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO event_volunteers (event_id, volunteer_id, role)
                    VALUES (?, ?, ?)
                ''', (event_id, volunteer_id, role))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # Volunteer already assigned or invalid IDs

    @staticmethod
    def remove_volunteer(event_id, volunteer_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM event_volunteers 
                WHERE event_id = ? AND volunteer_id = ?
            ''', (event_id, volunteer_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_event_volunteers(event_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.*, ev.role
                FROM volunteers v
                JOIN event_volunteers ev ON v.volunteer_id = ev.volunteer_id
                WHERE ev.event_id = ?
            ''', (event_id,))
            return cursor.fetchall()
