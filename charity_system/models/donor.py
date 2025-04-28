from database.db_connection import get_db

class Donor:
    def __init__(self, donor_id=None, first_name=None, surname=None, business_name=None,
                 postcode=None, house_number=None, phone_number=None, donor_type=None):
        self.donor_id = donor_id
        self.first_name = first_name
        self.surname = surname
        self.business_name = business_name
        self.postcode = postcode
        self.house_number = house_number
        self.phone_number = phone_number
        self.donor_type = donor_type

    @staticmethod
    def create(first_name, surname, business_name, postcode, house_number, phone_number, donor_type):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO donors (first_name, surname, business_name, postcode, 
                                  house_number, phone_number, donor_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, surname, business_name, postcode, house_number, phone_number, donor_type))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM donors')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(donor_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM donors WHERE donor_id = ?', (donor_id,))
            return cursor.fetchone()

    @staticmethod
    def update(donor_id, first_name, surname, business_name, postcode, house_number, phone_number, donor_type):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE donors 
                SET first_name=?, surname=?, business_name=?, postcode=?, 
                    house_number=?, phone_number=?, donor_type=?
                WHERE donor_id=?
            ''', (first_name, surname, business_name, postcode, house_number, 
                 phone_number, donor_type, donor_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(donor_id):
        with get_db() as conn:
            cursor = conn.cursor()
            # First check if donor has any donations
            cursor.execute('SELECT COUNT(*) FROM donations WHERE donor_id = ?', (donor_id,))
            if cursor.fetchone()[0] > 0:
                return False  # Can't delete donor with donations
            
            cursor.execute('DELETE FROM donors WHERE donor_id = ?', (donor_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search(term):
        with get_db() as conn:
            cursor = conn.cursor()
            search_term = f'%{term}%'
            cursor.execute('''
                SELECT * FROM donors 
                WHERE first_name LIKE ? 
                OR surname LIKE ? 
                OR business_name LIKE ?
                OR postcode LIKE ?
            ''', (search_term, search_term, search_term, search_term))
            return cursor.fetchall()
