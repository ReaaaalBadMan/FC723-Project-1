import sqlite3
import random
import string

# --------------------------
# Database Setup Functions
# --------------------------
def init_db():
    """
    Initializes the SQLite database and creates the 'bookings' table if it does not exist.
    The table stores booking details: booking reference, passport number, first name, last name,
    seat row, seat column, and the complete seat identifier.
    """
    global conn
    conn = sqlite3.connect("bookings.db")  # Creates or opens the database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_ref TEXT PRIMARY KEY,
            passport_number TEXT,
            first_name TEXT,
            last_name TEXT,
            seat_row INTEGER,
            seat_column TEXT,
            seat_id TEXT UNIQUE
        )
    ''')
    conn.commit()

def generate_booking_ref():
    """
    Generates a unique eight-character alphanumeric booking reference.
    Uses random choices from uppercase letters and digits.
    The function queries the database to ensure that the generated reference is unique,
    generating a new one if a duplicate is found.
    """
    cursor = conn.cursor()
    while True:
        booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_ref = ?", (booking_ref,))
        (count,) = cursor.fetchone()
        if count == 0:
            return booking_ref

def load_existing_bookings():
    """
    Loads booking records from the database and updates the in-memory seats dictionary.
    This ensures that previously booked seats (stored in the database) are marked as booked
    in the application's seating map when the program starts.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT seat_id, booking_ref FROM bookings")
    booked_seats = cursor.fetchall()
    for seat_id, booking_ref in booked_seats:
        if seat_id in seats:
            seats[seat_id] = booking_ref

# --------------------------
# Seating Layout Setup
# --------------------------

# Define seating layout for front and rear sections.
front_rows = range(1, 81)           # Front section rows 1-80
front_columns = ['A', 'B', 'C']      # Front section columns

rear_rows = range(1, 81)            # Rear section rows 1-80
rear_columns = ['D', 'E', 'F']       # Rear section columns

# Create a dictionary to store the current status of each seat.
# For free seats, the value is "F".
# For storage areas, the value is "S".
# For booked seats, the value will be the unique booking reference.
seats = {}

# Initialize front section seats as free.
for row in front_rows:
    for col in front_columns:
        seat_id = str(row) + col
        seats[seat_id] = "F"

# Initialize rear section seats.
# Note: Rows 77 and 78 in the rear section are designated as storage ("S").
for row in rear_rows:
    for col in rear_columns:
        seat_id = str(row) + col
        if row in [77, 78]:
            seats[seat_id] = "S"
        else:
            seats[seat_id] = "F"

# --------------------------
# Application Functionalities
# --------------------------
def check_availability():
    """
    Checks if a specified seat is available for booking.
    Prompts the user to input a seat number and then displays whether the seat is free,
    already booked (shows the booking reference), or not bookable (storage area).
    """
    seat_id = input("Enter the seat number (e.g., 1A, 3D): ").upper()
    if seat_id in seats:
        status = seats[seat_id]
        if status == "F":
            print(f"Seat {seat_id} is free and available for booking.")
        elif status == "S":
            print(f"Seat {seat_id} is a storage area and cannot be booked.")
        else:
            # If the seat status is not F or S, it stores a booking reference.
            print(f"Seat {seat_id} is booked with reference {status}.")
    else:
        print("Invalid seat number. Please try again.")

def book_seat():
    """
    Books a specified seat if it is free.
    In addition to booking the seat, the function:
      - Generates a unique booking reference.
      - Prompts the user for traveller details (passport number, first name, last name).
      - Updates the seat status in the 'seats' dictionary to the booking reference.
      - Inserts a new record with booking details into the SQLite database.
    """
    seat_id = input("Enter the seat number to book (e.g., 1A, 3D): ").upper()
    if seat_id in seats:
        status = seats[seat_id]
        if status == "F":  # Only free seats can be booked
            # Generate a unique 8-character booking reference.
            booking_ref = generate_booking_ref()
            
            # Prompt for traveller details.
            passport_number = input("Enter passport number: ").strip()
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            
            # Determine the seat's row and column based on the seat_id.
            # Assumes the seat_id is in the format <row><column>, e.g., "23B".
            row_part = seat_id[:-1]
            col_part = seat_id[-1]
            try:
                seat_row = int(row_part)
            except ValueError:
                print("Invalid seat row.")
                return

            # Update the seat dictionary with the booking reference.
            seats[seat_id] = booking_ref
            
            # Insert the booking details into the database.
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO bookings (booking_ref, passport_number, first_name, last_name, seat_row, seat_column, seat_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (booking_ref, passport_number, first_name, last_name, seat_row, col_part, seat_id))
                conn.commit()
                print(f"Seat {seat_id} has been successfully booked.")
                print(f"Your booking reference is: {booking_ref}")
            except sqlite3.IntegrityError:
                # In case the booking record already exists, revert the seat status.
                seats[seat_id] = "F"
                print("Error: This seat has already been booked.")
        elif status == "S":
            print(f"Seat {seat_id} is a storage area and cannot be booked.")
        else:
            print(f"Seat {seat_id} is already booked with reference {status}.")
    else:
        print("Invalid seat number. Please try again.")

def free_seat():
    """
    Frees a booked seat.
    Prompts the user to input the seat number. If the seat is booked,
    the function sets the seat status back to free ("F") and removes any
    corresponding booking record from the database.
    """
    seat_id = input("Enter the seat number to free (e.g., 1A, 3D): ").upper()
    if seat_id in seats:
        status = seats[seat_id]
        # Only booked seats (neither free "F" nor storage "S") can be freed.
        if status != "F" and status != "S":
            booking_ref = status  # The current value is the booking reference.
            # Remove the booking record from the database.
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE booking_ref = ?", (booking_ref,))
            conn.commit()
            
            # Update seat status to free.
            seats[seat_id] = "F"
            print(f"Seat {seat_id} has been freed and is now available.")
        elif status == "F":
            print(f"Seat {seat_id} is already free.")
        else:
            print(f"Seat {seat_id} is a storage area and cannot be freed.")
    else:
        print("Invalid seat number. Please try again.")

def show_booking_status():
    """
    Displays the current booking status for the aircraft seating.
    The display is organized by grouping rows (10 at a time) and showing both the front and rear sections,
    with an aisle separator. Booked seats will display the booking reference instead of 'R'.
    """
    while True:
        print("\nSelect rows to display (10 rows at a time):")
        print("1. Rows 1-10")
        print("2. Rows 11-20")
        print("3. Rows 21-30")
        print("4. Rows 31-40")
        print("5. Rows 41-50")
        print("6. Rows 51-60")
        print("7. Rows 61-70")
        print("8. Rows 71-80")
        print("9. Return to main menu")
        
        choice = input("Enter your choice (1-9): ")
        if choice == '9':
            return
        
        try:
            choice = int(choice)
            if 1 <= choice <= 8:
                start_row = (choice - 1) * 10 + 1
                end_row = start_row + 9
                
                print(f"\n--- Booking Status (Rows {start_row}-{end_row}) ---")
                
                # Display Front Section (Rows start_row to end_row, Columns A-C)
                print(f"\nFront Section (Rows {start_row}-{end_row}, Columns A-C):")
                for row in range(start_row, end_row + 1):
                    row_display = ""
                    for col in front_columns:
                        seat_id = str(row) + col
                        row_display += f"{seat_id}({seats[seat_id]})  "
                    print(row_display)
                
                # Display aisle separator
                print("\nAisle:")
                print("X   X   X")
                
                # Display Rear Section (Rows start_row to end_row, Columns D-F)
                print(f"\nRear Section (Rows {start_row}-{end_row}, Columns D-F):")
                for row in range(start_row, end_row + 1):
                    row_display = ""
                    for col in rear_columns:
                        seat_id = str(row) + col
                        row_display += f"{seat_id}({seats[seat_id]})  "
                    print(row_display)
                print()  # Blank line for improved readability
            else:
                print("Invalid choice. Please select a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def main_menu():
    """
    Main menu loop that displays options and handles user selections.
    The menu remains until the user chooses to exit the program.
    """
    while True:
        print("===== Apache Airlines Seat-Booking System =====")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            show_booking_status()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")
        print()  # Blank line for visual separation

# --------------------------
# Entry Point of the Program
# --------------------------
if __name__ == "__main__":
    # Initialize database connection and create bookings table.
    init_db()
    # Load any existing bookings from the database into the in-memory seats dictionary.
    load_existing_bookings()
    # Start the main application loop.
    main_menu()
    # Close the database connection when the program exits.
    conn.close()
