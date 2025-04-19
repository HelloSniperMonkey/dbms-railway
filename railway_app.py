import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import random
import string

flag = False
# Database connection function
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="railway",
            password="Railway@123",  # Change this to your actual MySQL password
            database="railway"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Generate PNR function
def generate_pnr():
    return ''.join(random.choices(string.digits, k=6))

# Function to get all train names and IDs (already exists, ensure it's accessible)
def get_all_trains():
    trains = {}
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT train_id, train_name FROM train ORDER BY train_name")
            result = cursor.fetchall()
            trains = {row[1]: row[0] for row in result} # Map name to ID
            cursor.close()
            conn.close()
        else:
            st.error("Could not connect to database to fetch trains.")
    except Exception as e:
        st.error(f"Error fetching trains: {e}")
    return trains

# Function to get all class names and IDs
def get_classes():
    classes = {}
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT class_id, class_name FROM class ORDER BY class_name")
            result = cursor.fetchall()
            # Map UI-friendly names if needed, or use DB names directly
            class_name_mapping_ui = { # Optional: Map DB names to UI names if different
                "First Class": "AC First Class (1A)",
                "AC 2-tier": "AC 2-Tier (2A)",
                "AC 3-tier": "AC 3-Tier (3A)",
                "Sleeper": "Sleeper (SL)",
                "Second Sitting": "Second Sitting (2S)",
                "AC Chair Car": "AC Chair Car",
                "Executive Class": "Executive Class"
            }
            classes = {class_name_mapping_ui.get(row[1], row[1]): row[0] for row in result} # Map UI name to ID
            cursor.close()
            conn.close()
        else:
            st.error("Could not connect to database to fetch classes.")
    except Exception as e:
        st.error(f"Error fetching classes: {e}")
    return classes

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'selected_train' not in st.session_state:
    st.session_state.selected_train = ""
if 'selected_class' not in st.session_state:
    st.session_state.selected_class = "AC First Class (1A)"
if 'from_station' not in st.session_state:
    st.session_state.from_station = ""
if 'to_station' not in st.session_state:
    st.session_state.to_station = ""
if 'journey_date' not in st.session_state:
    st.session_state.journey_date = datetime.now().date()
if 'trains_df' not in st.session_state:
    st.session_state.trains_df = None
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# App title
st.title("Indian Railway Ticket Reservation System")

# Sidebar navigation with buttons instead of dropdown
with st.sidebar:
    st.header("Navigation")
    
    if st.button("Login", key="nav_login", use_container_width=True):
        st.session_state.page = "Login"
        st.rerun()
        
    if st.button("Train Search", key="nav_search", use_container_width=True):
        st.session_state.page = "Train Search"
        st.rerun()
        
    if st.button("Booking", key="nav_booking", use_container_width=True):
        st.session_state.page = "Booking"
        st.rerun()
        
    if st.button("PNR Status", key="nav_pnr", use_container_width=True):
        st.session_state.page = "PNR Status"
        st.rerun()
        
    # Add Train Schedule button
    if st.button("Train Schedule", key="nav_schedule", use_container_width=True):
        st.session_state.page = "Train Schedule"
        st.rerun()
        
    # Add Seat Availability button
    if st.button("Seat Availability", key="nav_availability", use_container_width=True):
        st.session_state.page = "Seat Availability"
        st.rerun()
        
    # Add Passenger List button
    if st.button("Passenger List", key="nav_passenger_list", use_container_width=True):
        st.session_state.page = "Passenger List"
        st.rerun()
        
    # Add Busiest Routes button
    if st.button("Busiest Routes", key="nav_busiest_routes", use_container_width=True):
        st.session_state.page = "Busiest Routes"
        st.rerun()
        
    # Add Revenue Report button
    if st.button("Revenue Report", key="nav_revenue_report", use_container_width=True):
        st.session_state.page = "Revenue Report"
        st.rerun()
        
    if st.button("Cancellation", key="nav_cancel", use_container_width=True):
        st.session_state.page = "Cancellation"
        st.rerun()
        
    if st.button("My Bookings", key="nav_mybookings", use_container_width=True):
        st.session_state.page = "My Bookings"
        st.rerun()

# Content based on selected page
if st.session_state.page == "Login":
    st.header("User Login")
    
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    
    # Instead of using columns, use container and alignment
    login_col, register_col = st.columns([1, 1])
    
    with login_col:
        if st.button("Login", use_container_width=True):
            # Authentication logic remains the same
            if login_username == "user" and login_password == "password":
                st.session_state.logged_in = True
                st.session_state.user_id = 1001
                st.session_state.username = login_username
                st.session_state.role = "passenger"
                st.success("Login successful!")
            elif login_username == "admin" and login_password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_id = 9001
                st.session_state.username = login_username
                st.session_state.role = "admin"
                st.success("Admin login successful!")
            else:
                st.error("Invalid username or password")
    
    with register_col:
        if st.button("Register New User", use_container_width=True):
            st.info("Registration functionality would be implemented here")

