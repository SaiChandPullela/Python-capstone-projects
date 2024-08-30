import mysql.connector
import random
from datetime import datetime

class Railway:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1#@Saichand',
            database='Railway'
        )
        self.cursor = self.connection.cursor()
        self.current_user = None

    def get_train_details(self):
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
                trains[train_number][class_data[1]] = {'seats': class_data[2], 'fare': float(class_data[3])}
        return trains

    def register_user(self, username, password, mobile_number, hometown):
        user_id = str(random.randint(10000, 99999))
        sql = "INSERT INTO users (user_id, username, password, mobile_number, hometown) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, username, password, mobile_number, hometown)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print(f'User Registered with User ID: {user_id}')
        return user_id

    def login(self, user_id, password):
        sql = "SELECT * FROM users WHERE user_id = %s AND password = %s"
        val = (user_id, password)
        self.cursor.execute(sql, val)
        user = self.cursor.fetchone()
        if user:
            self.current_user = user_id
            print(f"\nWELCOME, {user[1]}\n")
            return True
        else:
            print('User ID or Password incorrect. Please try again')
            return False

    def book_tickets(self, source_station, destination_station, day_of_travel, ticket_class):
        if self.current_user:
            selected_train_number = self.check_seat_availability(ticket_class)
            if selected_train_number:
                pnr_number = str(random.randint(100000, 999999))
                trains = self.get_train_details()
                fare = trains[selected_train_number][ticket_class]['fare']
                train_details = trains[selected_train_number]
                travel_date = datetime.strptime(day_of_travel, "%Y-%m-%d")
                sql = '''
                INSERT INTO bookings(user_id, source_station, destination_station, day_of_travel,
                ticket_class, train_number, pnr_number, fare, arrival_time, departure_time)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                val = (self.current_user, source_station, destination_station, day_of_travel, ticket_class,
                       selected_train_number, pnr_number, fare, train_details['arrival_time'],
                       train_details['departure_time'])
                try:
                    self.cursor.execute(sql, val)
                    self.connection.commit()
                    self.update_seat_count(selected_train_number, ticket_class, -1)
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
        if not self.current_user:
            print('Please login first')
            return False
        print("Available Trains:")
        available_trains = []
        trains = self.get_train_details()
        for train_number, train_details in trains.items():
            if train_details[ticket_class]['seats'] > 0:
                print(f'''
                Train Number: {train_number}
                Train Name: {train_details['name']}
                Seats Available: {train_details[ticket_class]['seats']}''')
                available_trains.append(train_number)
        if not available_trains:
            print(f"No available trains for {ticket_class} class. \n")
            return False
        selected_train_number = input("Enter the Train Number from the above list: ")
        if selected_train_number not in available_trains:
            print("Invalid Train Number.")
            return False
        return selected_train_number

    def check_previous_bookings(self):
        if self.current_user:
            sql = "SELECT * FROM bookings WHERE user_id = %s"
            val = (self.current_user,)
            self.cursor.execute(sql, val)
            user_bookings = self.cursor.fetchall()
            if user_bookings:
                print("\n--------------------- Your Previous Bookings ---------------------------")
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
        sql = "SELECT * FROM bookings WHERE pnr_number = %s"
        val = (pnr_number,)
        self.cursor.execute(sql, val)
        booking = self.cursor.fetchone()
        if booking:
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
            print('Invalid PNR Number.\n')

    def cancel_ticket(self, pnr_number):
        if self.current_user:
            sql = "SELECT * FROM bookings WHERE pnr_number = %s AND user_id = %s"
            val = (pnr_number, self.current_user)
            self.cursor.execute(sql, val)
            booking = self.cursor.fetchone()
            if booking:
                train_number = booking[6]
                ticket_class = booking[5]
                sql = "DELETE FROM bookings WHERE pnr_number = %s"
                val = (pnr_number,)
                self.cursor.execute(sql, val)
                self.connection.commit()
                self.update_seat_count(train_number, ticket_class, 1)
                print("Booking Cancelled Successfully")
            else:
                print("Invalid PNR number or you don't have permission to cancel the ticket")
        else:
            print("Please login first")

    def update_seat_count(self, train_number, ticket_class, change):
        sql = "UPDATE train_classes SET seats = seats + %s WHERE train_number = %s AND class_name = %s"
        val = (change, train_number, ticket_class)
        self.cursor.execute(sql, val)
        self.connection.commit()

# The main function remains the same as in your original code

if __name__ == '__main__':
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
            break
        else:
            print("Invalid option selected. Please try again.")