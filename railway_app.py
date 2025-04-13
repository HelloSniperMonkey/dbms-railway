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
        # Check if we have booking info from train search
        if hasattr(st.session_state, 'booking_train'):
            st.info(f"Booking for: {st.session_state.booking_train} ({st.session_state.booking_class})")
            st.info(f"From {st.session_state.from_station} to {st.session_state.to_station}")
            st.info(f"Journey Date: {st.session_state.journey_date}")
        else:
            st.warning("Please search and select a train first")
            
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
        
        # Dynamically compute fare details based on concession (if applied)
        base_fare = 1240.00
        reservation_charge = 40.00
        superfast_charge = 45.00
        GST_rate = 5.00
        
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
        if 'has_concession' in locals() and has_concession:
            discount_rate = discount_mapping.get(concession_type.lower(), 0.0)
        
        discount_amount = base_fare * (discount_rate / 100)
        effective_base_fare = base_fare - discount_amount
        fare_without_tax = effective_base_fare + reservation_charge + superfast_charge
        GST_amount = fare_without_tax * (GST_rate / 100)
        total_fare = fare_without_tax + GST_amount
        
        fare_details = {
            "Base Fare": f"₹ {effective_base_fare:.2f}",
            "Reservation Charges": f"₹ {reservation_charge:.2f}",
            "Superfast Charges": f"₹ {superfast_charge:.2f}",
            "GST (5%)": f"₹ {GST_amount:.2f}",
            "Total Fare": f"₹ {total_fare:.2f}"
        }
        
        for item, amount in fare_details.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(item)
            with col2:
                st.write(amount)
        
        payment_method = st.selectbox("Payment Method", 
                                    ["Credit/Debit Card", "Net Banking", "UPI", "Wallet"])
        
        if st.button("Proceed to Payment"):
            st.success("Booking Successful!")
            pnr = generate_pnr()
            st.info(f"Your PNR number is: PNR{pnr}")
            st.info("Ticket details have been sent to your email.")

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

# Cancellation page
elif st.session_state.page == "Cancellation":
    st.header("Cancel Tickets")
    
    if not st.session_state.logged_in:
        st.warning("Please login to cancel tickets")
    else:
        pnr_number = st.text_input("Enter PNR Number to Cancel")
        
        if st.button("Search Ticket"):
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
                                        
                                        # Insert into cancellation table with refund status as Pending
                                        insert_query = """
                                        INSERT INTO cancellation 
                                        (ticket_id, cancellation_date, refund_amount, refund_status) 
                                        VALUES (%s, %s, %s, %s)
                                        """
                                        
                                        current_date = datetime.now()
                                        
                                        cursor.execute(insert_query, (
                                            st.session_state.ticket_id,
                                            current_date,
                                            st.session_state.refund_amount,
                                            "Pending"
                                        ))
                                        
                                        # Get the newly inserted cancellation_id
                                        cursor.execute("SELECT LAST_INSERT_ID()")
                                        cancellation_id = cursor.fetchone()[0]
                                        
                                        # Commit the transaction
                                        conn.commit()
                                        
                                        # Update ticket status to Cancelled in ticket table
                                        update_query = """
                                        UPDATE ticket SET status = 'Cancelled' WHERE ticket_id = %s
                                        """
                                        cursor.execute(update_query, (st.session_state.ticket_id,))
                                        conn.commit()
                                        
                                        cursor.close()
                                        conn.close()
                                        
                                        st.success("Ticket cancelled successfully!")
                                        st.info(f"Cancellation ID: {cancellation_id}")
                                        st.info(f"Cancellation Date: {current_date.strftime('%d-%b-%Y %H:%M:%S')}")
                                        st.info(f"Refund Amount: ₹{st.session_state.refund_amount}")
                                        st.info(f"Refund Status: Pending")
                                        st.info("Refund has been initiated and will be credited within 5-7 working days.")
                                        
                                    else:
                                        st.error("Database connection failed. Please try again later.")
                                except Exception as e:
                                    st.error(f"Error cancelling ticket: {e}")
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