# Train Search page
elif st.session_state.page == "Train Search":
    st.header("Search Trains")
    
    # Initialize search_performed in session state if not present
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    
    # Get stations from database for dropdowns
    def get_stations():
        try:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT station_id, station_name, station_code, city, state FROM station ORDER BY station_name;')
                result = cursor.fetchall()
                stations = [(row[0], f"{row[1]} ({row[2]}) - {row[3]}, {row[4]}") for row in result]
                cursor.close()
                conn.close()
                return stations
            else:
                st.error("Could not connect to database")
                return []
        except Exception as e:
            st.error(f"Error fetching stations: {e}")
            return []
    
    # Get available stations for dropdowns
    stations = get_stations()
    station_names = [station[1] for station in stations]
    station_ids = [station[0] for station in stations]
    station_dict = dict(zip(station_names, station_ids))
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_station = st.selectbox("From Station", station_names)
    
    with col2:
        to_station = st.selectbox("To Station", station_names)
    
    journey_date = st.date_input("Journey Date", min_value=datetime.now().date())
    
    # Update session state with the station selections and date
    st.session_state.from_station = from_station
    st.session_state.to_station = to_station
    st.session_state.journey_date = journey_date

    if st.button("Search Trains"):
        st.session_state.search_performed = True
        if from_station != to_station:
            # Get source and destination station IDs
            source_id = station_dict[from_station]
            destination_id = station_dict[to_station]
            
            # Query database for trains between these stations
            try:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    # Query to get trains between the selected stations
                    query = """
                    SELECT t.train_id, t.train_name, t.train_type, t.total_seats,
                           s1.station_name as source_station, s2.station_name as destination_station
                    FROM train t
                    JOIN station s1 ON t.source_station_id = s1.station_id
                    JOIN station s2 ON t.destination_station_id = s2.station_id
                    WHERE (t.source_station_id = %s AND t.destination_station_id = %s)
                       OR (t.source_station_id = %s AND t.destination_station_id = %s)
                    """
                    cursor.execute(query, (source_id, destination_id, destination_id, source_id))
                    result = cursor.fetchall()
                    
                    if result:
                        # Create DataFrame from results
                        trains_df = pd.DataFrame(result, columns=['Train ID', 'Train Name', 'Train Type', 'Total Seats', 
                                                                 'Source Station', 'Destination Station'])
                        
                        # Add some sample departure/arrival times and available seats
                        # In a real app, you would get this from schedule and seat availability tables
                        trains_df['Departure'] = ['06:00', '08:30', '15:45', '23:55', '11:30'][:len(trains_df)]
                        trains_df['Arrival'] = ['14:30', '13:00', '06:30', '13:40', '00:45'][:len(trains_df)]
                        trains_df['Duration'] = ['8h 30m', '4h 30m', '14h 45m', '13h 45m', '13h 15m'][:len(trains_df)]
                        trains_df['Available Seats'] = [random.randint(10, 100) for _ in range(len(trains_df))]
                        
                        st.write(f"Showing trains from {from_station} to {to_station} on {journey_date}")
                        st.dataframe(trains_df[['Train ID', 'Train Name', 'Train Type', 'Departure', 'Arrival', 'Duration', 'Available Seats']])
                        
                        # Store trains_df in session state for reuse
                        st.session_state.trains_df = trains_df
                        
                    else:
                        st.warning("No trains found between these stations. Try different stations.")
                    
                    cursor.close()
                    conn.close()
                else:
                    st.error("Could not connect to database")
            except Exception as e:
                st.error(f"Error searching for trains: {e}")
        else:
            st.error("Source and destination stations cannot be the same")

    # Display train selection UI only once - either after search or for previous results
    if st.session_state.search_performed and 'trains_df' in st.session_state and st.session_state.trains_df is not None:
        # If we have previous search results, display them
        trains_df = st.session_state.trains_df
        
        # Define callback functions to update session state
        def update_selected_train():
            st.session_state.selected_train = st.session_state.train_select_key

        def update_selected_class():
            st.session_state.selected_class = st.session_state.class_select_key

        # If trains_df exists and is not empty
        if not trains_df.empty:
            # Use the callback to update session state
            train_names = trains_df['Train Name'].tolist()
            
            # Set default value for train selection if not already in session state
            if not st.session_state.selected_train or st.session_state.selected_train not in train_names:
                st.session_state.selected_train = train_names[0]
            
            # Create the selectbox with on_change callback - using unique keys
            selected_train = st.selectbox(
                "Select Train to Book", 
                train_names,
                index=train_names.index(st.session_state.selected_train),
                key="train_select_key",
                on_change=update_selected_train
            )
            
            # Class options with callback - using unique keys
            class_options = ["AC First Class (1A)", "AC 2-Tier (2A)", "AC 3-Tier (3A)", "Sleeper (SL)", "Second Sitting (2S)"]
            
            selected_class = st.selectbox(
                "Select Class", 
                class_options,
                index=class_options.index(st.session_state.selected_class),
                key="class_select_key", 
                on_change=update_selected_class
            )
            
            # Book button
            if st.button("Proceed to Booking"):
                if st.session_state.logged_in:
                    st.session_state.booking_train = st.session_state.selected_train
                    st.session_state.booking_class = st.session_state.selected_class
                    st.session_state.from_station = from_station
                    st.session_state.to_station = to_station
                    st.session_state.journey_date = journey_date
                    st.session_state.page = "Booking"
                    st.rerun()
                else:
                    st.warning("Please login first to book tickets")

