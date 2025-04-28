import sqlite3
from pathlib import Path

def create_database():
    # Create the database file in the same directory as this script
    db_path = Path(__file__).parent / 'charity.db'
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Donors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        surname TEXT,
        business_name TEXT,
        postcode TEXT NOT NULL,
        house_number TEXT,
        phone_number TEXT NOT NULL,
        donor_type TEXT CHECK(donor_type IN ('individual', 'business')) NOT NULL
    )
    ''')
    
    # Create Volunteers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS volunteers (
        volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        join_date DATE NOT NULL
    )
    ''')
    
    # Create Events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        room_name TEXT NOT NULL,
        booking_date DATE NOT NULL,
        booking_time TIME NOT NULL,
        cost DECIMAL(10,2) NOT NULL,
        organizer_id INTEGER,
        FOREIGN KEY (organizer_id) REFERENCES volunteers(volunteer_id)
    )
    ''')
    
    # Create Donations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount DECIMAL(10,2) NOT NULL CHECK(amount > 0),
        donation_date DATE NOT NULL,
        gift_aid BOOLEAN NOT NULL,
        notes TEXT,
        donor_id INTEGER NOT NULL,
        event_id INTEGER,
        collected_by INTEGER NOT NULL,
        FOREIGN KEY (donor_id) REFERENCES donors(donor_id),
        FOREIGN KEY (event_id) REFERENCES events(event_id),
        FOREIGN KEY (collected_by) REFERENCES volunteers(volunteer_id)
    )
    ''')
    
    # Create EventVolunteers junction table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_volunteers (
        event_id INTEGER,
        volunteer_id INTEGER,
        role TEXT NOT NULL,
        PRIMARY KEY (event_id, volunteer_id),
        FOREIGN KEY (event_id) REFERENCES events(event_id),
        FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
    )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully!")
