import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="railway_db"
    )

# ...existing code...

def calculate_fare(distance, base_fare_per_km, concession_type=None):
    """
    Calculates the fare based on distance, base fare, and concession type.

    Args:
        distance (float): The distance of the journey in kilometers.
        base_fare_per_km (float): The base fare per kilometer.
        concession_type (str, optional): The type of concession requested. Defaults to None.

    Returns:
        float: The calculated fare after applying any applicable discount.
    """
    base_fare = distance * base_fare_per_km
    discount_percentage = 0.0

    if concession_type:
        concession_type = concession_type.lower() # Make comparison case-insensitive
        if concession_type == "senior citizen (male)":
            # Assuming age check happens elsewhere or is implied
            discount_percentage = 40.0
        elif concession_type == "senior citizen (female)":
            # Assuming age check happens elsewhere or is implied
            discount_percentage = 50.0
        elif concession_type == "student":
            discount_percentage = 25.0
        elif concession_type in ["disabled", "physically challenged"]: # Group similar discounts
            discount_percentage = 50.0
        elif concession_type == "armed forces":
            discount_percentage = 30.0
        elif concession_type == "war widow":
            discount_percentage = 75.0
        elif concession_type == "paramilitary forces":
            discount_percentage = 30.0
        elif concession_type == "patients":
            discount_percentage = 50.0
        elif concession_type == "press correspondents":
            discount_percentage = 50.0
        # Add more concession types here if needed

    discount_amount = base_fare * (discount_percentage / 100)
    final_fare = base_fare - discount_amount
    return final_fare

# ...existing code...

def book_ticket(user_id, train_id, source_station_id, destination_station_id, travel_date, num_passengers, concession_type=None):
    """
    Books a ticket for a user.

    Args:
        user_id (int): The ID of the user booking the ticket.
        train_id (int): The ID of the train.
        source_station_id (int): The ID of the source station.
        destination_station_id (int): The ID of the destination station.
        travel_date (str): The date of travel (YYYY-MM-DD).
        num_passengers (int): The number of passengers.
        concession_type (str, optional): The type of concession requested. Defaults to None.


    Returns:
        int or None: The booking ID if successful, None otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Get train details (including base fare rate if stored per train, or use a global rate)
        cursor.execute("SELECT base_fare_rate FROM Trains WHERE train_id = %s", (train_id,))
        train = cursor.fetchone()
        if not train:
            print("Error: Train not found.")
            return None
        # Assuming a base_fare_rate column exists in Trains table, otherwise use a default
        base_fare_per_km = train.get('base_fare_rate', 1.5) # Example default rate

        # 2. Get distance between stations (this might involve multiple steps or a dedicated function)
        # This is a simplified example; real distance calculation might be complex
        cursor.execute("""
            SELECT ABS(s1.distance_from_origin - s2.distance_from_origin) AS travel_distance
            FROM Stations s1, Stations s2
            WHERE s1.station_id = %s AND s2.station_id = %s
        """, (source_station_id, destination_station_id))
        distance_result = cursor.fetchone()
        if not distance_result or distance_result['travel_distance'] is None:
             # Fallback or alternative way to get distance if stations aren't on the same 'line'
             # For now, let's assume a fixed distance or handle error
             print("Error: Could not determine distance between stations.")
             # As a placeholder, let's query route segments if available
             cursor.execute("""
                 SELECT SUM(distance_to_next) as total_distance
                 FROM RouteSegments rs
                 JOIN Trains t ON rs.route_id = t.route_id
                 WHERE t.train_id = %s
                 AND rs.segment_order >= (SELECT segment_order FROM RouteSegments WHERE route_id = t.route_id AND station_id = %s LIMIT 1)
                 AND rs.segment_order < (SELECT segment_order FROM RouteSegments WHERE route_id = t.route_id AND station_id = %s LIMIT 1)
             """, (train_id, source_station_id, destination_station_id))
             distance_result = cursor.fetchone()
             if not distance_result or distance_result['total_distance'] is None:
                 print("Error: Could not determine distance via route segments.")
                 return None # Or handle appropriately
             distance = distance_result['total_distance']
        else:
            distance = distance_result['travel_distance']


        # 3. Check seat availability (complex logic, simplified here)
        # This needs a proper availability check based on date, train, source, dest, coach type etc.
        # Placeholder: Assume seats are available for now
        available_seats = 100 # Simplified
        if available_seats < num_passengers:
            print("Error: Not enough seats available.")
            return None

        # 4. Calculate fare using the updated function
        fare_per_passenger = calculate_fare(distance, base_fare_per_km, concession_type)
        total_fare = fare_per_passenger * num_passengers

        # 5. Insert booking record
        booking_status = "Confirmed" # Or "Pending Payment" etc.
        cursor.execute("""
            INSERT INTO Bookings (user_id, train_id, source_station_id, destination_station_id, travel_date, num_passengers, total_fare, booking_status, concession_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, train_id, source_station_id, destination_station_id, travel_date, num_passengers, total_fare, booking_status, concession_type))

        booking_id = cursor.lastrowid

        # 6. Update seat availability (decrement available seats)
        # This requires knowing which coach/seats were booked, highly simplified
        # update_seat_availability(train_id, travel_date, source_station_id, destination_station_id, num_passengers)


        conn.commit()
        print(f"Booking successful! Booking ID: {booking_id}, Total Fare: {total_fare:.2f}")
        return booking_id

    except mysql.connector.Error as err:
        print(f"Database error during booking: {err}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

# ...existing code...