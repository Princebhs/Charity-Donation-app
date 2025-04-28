# Charity Donation Tracking System

A Python-based database application for tracking charitable donations, events, and volunteers.

## Installation

1. Ensure you have Python 3.x installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Initialize the database:
   ```bash
   python database_init.py
   ```
2. Run the application:
   ```bash
   python main.py
   ```

## Features

- Create, view, update and delete donations, events, volunteers and donors
- Search for donations by donor, volunteer, or event
- Track monetary donations with gift aid information
- Manage events and volunteer assignments
- Maintain donor information for both individuals and businesses

## Database Schema

The system uses SQLite with the following table structure:

### Donors
- `donor_id` (Primary Key)
- `first_name`
- `surname`
- `business_name`
- `postcode`
- `house_number`
- `phone_number`
- `donor_type` (individual/business)

### Volunteers
- `volunteer_id` (Primary Key)
- `first_name`
- `surname`
- `phone_number`
- `email`
- `join_date`

### Events
- `event_id` (Primary Key)
- `event_name`
- `room_name`
- `booking_date`
- `booking_time`
- `cost`
- `organizer_id` (Foreign Key to Volunteers)

### Donations
- `donation_id` (Primary Key)
- `amount`
- `donation_date`
- `gift_aid`
- `notes`
- `donor_id` (Foreign Key to Donors)
- `event_id` (Foreign Key to Events)
- `collected_by` (Foreign Key to Volunteers)

### Event Volunteers
- `event_id` (Foreign Key to Events)
- `volunteer_id` (Foreign Key to Volunteers)
- `role`

## Dependencies

- Python 3.x
- SQLite (included in Python)
- tkinter (included in Python)
- tkcalendar (for date picker widgets)

## Development

For development, additional tools are available:
- pytest for unit testing
- black for code formatting
- flake8 for code linting

## Data Constraints

- Donations must be monetary values (positive numbers)
- Donors cannot be deleted if they have associated donations
- Events cannot be deleted if they have associated donations
- Gift aid is tracked for each donation
- Each donation must be associated with a donor and collector (volunteer)
- Events are optional for donations
