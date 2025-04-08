# Python Seat-Booking Application for Apache Airlines
# -----------------------------------------------------
# This program simulates a seat booking system for an airline.
# The aircraft is divided into two sections:
# - Front Section: Rows 1 to 80 with columns A, B, C (all bookable)
# - Rear Section: Rows 1 to 80 with columns D, E, F 
# - Rows 77-78 in columns D, E, F represent storage areas ("S") and are not bookable.
# All bookable seats are initially free (represented by "F").
# When a seat is booked, its status changes to "R".
# The program displays a menu to allow the user to perform different operations until exit.

# Define the seating layout for the front and rear sections

# Front section: rows numbered 1 through 80 and columns A, B, C.
front_rows = range(1, 81)          # Rows from 1 to 80 for the front section
front_columns = ['A', 'B', 'C']     # Columns A, B, C for the front section

# Rear section: same rows (1 to 80) but columns D, E, F.
rear_rows = range(1, 81)           # Rows from 1 to 80 for the rear section
rear_columns = ['D', 'E', 'F']      # Columns D, E, F for the rear section

# Create a dictionary to store the status of each seat.
# The keys are seat identifiers (e.g., "1A", "3B") and the values represent:
#   "F" for free, "R" for reserved, and "S" for storage (non-bookable).
seats = {}

# Initialize all front section seats as free ("F")
for row in front_rows:
    for col in front_columns:
        seat_id = str(row) + col          # Create seat ID, e.g., "1A"
        seats[seat_id] = "F"                # Mark seat as free

# Initialize all rear section seats.
# Note: In rows 77 and 78, seats in the rear section are marked as storage ("S") and are not bookable.
for row in rear_rows:
    for col in rear_columns:
        seat_id = str(row) + col          # Create seat ID, e.g., "77D"
        if row in [77, 78]:
            seats[seat_id] = "S"          # Mark storage seats as "S"
        else:
            seats[seat_id] = "F"          # All other seats are free ("F")

def check_availability():
    """
    Checks if a specified seat is available for booking.
    Prompts the user to input a seat number.
    Displays whether the seat is free, already reserved, or not bookable.
    """
    seat_id = input("Enter the seat number (e.g., 1A, 3D): ").upper()  # Convert input to uppercase to match keys
    if seat_id in seats:                         # Validate if the seat exists
        status = seats[seat_id]
        if status == "F":
            print(f"Seat {seat_id} is free and available for booking.")
        elif status == "R":
            print(f"Seat {seat_id} is already booked.")
        elif status == "S":
            print(f"Seat {seat_id} is a storage area and cannot be booked.")
    else:
        print("Invalid seat number. Please try again.")

def book_seat():
    """
    Books a specified seat if it is free.
    Prompts the user to input the seat number to book.
    Changes the seat status from free ("F") to reserved ("R") if available.
    """
    seat_id = input("Enter the seat number to book (e.g., 1A, 3D): ").upper()
    if seat_id in seats:                         # Check if seat exists in the seating layout
        status = seats[seat_id]
        if status == "F":                        # Only free seats can be booked
            seats[seat_id] = "R"                 # Update the seat's status to reserved
            print(f"Seat {seat_id} has been successfully booked.")
        elif status == "R":
            print(f"Seat {seat_id} is already booked.")
        elif status == "S":
            print(f"Seat {seat_id} is a storage area and cannot be booked.")
    else:
        print("Invalid seat number. Please try again.")

def free_seat():
    """
    Frees a booked seat.
    Prompts the user to input the seat number to free.
    Only seats that have been booked ("R") can be freed to become available ("F").
    """
    seat_id = input("Enter the seat number to free (e.g., 1A, 3D): ").upper()
    if seat_id in seats:                         # Validate if seat exists
        status = seats[seat_id]
        if status == "R":                        # Can only free a seat that is currently booked
            seats[seat_id] = "F"                 # Change the seat status back to free
            print(f"Seat {seat_id} has been freed and is now available.")
        elif status == "F":
            print(f"Seat {seat_id} is already free.")
        elif status == "S":
            print(f"Seat {seat_id} is a storage area and cannot be freed.")
    else:
        print("Invalid seat number. Please try again.")

def show_booking_status():
    """
    Displays the current booking status of the aircraft seating.
    Organizes the display by grouping rows (10 at a time) and separating 
    the front and rear sections with an aisle in between.
    """
    while True:
        # Show selection menu for rows to display
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
        if choice == '9':                       # Option to return to the main menu
            return
        
        try:
            choice = int(choice)
            if 1 <= choice <= 8:
                # Calculate start and end rows for the selected grouping
                start_row = (choice - 1) * 10 + 1
                end_row = start_row + 9
                
                print(f"\n--- Booking Status (Rows {start_row}-{end_row}) ---")
                
                # Display the front section seats for the selected rows
                print(f"\nFront Section (Rows {start_row}-{end_row}, Columns A-C):")
                for row in range(start_row, end_row + 1):
                    row_display = ""
                    for col in front_columns:
                        seat_id = str(row) + col      # Construct seat ID
                        # Display each seat and its current status (F, R, or S)
                        row_display += f"{seat_id}({seats[seat_id]})  "
                    print(row_display)
                
                # Print an aisle separator between front and rear sections
                print("\nAisle:")
                print("X   X   X")
                
                # Display the rear section seats for the selected rows
                print(f"\nRear Section (Rows {start_row}-{end_row}, Columns D-F):")
                for row in range(start_row, end_row + 1):
                    row_display = ""
                    for col in rear_columns:
                        seat_id = str(row) + col      # Construct seat ID
                        # Display each seat and its current status
                        row_display += f"{seat_id}({seats[seat_id]})  "
                    print(row_display)
                print()  # Blank line for better readability after printing a block
            else:
                print("Invalid choice. Please select a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def main_menu():
    """
    Displays the main menu for the seat-booking system and processes the user’s selection.
    Loops continuously until the user decides to exit the program.
    """
    while True:
        print("===== Apache Airlines Seat-Booking System =====")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")
        choice = input("Enter your choice (1-5): ")
        
        # Route the user's choice to the appropriate function
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
        print()  # Blank line added for better visual separation between operations

# Entry point of the program
if __name__ == "__main__":
    # Start the main menu loop when the script is run directly.
    main_menu()
# The program will continue to run until the user chooses to exit.