# Booking page
elif st.session_state.page == "Booking":
    st.header("Book Tickets")
    
    if not st.session_state.logged_in:
        st.warning("Please login to book tickets")
    else:
        # Fetch stations and create station_dict for this page scope
        def get_stations(): # Define or ensure get_stations is accessible here
            try:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT station_id, station_name, station_code, city, state FROM station ORDER BY station_name;')
                    result = cursor.fetchall()
                    stations_data = [(row[0], f"{row[1]} ({row[2]}) - {row[3]}, {row[4]}") for row in result]
                    cursor.close()
                    conn.close()
                    return stations_data
                else:
                    st.error("Could not connect to database")
                    return []
            except Exception as e:
                st.error(f"Error fetching stations: {e}")
                return []
        
        stations = get_stations()
        station_names = [station[1] for station in stations]
        station_ids = [station[0] for station in stations]
        station_dict = dict(zip(station_names, station_ids)) # Define station_dict here

        calculated_base_fare = 0.0 # Initialize calculated base fare
        train_id = None
        class_id = None
        from_station_id = None
        to_station_id = None
        error_in_fare_calc = False

        # Check if we have booking info from train search
        if hasattr(st.session_state, 'booking_train'):
            st.info(f"Booking for: {st.session_state.booking_train} ({st.session_state.booking_class})")
            st.info(f"From {st.session_state.from_station} to {st.session_state.to_station}")
            st.info(f"Journey Date: {st.session_state.journey_date}")

            # --- Start: Fetch data for fare calculation ---
            try:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()

                    # Map UI class name to DB class name
                    class_name_mapping = {
                        "AC First Class (1A)": "First Class",
                        "AC 2-Tier (2A)": "AC 2-tier",
                        "AC 3-Tier (3A)": "AC 3-tier",
                        "Sleeper (SL)": "Sleeper",
                        "Second Sitting (2S)": "Second Sitting",
                        "AC Chair Car": "AC Chair Car",
                        "Executive Class": "Executive Class"
                    }
                    db_class_name = class_name_mapping.get(st.session_state.booking_class)

                    if not db_class_name:
                        st.error(f"Invalid class selected: {st.session_state.booking_class}")
                        error_in_fare_calc = True
                    else:
                        # 1. Get train_id and class_id
                        query_ids = """
                        SELECT t.train_id, c.class_id 
                        FROM train t, class c 
                        WHERE t.train_name = %s AND c.class_name = %s
                        LIMIT 1;
                        """
                        cursor.execute(query_ids, (st.session_state.booking_train, db_class_name))
                        id_result = cursor.fetchone()

                        if not id_result:
                            st.error(f"Could not find Train/Class ID for fare calculation.")
                            error_in_fare_calc = True
                        else:
                            train_id, class_id = id_result

                            # 2. Get station IDs
                            from_station_id = station_dict.get(st.session_state.from_station)
                            to_station_id = station_dict.get(st.session_state.to_station)

                            if not from_station_id or not to_station_id:
                                st.error("Could not resolve station IDs for fare calculation.")
                                error_in_fare_calc = True
                            else:
                                # 3. Get base_fare_per_km
                                query_base_fare = "SELECT base_fare_per_km FROM class WHERE class_id = %s"
                                cursor.execute(query_base_fare, (class_id,))
                                fare_result = cursor.fetchone()
                                if not fare_result:
                                    st.error("Could not find base fare for the selected class.")
                                    error_in_fare_calc = True
                                else:
                                    base_fare_per_km = float(fare_result[0]) # Ensure it's float

                                    # 4. Get distances
                                    query_distance = """
                                    SELECT station_id, distance_from_source 
                                    FROM route 
                                    WHERE train_id = %s AND station_id IN (%s, %s)
                                    """
                                    cursor.execute(query_distance, (train_id, from_station_id, to_station_id))
                                    distance_results = cursor.fetchall()

                                    if len(distance_results) != 2:
                                        st.error("Could not find route distance information for one or both stations.")
                                        error_in_fare_calc = True
                                    else:
                                        dist_map = {row[0]: float(row[1]) for row in distance_results} # Ensure float
                                        distance_from = dist_map.get(from_station_id)
                                        distance_to = dist_map.get(to_station_id)
                                        
                                        if distance_from is None or distance_to is None:
                                             st.error("Error retrieving distances from route.")
                                             error_in_fare_calc = True
                                        else:
                                            travel_distance = abs(distance_to - distance_from)
                                            calculated_base_fare = travel_distance * base_fare_per_km
                    
                    cursor.close()
                    conn.close()
                else:
                    st.error("Database connection failed during fare calculation.")
                    error_in_fare_calc = True
            except Exception as e:
                st.error(f"Error calculating fare: {e}")
                error_in_fare_calc = True
            # --- End: Fetch data for fare calculation ---

        else:
            st.warning("Please search and select a train first")
            st.stop() # Stop execution if no booking info is present
            
        # Passenger details
        st.subheader("Passenger Details")
        
        passenger_name = st.text_input("Full Name")
        
        col1, col2 = st.columns(2)
        with col1:
            passenger_age = st.number_input("Age", min_value=1, max_value=120, value=30)
        with col2:
            passenger_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        passenger_mobile = st.text_input("Mobile Number")
        passenger_email = st.text_input("Email")
        
        # Concession options
        has_concession = st.checkbox("Apply for Concession")
        
        concession_type = None # Initialize concession_type
        if has_concession:
            concession_type = st.selectbox("Concession Type", 
                                         ["Senior Citizen (Male)","Senior Citizen (Female)", "Student", "Disabled", "Armed Forces", "War Widow", "Paramilitary Forces", "Press Correspondents"])
            concession_id = st.text_input("Concession ID / Document Number")
        
        # Berth preference
        berth_preference = st.selectbox("Berth Preference", 
                                      ["No Preference", "Lower", "Middle", "Upper", "Side Lower", "Side Upper"])
        
        # Meals preference
        meals = st.checkbox("Opt for Meals")
        
        # Payment options
        st.subheader("Payment Details")
        
        if error_in_fare_calc:
             st.error("Cannot display fare details due to calculation error.")
        else:
            # Dynamically compute fare details based on calculated base fare and concession
            reservation_charge = 40.00 # Keep hardcoded or fetch if available
            superfast_charge = 45.00 # Keep hardcoded or fetch if available
            GST_rate = 5.00 # Keep hardcoded or fetch if available
            
            discount_mapping = {
                "senior citizen (male)": 40.0,
                "senior citizen (female)": 50.0,
                "student": 25.0,
                "disabled": 50.0,
                "armed forces": 30.0,
                "war widow": 75.0,
                "paramilitary forces": 30.0,
                "press correspondents": 50.0
            }
            
            discount_rate = 0.0
            # If concession is requested, obtain discount percentage (case-insensitive)
            if has_concession and concession_type: # Check if concession_type is not None
                discount_rate = discount_mapping.get(concession_type.lower(), 0.0)
            
            # Use calculated_base_fare here
            discount_amount = calculated_base_fare * (discount_rate / 100)
            effective_base_fare = calculated_base_fare - discount_amount
            fare_without_tax = effective_base_fare + reservation_charge + superfast_charge
            GST_amount = fare_without_tax * (GST_rate / 100)
            total_fare = fare_without_tax + GST_amount # This is the final fare to be paid and stored
            
            fare_details = {
                "Calculated Base Fare": f"₹ {calculated_base_fare:.2f}", # Show calculated base
                "Reservation Charges": f"₹ {reservation_charge:.2f}",
                "Superfast Charges": f"₹ {superfast_charge:.2f}",
            }
            if discount_amount > 0:
                 fare_details["Concession Discount"] = f"- ₹ {discount_amount:.2f}"
            
            fare_details.update({
                 "Fare after Concession": f"₹ {effective_base_fare:.2f}",
                 "GST (5%)": f"₹ {GST_amount:.2f}",
                 "Total Fare": f"₹ {total_fare:.2f}"
            })
            
            for item, amount in fare_details.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(item)
                with col2:
                    st.write(amount)
            
            payment_method = st.selectbox("Payment Method", 
                                        ["Credit/Debit Card", "Net Banking", "UPI", "Wallet"])
            
            if st.button("Proceed to Payment"):
                # Basic validation
                if not passenger_name or not passenger_mobile:
                     st.warning("Please fill in passenger name and mobile number.")
                # Check if IDs were fetched correctly earlier
                elif train_id is None or class_id is None or from_station_id is None or to_station_id is None:
                     st.error("Cannot proceed with booking due to missing train/class/station information.")
                else:
                    pnr = generate_pnr() # Generate PNR first
                    
                    insert_ticket_query = """
                    INSERT INTO ticket (pnr_number, train_id, class_id, passenger_id, from_station_id, to_station_id, journey_date, fare, concession_applied, status, seat_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    """ 
                    insert_passenger_query = """
                    INSERT INTO passenger (name, age, gender, mobile, email) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE passenger_id=LAST_INSERT_ID(passenger_id); 
                    """ 

                    try:
                        conn = connect_to_db()
                        if conn:
                            cursor = conn.cursor()
                            
                            # 1. Insert or get passenger_id (Moved from previous position)
                            cursor.execute(insert_passenger_query, (
                                passenger_name, passenger_age, passenger_gender, passenger_mobile, passenger_email
                            ))
                            passenger_id = cursor.lastrowid # Get the ID of the inserted or existing passenger
                            
                            # IDs (train_id, class_id, from_station_id, to_station_id) are already fetched above
                            
                            journey_date = st.session_state.journey_date
                            fare = total_fare # Use the final calculated total_fare
                            concession_amount_val = discount_amount # Use calculated discount amount
                            status = "Confirmed" # Assuming confirmed for now
                            seat_number = None # Placeholder

                            # 2. Insert ticket details into the database
                            cursor.execute(insert_ticket_query, (
                                "PNR"+pnr, train_id, class_id, passenger_id, 
                                from_station_id, to_station_id, journey_date, 
                                fare, concession_amount_val, status, seat_number
                            ))
                            conn.commit()
                            
                            cursor.close()
                            conn.close()
                            
                            st.success("Booking Successful!") 
                            st.info(f"Your PNR number is: PNR{pnr}")
                            st.info("Ticket details have been sent to your email (simulation).")
                            # Clear booking state after success
                            del st.session_state.booking_train
                            del st.session_state.booking_class
                            # st.session_state.page = "My Bookings" 
                            # st.rerun()

                        else:
                            st.error("Database connection failed. Please try again later.")
                    except Exception as e:
                        st.error(f"Error booking ticket: {e}")
                        # ... (error handling with rollback) ...
                        if conn and conn.is_connected():
                            conn.rollback()
                            cursor.close()
                            conn.close()

