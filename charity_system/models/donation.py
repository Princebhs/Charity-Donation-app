from database.db_connection import get_db
from datetime import datetime

class Donation:
    def __init__(self, donation_id=None, amount=None, donation_date=None,
                 gift_aid=None, notes=None, donor_id=None, event_id=None, collected_by=None):
        self.donation_id = donation_id
        self.amount = amount
        self.donation_date = donation_date
        self.gift_aid = gift_aid
        self.notes = notes
        self.donor_id = donor_id
        self.event_id = event_id
        self.collected_by = collected_by

    @staticmethod
    def create(amount, donation_date, gift_aid, notes, donor_id, event_id, collected_by):
        if donation_date is None:
            donation_date = datetime.now().strftime('%Y-%m-%d')
            
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO donations (amount, donation_date, gift_aid, notes,
                                     donor_id, event_id, collected_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (amount, donation_date, gift_aid, notes, donor_id, event_id, collected_by))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT d.*,
                       CASE 
                           WHEN dn.business_name IS NOT NULL THEN dn.business_name
                           ELSE dn.first_name || ' ' || dn.surname 
                       END as donor_name,
                       e.event_name,
                       v.first_name || ' ' || v.surname as collector_name
                FROM donations d
                JOIN donors dn ON d.donor_id = dn.donor_id
                LEFT JOIN events e ON d.event_id = e.event_id
                JOIN volunteers v ON d.collected_by = v.volunteer_id
                ORDER BY d.donation_date DESC
            ''')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(donation_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT d.*,
                       CASE 
                           WHEN dn.business_name IS NOT NULL THEN dn.business_name
                           ELSE dn.first_name || ' ' || dn.surname 
                       END as donor_name,
                       e.event_name,
                       v.first_name || ' ' || v.surname as collector_name
                FROM donations d
                JOIN donors dn ON d.donor_id = dn.donor_id
                LEFT JOIN events e ON d.event_id = e.event_id
                JOIN volunteers v ON d.collected_by = v.volunteer_id
                WHERE d.donation_id = ?
            ''', (donation_id,))
            return cursor.fetchone()

    @staticmethod
    def update(donation_id, amount, donation_date, gift_aid, notes, donor_id, event_id, collected_by):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE donations 
                SET amount=?, donation_date=?, gift_aid=?, notes=?,
                    donor_id=?, event_id=?, collected_by=?
                WHERE donation_id=?
            ''', (amount, donation_date, gift_aid, notes, donor_id, 
                 event_id, collected_by, donation_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(donation_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM donations WHERE donation_id = ?', (donation_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search(term=None, donor_id=None, volunteer_id=None, event_id=None):
        with get_db() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT d.*,
                       CASE 
                           WHEN dn.business_name IS NOT NULL THEN dn.business_name
                           ELSE dn.first_name || ' ' || dn.surname 
                       END as donor_name,
                       e.event_name,
                       v.first_name || ' ' || v.surname as collector_name
                FROM donations d
                JOIN donors dn ON d.donor_id = dn.donor_id
                LEFT JOIN events e ON d.event_id = e.event_id
                JOIN volunteers v ON d.collected_by = v.volunteer_id
                WHERE 1=1
            '''
            params = []
            
            if term:
                search_term = f'%{term}%'
                query += '''
                    AND (dn.first_name LIKE ? 
                    OR dn.surname LIKE ?
                    OR dn.business_name LIKE ?
                    OR e.event_name LIKE ?
                    OR v.first_name || ' ' || v.surname LIKE ?)
                '''
                params.extend([search_term] * 5)
            
            if donor_id:
                query += ' AND d.donor_id = ?'
                params.append(donor_id)
            
            if volunteer_id:
                query += ' AND d.collected_by = ?'
                params.append(volunteer_id)
            
            if event_id:
                query += ' AND d.event_id = ?'
                params.append(event_id)
            
            query += ' ORDER BY d.donation_date DESC'
            
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_total_by_donor(donor_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(amount) as total
                FROM donations
                WHERE donor_id = ?
            ''', (donor_id,))
            result = cursor.fetchone()
            return result['total'] if result['total'] else 0.0

    @staticmethod
    def get_total_by_event(event_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(amount) as total
                FROM donations
                WHERE event_id = ?
            ''', (event_id,))
            result = cursor.fetchone()
            return result['total'] if result['total'] else 0.0
