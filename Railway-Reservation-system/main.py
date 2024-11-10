import mysql.connector
import random
from datetime import datetime


class Railway:
    """
    This class is used to interact with the Railway Reservation System database.
    """
    def __init__(self):
        """
        Connects to the Railway database and initializes the current user as None.
        """
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1#@Saichand',
            database='Railway'
        )
        self.cursor = self.connection.cursor()
        self.current_user = None

    def get_train_details(self):
        """
        Retrieves train details from the database.

        Returns a dictionary in the following format:
        {
            <train_number>: {
                'name': <train_name>,
                'arrival_time': <arrival_time>,
                'departure_time': <departure_time>,
                <class_name>: {
                    'seats': <number_of_seats>,
                    'fare': <fare_of_class>
                }
            }
        }
        """
        trains = {}
        self.cursor.execute("SELECT * FROM trains")
        for train in self.cursor.fetchall():
            train_number = train[0]
            trains[train_number] = {
                'name': train[1],
                'arrival_time': (datetime.min + train[2]).time().strftime('%H:%M'),
                'departure_time': (datetime.min + train[3]).time().strftime('%H:%M'),
                'day_of_train': train[4]
            }
            self.cursor.execute("SELECT * FROM train_classes WHERE train_number = %s", (train_number,))
            for class_data in self.cursor.fetchall():
                # class_data[1] is the class name
                # class_data[2] is the number of seats
                # class_data[3] is the fare of the class
                trains[train_number][class_data[1]] = {'seats': class_data[2], 'fare': float(class_data[3])}
        return trains



    def register_user(self, username, password, mobile_number, hometown):
        """
        Registers a new user into the Railway Reservation System.

        Parameters:
        username (str): The username of the user
        password (str): The password of the user
        mobile_number (str): The mobile number of the user
        hometown (str): The hometown of the user

        Returns:
        str: The user ID of the newly registered user
        """
        user_id = str(random.randint(10000, 99999))
        sql = "INSERT INTO users (user_id, username, password, mobile_number, hometown) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, username, password, mobile_number, hometown)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print(f'User Registered with User ID: {user_id}')
        return user_id

    def login(self, user_id, password):
        """
        Authenticates a user with the given user ID and password.

        Parameters:
        user_id (str): The user ID of the user attempting to log in.
        password (str): The password of the user.

        Returns:
        bool: True if login is successful, False otherwise.
        """
        # SQL query to fetch user details based on user_id and password
        sql = "SELECT * FROM users WHERE user_id = %s AND password = %s"
        val = (user_id, password)

        # Execute the SQL query
        self.cursor.execute(sql, val)

        # Fetch one user record
        user = self.cursor.fetchone()

        # Check if a user record was found
        if user:
            # Set the current user and display a welcome message
            self.current_user = user_id
            print(f"\nWELCOME, {user[1]}\n")
            return True
        else:
            # Inform the user of incorrect credentials
            print('User ID or Password incorrect. Please try again')
            return False

    def book_tickets(self, source_station, destination_station, day_of_travel, ticket_class):
        """
        Books a ticket for the given source station, destination station, travel date and class.

        Parameters:
        source_station (str): The source station of the journey.
        destination_station (str): The destination station of the journey.
        day_of_travel (str): The travel date in the "YYYY-MM-DD" format.
        ticket_class (str): The class of the ticket (1AC, 2AC, SL).

        Returns:
        None
        """
        if self.current_user:
            # Check the availability of the ticket class
            selected_train_number = self.check_seat_availability(ticket_class)
            if selected_train_number:
                # Generate a unique PNR number
                pnr_number = str(random.randint(100000, 999999))
                trains = self.get_train_details()
                fare = trains[selected_train_number][ticket_class]['fare']
                train_details = trains[selected_train_number]
                travel_date = datetime.strptime(day_of_travel, "%Y-%m-%d")
                try:
                    # Insert the booking into the bookings table
                    sql = '''
                    INSERT INTO bookings(user_id, source_station, destination_station, day_of_travel,
                    ticket_class, train_number, pnr_number, fare, arrival_time, departure_time)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    val = (self.current_user, source_station, destination_station, day_of_travel, ticket_class,
                           selected_train_number, pnr_number, fare, train_details['arrival_time'],
                           train_details['departure_time'])
                    self.cursor.execute(sql, val)
                    self.connection.commit()
                    self.update_seat_count(selected_train_number, ticket_class, -1)
                    # Print the ticket details
                    print("\n######################### Ticket Details ########################")
                    print(f"PNR Number: {pnr_number}")
                    print(f"Train Number: {selected_train_number}")
                    print(f"Train Name: {train_details['name']}")
                    print(f"Class: {ticket_class}")
                    print(f"Fare: {fare}")
                    print(f"Source Station: {source_station}")
                    print(f"Destination Station: {destination_station}")
                    print(f"Arrival Time: {train_details['arrival_time']}")
                    print(f"Departure Time: {train_details['departure_time']}")
                    print(f"Day of Travel: {travel_date.strftime('%Y-%m-%d')}")
                    print("########################## Safe Journey ##########################")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            else:
                print('Select the valid train number.\n')
        else:
            print("Please login first")

    def check_seat_availability(self, ticket_class):
        """
        Checks the seat availability for the provided ticket class.

        Parameters:
        ticket_class (str): The class of the ticket (e.g., 1AC, 2AC, SL).

        Returns:
        str or bool: The selected train number if available, otherwise False.
        """
        # Ensure the user is logged in
        if not self.current_user:
            print('Please login first')
            return False

        print("Available Trains:")
        available_trains = []

        # Retrieve train details
        trains = self.get_train_details()

        # Check availability of seats in each train
        for train_number, train_details in trains.items():
            if train_details[ticket_class]['seats'] > 0:
                print(f'''
                Train Number: {train_number}
                Train Name: {train_details['name']}
                Seats Available: {train_details[ticket_class]['seats']}
                Fare: {train_details[ticket_class]['fare']}''')
                available_trains.append(train_number)

        # If no trains have available seats, return False
        if not available_trains:
            print(f"No available trains for {ticket_class} class. \n")
            return False

        # Prompt user to select a train number
        selected_train_number = input("Enter the Train Number from the above list: ")

        # Validate the selected train number
        if selected_train_number not in available_trains:
            print("Invalid Train Number.")
            return False

        return selected_train_number

    def check_previous_bookings(self):
        """
        Displays the previous bookings of the current user.
        """
        if self.current_user:
            # Retrieve the bookings of the current user
            sql = "SELECT * FROM bookings WHERE user_id = %s"
            val = (self.current_user,)
            self.cursor.execute(sql, val)
            user_bookings = self.cursor.fetchall()

            if user_bookings:
                print("\n--------------------- Your Previous Bookings ---------------------------")
                # Iterate over the user bookings and print the details of each booking
                for booking in user_bookings:
                    print(f"PNR Number: {booking[7]}")
                    print(f"Train Number: {booking[6]}")
                    print(f"Source Station: {booking[2]}")
                    print(f"Destination Station: {booking[3]}")
                    print(f"Travel Date: {booking[4]}")
                    print(f"Class: {booking[5]}")
                    print(f"Fare: {booking[8]}")
                    print(f"Arrival Time: {booking[9]}")
                    print(f"Departure Time: {booking[10]}")
                    print('------------------------------------------------------------------')
                print("======================= End of Bookings ============================")
            else:
                print("You have no previous bookings.\n")
        else:
            print("Please login first")

    def check_pnr(self, pnr_number):
        """
        Checks and displays the booking details associated with a given PNR number.

        Parameters:
        pnr_number (str): The PNR number of the booking to check.

        Returns:
        None
        """
        # Prepare SQL query to fetch booking details based on PNR number
        sql = "SELECT * FROM bookings WHERE pnr_number = %s"
        val = (pnr_number,)

        # Execute the SQL query
        self.cursor.execute(sql, val)

        # Fetch the booking details
        booking = self.cursor.fetchone()

        # Check if the booking exists
        if booking:
            # Print the booking details
            print("\n======================== PNR Details =======================================")
            print(f"PNR Number: {booking[7]}")
            print(f"Train Number: {booking[6]}")
            print(f"Source Station: {booking[2]}")
            print(f"Destination Station: {booking[3]}")
            print(f"Travel Date: {booking[4]}")
            print(f"Class: {booking[5]}")
            print(f"Fare: {booking[8]}")
            print(f"Arrival Time: {booking[9]}")
            print(f"Departure Time: {booking[10]}")
            print("========================= End of PNR Details =================================")
        else:
            # Inform the user that the PNR number is invalid
            print('Invalid PNR Number.\n')

    def cancel_ticket(self, pnr_number):
        """
        Cancels a booking based on the given PNR number, provided the user is logged in.

        Parameters:
        pnr_number (str): The PNR number of the booking to cancel.

        Returns:
        None
        """
        if self.current_user:
            # Prepare SQL query to fetch booking details based on PNR number and user ID
            sql = "SELECT * FROM bookings WHERE pnr_number = %s AND user_id = %s"
            val = (pnr_number, self.current_user)

            # Execute the SQL query
            self.cursor.execute(sql, val)

            # Fetch the booking details
            booking = self.cursor.fetchone()

            # Check if the booking exists
            if booking:
                # Retrieve the train number and ticket class from the booking details
                train_number = booking[6]
                ticket_class = booking[5]

                # Prepare SQL query to delete the booking
                sql = "DELETE FROM bookings WHERE pnr_number = %s"
                val = (pnr_number,)

                # Execute the SQL query
                self.cursor.execute(sql, val)

                # Commit the changes to the database
                self.connection.commit()

                # Increase the seat count for the ticket class in the train
                self.update_seat_count(train_number, ticket_class, 1)

                # Print success message
                print("Booking Cancelled Successfully")
            else:
                # Inform the user of the invalid PNR number
                print("Invalid PNR number or you don't have permission to cancel the ticket")
        else:
            # Inform the user that they need to log in first
            print("Please login first")

    def update_seat_count(self, train_number, ticket_class, change):
        """
        Updates the seat count for the given train number and ticket class by the given change.

        Parameters:
        train_number (str): The train number of the train to update.
        ticket_class (str): The ticket class to update.
        change (int): The number of seats to increase or decrease.
        """
        # Prepare SQL query to update the seat count
        sql = "UPDATE train_classes SET seats = seats + %s WHERE train_number = %s AND class_name = %s"
        val = (change, train_number, ticket_class)

        # Execute the SQL query
        self.cursor.execute(sql, val)

        # Commit the changes to the database
        self.connection.commit()

# The main function remains the same as in your original code

def main():
    railway_system = Railway()
    print("---------------------------- Welcome to Railway Reservation System -----------------------")
    print('------------------------------------------------------------------------------------------\n')

    while True:
        print("Choose one of the following options: ")
        print("1. Book Tickets")
        print("2. Cancel Tickets")
        print("3. Check PNR")
        print("4. Check Seat Availability")
        print("5. Create New Account")
        print("6. Check Previous Bookings")
        print("7. Login")
        print("8. Exit")
        print('\n')

        option = input('Enter your option: ')

        if option == '1':
            if not railway_system.current_user:
                user_id = input('Enter Your User ID: ')
                password = input('Enter Your Password: ')
                if not railway_system.login(user_id, password):
                    print('Login Failed. Please try again')
                    continue
            railway_system.book_tickets(
                input("Enter Source Station: "),
                input("Enter Destination Station: "),
                input("Enter Travel Date in (YYYY-MM-DD) Format: "),
                input("Select Ticket Class (1AC, 2AC, SL): ").upper()
            )
        elif option == '2':
            railway_system.cancel_ticket(input("Enter your PNR number: "))
        elif option == '3':
            railway_system.check_pnr(input("Enter your PNR number: "))
        elif option == '4':
            ticket_class = input("Enter Ticket Class (1AC, 2AC, SL): ")
            if railway_system.check_seat_availability(ticket_class):
                print(f"Seats available for {ticket_class} Class\n")
            else:
                print(f"No Seats Available for {ticket_class} Class\n")
        elif option == '5':
            user_id = railway_system.register_user(
                input("Enter Your Username: "),
                input("Enter Your Password: "),
                input("Enter Your Mobile Number: "),
                input("Enter Your Hometown: ")
            )
            print(f"Account created successfully! Your User ID is {user_id}")
        elif option == '6':
            railway_system.check_previous_bookings()
        elif option == '7':
            user_id = input("Enter Your User ID: ")
            password = input("Enter Your Password: ")
            if not railway_system.login(user_id, password):
                print('Login Failed. Please try again')
        elif option == '8':
            print("Thank you for using the Railway Reservation System. Goodbye!")
            railway_system.connection.close() # Database connection closed
            break
        else:
            print("Invalid option selected. Please try again.")


# Call the main function when you want to run the application
main()