# PNR Status page
elif st.session_state.page == "PNR Status":
    st.header("Check PNR Status")
    
    pnr_number = st.text_input("Enter PNR Number")
    
    if st.button("Check Status"):
        if pnr_number:
            # Query the database for the PNR
            try:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    
                    # Query to get ticket information based on PNR number
                    ticket_query = """
                    SELECT 
                        t.ticket_id, t.pnr_number, t.journey_date, t.seat_number, t.status, t.fare,
                        tr.train_id, tr.train_name, tr.train_type,
                        c.class_name,
                        s1.station_name as from_station, s1.station_code as from_code,
                        s2.station_name as to_station, s2.station_code as to_code,
                        p.passenger_id, p.name as passenger_name, p.age, p.gender, 
                        IFNULL(t.concession_applied, 0) as concession_applied
                    FROM ticket t
                    JOIN train tr ON t.train_id = tr.train_id
                    JOIN class c ON t.class_id = c.class_id
                    JOIN station s1 ON t.from_station_id = s1.station_id
                    JOIN station s2 ON t.to_station_id = s2.station_id
                    JOIN passenger p ON t.passenger_id = p.passenger_id
                    WHERE t.pnr_number = %s
                    """
                    cursor.execute(ticket_query, (pnr_number,))
                    ticket_results = cursor.fetchall()
                    
                    if ticket_results:
                        st.success("PNR Found")
                        
                        # Get the first result for common ticket information
                        first_result = ticket_results[0]
                        
                        # Display ticket details
                        common_data = {
                            "PNR Number": first_result['pnr_number'],
                            "Train": first_result['train_name'],
                            "Train Type": first_result['train_type'],
                            "From": f"{first_result['from_station']} ({first_result['from_code']})",
                            "To": f"{first_result['to_station']} ({first_result['to_code']})",
                            "Date of Journey": first_result['journey_date'].strftime('%d-%b-%Y') if isinstance(first_result['journey_date'], datetime) else first_result['journey_date'],
                            "Class": first_result['class_name'],
                            "Status": first_result['status']
                        }
                        
                        # Display common ticket details
                        for field, value in common_data.items():
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.write(f"**{field}:**")
                            with col2:
                                st.write(value)
                        
                        # Display passenger details
                        st.subheader("Passenger Details")
                        for i, passenger in enumerate(ticket_results):
                            seat_info = f" ({passenger['seat_number']})" if passenger['seat_number'] else ""
                            passenger_status = f"{passenger['status']}{seat_info}"
                            st.write(f"**Passenger {i+1}:** {passenger['passenger_name']} ({passenger['age']}, {passenger['gender']}) - {passenger_status}")
                            
                            # Show concession details if applied
                            if passenger['concession_applied'] > 0:
                                st.write(f"   *Concession Applied: ₹{passenger['concession_applied']}*")
                        
                        # Display fare details
                        st.subheader("Fare Details")
                        total_fare = sum(p['fare'] for p in ticket_results)
                        total_concession = sum(p['concession_applied'] for p in ticket_results)
                        
                        st.write(f"**Base Fare:** ₹{total_fare + total_concession}")
                        if total_concession > 0:
                            st.write(f"**Concession Applied:** ₹{total_concession}")
                        st.write(f"**Final Fare:** ₹{total_fare}")
                        
                    else:
                        st.error(f"No ticket found with PNR number: {pnr_number}")
                    
                    cursor.close()
                    conn.close()
                else:
                    st.error("Database connection failed. Please try again later.")
            except Exception as e:
                st.error(f"Error retrieving ticket information: {e}")
        else:
            st.error("Please enter a valid PNR number")

# Train Schedule page (New Section)
elif st.session_state.page == "Train Schedule":
    st.header("Train Schedule Lookup")

    # Function to get all train names and IDs
    def get_all_trains():
        trains = {}
        try:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT train_id, train_name FROM train ORDER BY train_name")
                result = cursor.fetchall()
                trains = {row[1]: row[0] for row in result} # Map name to ID
                cursor.close()
                conn.close()
            else:
                st.error("Could not connect to database to fetch trains.")
        except Exception as e:
            st.error(f"Error fetching trains: {e}")
        return trains

    train_dict = get_all_trains()
    train_names = list(train_dict.keys())

    if not train_names:
        st.warning("No trains found in the database.")
    else:
        selected_train_name = st.selectbox("Select Train", train_names)

        if st.button("Get Schedule"):
            if selected_train_name:
                selected_train_id = train_dict.get(selected_train_name)
                if selected_train_id:
                    try:
                        conn = connect_to_db()
                        if conn:
                            cursor = conn.cursor(dictionary=True)
                            # Call the stored procedure GetTrainSchedule
                            cursor.callproc('GetTrainSchedule', (selected_train_id,))
                            
                            schedule_results = []
                            # Fetch results from the procedure call
                            for result in cursor.stored_results():
                                schedule_results.extend(result.fetchall())

                            if schedule_results:
                                st.subheader(f"Schedule for {selected_train_name} ({selected_train_id})")
                                schedule_df = pd.DataFrame(schedule_results)
                                # Format time columns if they exist
                                if 'arrival_time' in schedule_df.columns:
                                     schedule_df['arrival_time'] = schedule_df['arrival_time'].astype(str).replace('NaT', 'Starts')
                                if 'departure_time' in schedule_df.columns:
                                     schedule_df['departure_time'] = schedule_df['departure_time'].astype(str).replace('NaT', 'Ends')
                                
                                # Rename columns for better readability
                                schedule_df.rename(columns={
                                    'station_name': 'Station Name',
                                    'arrival_time': 'Arrival',
                                    'departure_time': 'Departure',
                                    'distance_from_source': 'Distance (km)'
                                }, inplace=True)
                                
                                st.dataframe(schedule_df[['Station Name', 'Arrival', 'Departure', 'Distance (km)']])
                            else:
                                st.warning(f"No schedule found for train: {selected_train_name}")
                            
                            cursor.close()
                            conn.close()
                        else:
                            st.error("Database connection failed.")
                    except Exception as e:
                        st.error(f"Error retrieving train schedule: {e}")
                else:
                    st.error("Could not find ID for the selected train.")
            else:
                st.error("Please select a train.")

# Seat Availability page (New Section)
elif st.session_state.page == "Seat Availability":
    st.header("Check Seat Availability")

    train_dict = get_all_trains()
    class_dict = get_classes()

    train_names = list(train_dict.keys())
    class_names = list(class_dict.keys())

    if not train_names or not class_names:
        st.warning("Could not fetch train or class data.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            selected_train_name = st.selectbox("Select Train", train_names)
        with col2:
            selected_class_name = st.selectbox("Select Class", class_names)

        journey_date = st.date_input("Journey Date", min_value=datetime.now().date())

        if st.button("Check Availability"):
            if selected_train_name and selected_class_name and journey_date:
                selected_train_id = train_dict.get(selected_train_name)
                selected_class_id = class_dict.get(selected_class_name)

                if selected_train_id and selected_class_id:
                    try:
                        conn = connect_to_db()
                        if conn:
                            cursor = conn.cursor(dictionary=True)
                            # Call the stored procedure CheckSeatAvailability
                            cursor.callproc('CheckSeatAvailability', (selected_train_id, selected_class_id, journey_date))

                            total_available = -1 # Default value if not found
                            available_seat_numbers = []

                            # Iterate through the results
                            results_iterator = cursor.stored_results()
                            
                            # First result set: Total available seats count
                            try:
                                first_result_set = next(results_iterator)
                                total_seats_result = first_result_set.fetchone()
                                if total_seats_result:
                                    total_available = total_seats_result.get('total_available_seats', 0)
                            except StopIteration:
                                st.warning("Could not retrieve total available seats count.")
                            except Exception as e:
                                st.error(f"Error processing first result set: {e}")

                            # Second result set: List of available seat numbers
                            try:
                                second_result_set = next(results_iterator)
                                available_seat_numbers = [row['seat_number'] for row in second_result_set.fetchall()]
                            except StopIteration:
                                # This might be expected if no specific seats are listed or only count is returned
                                pass 
                            except Exception as e:
                                st.error(f"Error processing second result set: {e}")


                            if total_available != -1:
                                st.success(f"Availability for {selected_train_name} ({selected_class_name}) on {journey_date}:")
                                st.metric(label="Total Available Seats", value=total_available)
                                
                                if available_seat_numbers:
                                     st.write(f"Count of specific available seats listed: {len(available_seat_numbers)}")
                                     # Optionally display a sample or all seats if the list isn't too long
                                     # st.write("Available Seat Numbers:", ", ".join(available_seat_numbers))
                                elif total_available > 0:
                                     st.info("Specific seat numbers are not listed, but seats are available based on the total count.")
                                else: # total_available is 0 or less
                                     st.warning("No seats available.")

                            else:
                                st.warning(f"Could not determine availability for the selected criteria.")

                            cursor.close()
                            conn.close()
                        else:
                            st.error("Database connection failed.")
                    except Exception as e:
                        st.error(f"Error checking seat availability: {e}")
                else:
                    st.error("Could not find ID for the selected train or class.")
            else:
                st.error("Please select a train, class, and journey date.")

# Passenger List page (New Section)
elif st.session_state.page == "Passenger List":
    st.header("Passenger List by Train and Date")

    # Optional: Add admin check later
    # if st.session_state.role != 'admin':
    #     st.warning("This feature is available for administrators only.")
    # else:

    train_dict = get_all_trains()
    train_names = list(train_dict.keys())

    if not train_names:
        st.warning("Could not fetch train data.")
    else:
        selected_train_name = st.selectbox("Select Train", train_names)
        journey_date = st.date_input("Journey Date", min_value=datetime.now().date() - timedelta(days=365), max_value=datetime.now().date() + timedelta(days=365)) # Allow past/future dates

        if st.button("Get Passenger List"):
            if selected_train_name and journey_date:
                selected_train_id = train_dict.get(selected_train_name)

                if selected_train_id:
                    try:
                        conn = connect_to_db()
                        if conn:
                            cursor = conn.cursor(dictionary=True)
                            # Call the stored procedure GetPassengersByTrain
                            cursor.callproc('GetPassengersByTrain', (selected_train_id, journey_date))

                            passenger_results = []
                            # Fetch results from the procedure call
                            for result in cursor.stored_results():
                                passenger_results.extend(result.fetchall())

                            if passenger_results:
                                st.subheader(f"Confirmed Passengers for {selected_train_name} on {journey_date}")
                                passenger_df = pd.DataFrame(passenger_results)
                                
                                # Rename columns for better readability
                                passenger_df.rename(columns={
                                    'name': 'Passenger Name',
                                    'age': 'Age',
                                    'gender': 'Gender',
                                    'class_name': 'Class',
                                    'seat_number': 'Seat',
                                    'from_station': 'From',
                                    'to_station': 'To'
                                }, inplace=True)
                                
                                st.dataframe(passenger_df[['Passenger Name', 'Age', 'Gender', 'Class', 'Seat', 'From', 'To']])
                            else:
                                st.info(f"No confirmed passengers found for {selected_train_name} on {journey_date}.")
                            
                            cursor.close()
                            conn.close()
                        else:
                            st.error("Database connection failed.")
                    except Exception as e:
                        st.error(f"Error retrieving passenger list: {e}")
                else:
                    st.error("Could not find ID for the selected train.")
            else:
                st.error("Please select a train and journey date.")

# Busiest Routes page (Modified Section)
elif st.session_state.page == "Busiest Routes":
    st.header("Overall Busiest Routes") # Updated header

    # Optional: Add admin check later
    # if st.session_state.role != 'admin':
    #     st.warning("This feature is available for administrators only.")
    # else:

    # Removed date inputs and button
    # Logic now runs directly on page load

    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Query to get all confirmed tickets with source and destination station names
            query = """
            SELECT 
                s1.station_name AS source_station, 
                s2.station_name AS destination_station
            FROM ticket t
            JOIN station s1 ON t.from_station_id = s1.station_id
            JOIN station s2 ON t.to_station_id = s2.station_id
            WHERE t.status = 'Confirmed'; 
            """
            cursor.execute(query)
            all_tickets = cursor.fetchall()

            if all_tickets:
                # Use pandas to calculate busiest routes
                tickets_df = pd.DataFrame(all_tickets)
                
                # Group by source and destination and count occurrences
                busiest_routes = tickets_df.groupby(['source_station', 'destination_station']).size().reset_index(name='passenger_count')
                
                # Sort by passenger count descending and get top 5
                top_routes = busiest_routes.sort_values(by='passenger_count', ascending=False)

                if not top_routes.empty:
                    st.subheader("Top 5 Busiest Routes (Overall)")
                    # Rename columns for display
                    top_routes.rename(columns={
                        'source_station': 'Source Station',
                        'destination_station': 'Destination Station',
                        'passenger_count': 'Total Passenger Count'
                    }, inplace=True)
                    st.dataframe(top_routes[['Source Station', 'Destination Station', 'Total Passenger Count']])
                else:
                     st.info("No confirmed booking data found to determine busiest routes.")

            else:
                st.info("No confirmed booking data found.")
            
            cursor.close()
            conn.close()
        else:
            st.error("Database connection failed.")
    except Exception as e:
        st.error(f"Error retrieving or processing busiest routes: {e}")

# Revenue Report page (Modified Section)
elif st.session_state.page == "Revenue Report":
    st.header("Revenue Report")

    # Optional: Add admin check later
    # if st.session_state.role != 'admin':
    #     st.warning("This feature is available for administrators only.")
    # else:

    # Adjust default dates to match sample data (May 2023)
    default_start_date = datetime(2023, 5, 1).date()
    default_end_date = datetime(2023, 5, 31).date()

    col1, col2 = st.columns(2)
    with col1:
        # Remove max_value constraint tied to today
        start_date = st.date_input("Start Date", value=default_start_date) 
    with col2:
        # Remove min_value and max_value constraints tied to start_date/today
        end_date = st.date_input("End Date", value=default_end_date) 

    if st.button("Generate Report"):
        if start_date > end_date:
            st.error("Error: Start date cannot be after end date.")
        else:
            try:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    # Call the stored procedure GenerateRevenueReport
                    cursor.callproc('GenerateRevenueReport', (start_date, end_date))

                    results_iterator = cursor.stored_results()
                    total_revenue = 0
                    revenue_by_mode = pd.DataFrame()
                    revenue_by_train = pd.DataFrame()
                    found_data = False

                    # Process first result set: Total Revenue
                    try:
                        first_result_set = next(results_iterator)
                        total_revenue_result = first_result_set.fetchone()
                        if total_revenue_result and total_revenue_result['total_revenue'] is not None:
                            total_revenue = float(total_revenue_result['total_revenue'])
                            found_data = True
                    except StopIteration:
                        pass # No result sets returned
                    except Exception as e:
                        st.error(f"Error processing total revenue: {e}")

                    # Process second result set: Revenue by Payment Mode
                    try:
                        second_result_set = next(results_iterator)
                        mode_results = second_result_set.fetchall()
                        if mode_results:
                            revenue_by_mode = pd.DataFrame(mode_results)
                            # Convert decimal to float for display
                            revenue_by_mode['mode_revenue'] = revenue_by_mode['mode_revenue'].astype(float)
                            found_data = True # Mark data as found if this set has results
                    except StopIteration:
                        pass # Only one result set returned
                    except Exception as e:
                        st.error(f"Error processing revenue by mode: {e}")

                    # Process third result set: Revenue by Train
                    try:
                        third_result_set = next(results_iterator)
                        train_results = third_result_set.fetchall()
                        if train_results:
                            revenue_by_train = pd.DataFrame(train_results)
                            # Convert decimal to float for display
                            revenue_by_train['train_revenue'] = revenue_by_train['train_revenue'].astype(float)
                            found_data = True # Mark data as found if this set has results
                    except StopIteration:
                        pass # Only two result sets returned
                    except Exception as e:
                        st.error(f"Error processing revenue by train: {e}")

                    if found_data:
                        st.subheader(f"Revenue Report ({start_date} to {end_date})")
                        
                        # Display Total Revenue only if it's greater than 0 or other data exists
                        if total_revenue > 0:
                             st.metric(label="Total Revenue", value=f"₹ {total_revenue:,.2f}")
                             st.markdown("---")
                        # Check if DataFrames are empty before displaying
                        elif revenue_by_mode.empty and revenue_by_train.empty:
                             st.info(f"No revenue data found for the period {start_date} to {end_date}.")
                             # Exit early if no data at all
                             cursor.close()
                             conn.close()
                             st.stop()


                        # Display Revenue by Payment Mode
                        if not revenue_by_mode.empty:
                            st.subheader("Revenue by Payment Mode")
                            revenue_by_mode.rename(columns={
                                'payment_mode': 'Payment Mode',
                                'mode_revenue': 'Revenue (₹)'
                            }, inplace=True)
                            st.dataframe(revenue_by_mode.sort_values(by='Revenue (₹)', ascending=False)) # Sort for consistency
                            st.markdown("---")
                        # Don't show 'No data' if total revenue was shown
                        elif total_revenue == 0 and revenue_by_train.empty: 
                            st.info("No revenue data found by payment mode for this period.")


                        # Display Revenue by Train
                        if not revenue_by_train.empty:
                            st.subheader("Revenue by Train")
                            revenue_by_train.rename(columns={
                                'train_name': 'Train Name',
                                'train_revenue': 'Revenue (₹)'
                            }, inplace=True)
                            st.dataframe(revenue_by_train.sort_values(by='Revenue (₹)', ascending=False))
                        # Don't show 'No data' if total revenue or mode revenue was shown
                        elif total_revenue == 0 and revenue_by_mode.empty:
                            st.info("No revenue data found by train for this period.")

                    # This else handles the case where found_data remains False after checking all result sets
                    else:
                        st.info(f"No revenue data found for the period {start_date} to {end_date}.")
                    
                    cursor.close()
                    conn.close()
                else:
                    st.error("Database connection failed.")
            except Exception as e:
                st.error(f"Error generating revenue report: {e}")

# Cancellation page
elif st.session_state.page == "Cancellation":
    st.header("Cancel Tickets")
    
    if not st.session_state.logged_in:
        st.warning("Please login to cancel tickets")
    else:
        pnr_number = st.text_input("Enter PNR Number to Cancel")
        
        if st.button("Search Ticket") or st.session_state.search_performed:
            st.session_state.search_performed = not st.session_state.search_performed
            if pnr_number:
                # Query the database for the PNR
                try:
                    conn = connect_to_db()
                    if conn:
                        cursor = conn.cursor(dictionary=True)
                        
                        # Query to get ticket information based on PNR number
                        ticket_query = """
                        SELECT 
                            t.ticket_id, t.pnr_number, t.journey_date, t.seat_number, t.status, t.fare,
                            tr.train_id, tr.train_name, tr.train_type,
                            c.class_name,
                            s1.station_name as from_station, s1.station_code as from_code,
                            s2.station_name as to_station, s2.station_code as to_code,
                            p.passenger_id, p.name as passenger_name, p.age, p.gender
                        FROM ticket t
                        JOIN train tr ON t.train_id = tr.train_id
                        JOIN class c ON t.class_id = c.class_id
                        JOIN station s1 ON t.from_station_id = s1.station_id
                        JOIN station s2 ON t.to_station_id = s2.station_id
                        JOIN passenger p ON t.passenger_id = p.passenger_id
                        LEFT JOIN cancellation cn ON t.ticket_id = cn.ticket_id
                        WHERE t.pnr_number = %s AND cn.cancellation_id IS NULL
                        """
                        cursor.execute(ticket_query, (pnr_number,))
                        ticket_results = cursor.fetchall()
                        
                        if ticket_results:
                            st.success("Ticket Found")
                            
                            # Get the first result for common ticket information
                            first_result = ticket_results[0]
                            
                            # Store ticket ID in session state for cancellation
                            st.session_state.ticket_id = first_result['ticket_id']
                            st.session_state.ticket_fare = float(first_result['fare'])  # Convert Decimal to float
                            
                            # Display ticket details
                            ticket_data = {
                                "PNR Number": first_result['pnr_number'],
                                "Train": first_result['train_name'],
                                "Train Type": first_result['train_type'],
                                "From": f"{first_result['from_station']} ({first_result['from_code']})",
                                "To": f"{first_result['to_station']} ({first_result['to_code']})",
                                "Date of Journey": first_result['journey_date'].strftime('%d-%b-%Y') if isinstance(first_result['journey_date'], datetime) else first_result['journey_date'],
                                "Class": first_result['class_name'],
                                "Status": first_result['status']
                            }
                            
                            for field, value in ticket_data.items():
                                col1, col2 = st.columns([1, 2])
                                with col1:
                                    st.write(f"**{field}:**")
                                with col2:
                                    st.write(value)
                            
                            # Display passenger details with checkboxes for selection
                            st.subheader("Passengers")
                            
                            passengers = []
                            for i, passenger in enumerate(ticket_results):
                                seat_info = f" ({passenger['seat_number']})" if passenger['seat_number'] else ""
                                passenger_status = f"{passenger['status']}{seat_info}"
                                
                                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
                                with col1:
                                    st.write(passenger["passenger_name"])
                                with col2:
                                    st.write(passenger["age"])
                                with col3:
                                    st.write(passenger["gender"])
                                with col4:
                                    st.write(passenger_status)
                                with col5:
                                    selected = st.checkbox(f"Select", key=f"cancel_passenger_{i}", value=True)
                                    if selected:
                                        passengers.append(passenger)
                            
                            # Calculate cancellation charges and refund amount
                            # In a real app, this would be based on railway rules, journey date, etc.
                            journey_date = first_result['journey_date']
                            current_date = datetime.now().date()
                            
                            # Simple logic: 
                            # - If journey date is more than 7 days away: 20% charge
                            # - If journey date is between 2-7 days away: 30% charge
                            # - If journey date is less than 2 days away: 50% charge
                            days_to_journey = (journey_date - current_date).days if isinstance(journey_date, datetime) else 5
                            
                            if days_to_journey > 7:
                                cancellation_percentage = 0.20
                            elif days_to_journey >= 2:
                                cancellation_percentage = 0.30
                            else:
                                cancellation_percentage = 0.50
                            
                            # Convert fare to float to avoid decimal multiplication error
                            total_fare = float(first_result['fare'])
                            cancellation_charge = round(total_fare * cancellation_percentage, 2)
                            refund_amount = round(total_fare - cancellation_charge, 2)
                            
                            # Store refund amount in session state
                            st.session_state.refund_amount = refund_amount
                            
                            reason = st.selectbox("Reason for Cancellation", 
                                                ["Change of plans", "Emergency", "Duplicate booking", "Other"])
                            
                            st.warning(f"Cancellation Charges: ₹ {cancellation_charge}")
                            st.success(f"Refund Amount: ₹ {refund_amount}")
                            
                            if st.button("Confirm Cancellation"):
                                try:
                                    conn = connect_to_db()
                                    if conn:
                                        cursor = conn.cursor()
                                        
                                        # Store the reason for future reference
                                        st.session_state.cancellation_reason = reason
                                        
                                        # Insert into cancellation table - This will trigger the 'after_cancellation' trigger
                                        insert_query = """
                                        INSERT INTO cancellation 
                                        (ticket_id, cancellation_date, refund_amount, refund_status) 
                                        VALUES (%s, %s, %s, %s)
                                        """
                                        
                                        current_datetime = datetime.now() # Use datetime for cancellation_date
                                        
                                        cursor.execute(insert_query, (
                                            st.session_state.ticket_id,
                                            current_datetime, # Use current datetime
                                            st.session_state.refund_amount,
                                            "Pending" # Set initial refund status
                                        ))
                                        
                                        # Get the newly inserted cancellation_id
                                        cursor.execute("SELECT LAST_INSERT_ID()")
                                        cancellation_id = cursor.fetchone()[0]
                                        
                                        # Commit the transaction (which includes the trigger action)
                                        conn.commit()
                                        
                                        cursor.close()
                                        conn.close()
                                        
                                        st.success("Ticket cancellation initiated successfully!") # Updated message
                                        st.info(f"Cancellation ID: {cancellation_id}")
                                        st.info(f"Cancellation Date: {current_datetime.strftime('%d-%b-%Y %H:%M:%S')}")
                                        st.info(f"Refund Amount: ₹{st.session_state.refund_amount}")
                                        st.info(f"Refund Status: Pending")
                                        st.info("Refund will be processed based on cancellation rules.")
                                        # Clear state if needed
                                        # del st.session_state.ticket_id
                                        # del st.session_state.ticket_fare
                                        # del st.session_state.refund_amount
                                        
                                    else:
                                        st.error("Database connection failed. Please try again later.")
                                except Exception as e:
                                    st.error(f"Error cancelling ticket: {e}")
                                    # Rollback if connection exists and an error occurred during insert
                                    if conn and conn.is_connected():
                                        conn.rollback()
                                        cursor.close()
                                        conn.close()
                        else:
                            st.error(f"No valid ticket found with PNR number: {pnr_number}")
                            st.info("The ticket may not exist, already be cancelled, or the journey date has passed.")
                        
                        cursor.close()
                        conn.close()
                    else:
                        st.error("Database connection failed. Please try again later.")
                except Exception as e:
                    st.error(f"Error retrieving ticket information: {e}")
            else:
                st.error("Please enter a valid PNR number")

# My Bookings page
elif st.session_state.page == "My Bookings":
    st.header("My Bookings")
    
    if not st.session_state.logged_in:
        st.warning("Please login to view your bookings")
    else:
        tab1, tab2 = st.tabs(["Upcoming Journeys", "Past Journeys"])
        
        with tab1:
            st.subheader("Upcoming Journeys")
            
            # In a real app, this would query your database
            # For demo, we'll create sample data
            upcoming_bookings = pd.DataFrame({
                'PNR': ['1234567890', '2345678901'],
                'Train': ['Rajdhani Express', 'Shatabdi Express'],
                'From': ['Delhi', 'Mumbai'],
                'To': ['Mumbai', 'Pune'],
                'Date': ['15-Apr-2025', '25-Apr-2025'],
                'Status': ['Confirmed', 'Waitlist #2']
            })
            
            if len(upcoming_bookings) > 0:
                for i, row in upcoming_bookings.iterrows():
                    with st.expander(f"{row['Train']} - {row['Date']} ({row['Status']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**PNR:** {row['PNR']}")
                            st.write(f"**From:** {row['From']}")
                            st.write(f"**To:** {row['To']}")
                        with col2:
                            st.write(f"**Train:** {row['Train']}")
                            st.write(f"**Date:** {row['Date']}")
                            st.write(f"**Status:** {row['Status']}")
                        
                        if row['Status'] == 'Confirmed':
                            if st.button(f"Cancel Booking {row['PNR']}", key=f"cancel_{row['PNR']}"):
                                st.warning("Redirecting to cancellation page...")
                        elif 'Waitlist' in row['Status']:
                            if st.button(f"Check Status {row['PNR']}", key=f"status_{row['PNR']}"):
                                st.info("Checking latest waitlist position...")
            else:
                st.info("No upcoming journeys found")
        
        with tab2:
            st.subheader("Past Journeys")
            
            # In a real app, this would query your database
            # For demo, we'll create sample data
            past_bookings = pd.DataFrame({
                'PNR': ['3456789012', '4567890123'],
                'Train': ['Duronto Express', 'Jan Shatabdi'],
                'From': ['Kolkata', 'Chennai'],
                'To': ['Delhi', 'Bengaluru'],
                'Date': ['10-Mar-2025', '15-Feb-2025'],
                'Status': ['Completed', 'Cancelled']
            })
            
            if len(past_bookings) > 0:
                for i, row in past_bookings.iterrows():
                    with st.expander(f"{row['Train']} - {row['Date']} ({row['Status']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**PNR:** {row['PNR']}")
                            st.write(f"**From:** {row['From']}")
                            st.write(f"**To:** {row['To']}")
                        with col2:
                            st.write(f"**Train:** {row['Train']}")
                            st.write(f"**Date:** {row['Date']}")
                            st.write(f"**Status:** {row['Status']}")
            else:
                st.info("No past journeys found")

# Add logout button to sidebar if logged in
if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 Indian Railway Ticket Reservation System | CS2202 Mini Project")