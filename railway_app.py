import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import random
import string

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
    return ''.join(random.choices(string.digits, k=10))

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None

# App title and sidebar
st.title("Indian Railway Ticket Reservation System")

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", 
                           ["Login", "Train Search", "Booking", "PNR Status", 
                            "Cancellation", "My Bookings", "Admin Panel"])

# Login page
if page == "Login":
    st.header("User Login")
    
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            # In a real app, you would verify credentials against the database
            # For demo, we'll use hardcoded values
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
    
    with col2:
        if st.button("Register New User"):
            st.info("Registration functionality would be implemented here")

# Train Search page
elif page == "Train Search":
    st.header("Search Trains")
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_station = st.selectbox("From Station", 
                                   ["Delhi (NDLS)", "Mumbai (CSTM)", "Chennai (MAS)", 
                                    "Kolkata (KOAA)", "Bengaluru (SBC)"])
    
    with col2:
        to_station = st.selectbox("To Station", 
                                 ["Mumbai (CSTM)", "Delhi (NDLS)", "Bengaluru (SBC)", 
                                  "Chennai (MAS)", "Hyderabad (SC)"])
    
    journey_date = st.date_input("Journey Date", min_value=datetime.now().date())
    
    if st.button("Search Trains"):
        # In a real app, this would query your database
        # For demo, we'll create sample data
        if from_station != to_station:
            sample_trains = pd.DataFrame({
                'Train Number': ['12309', '12951', '12910', '12301', '12259'],
                'Train Name': ['Rajdhani Express', 'Shatabdi Express', 'Duronto Express', 'Howrah Mail', 'Garib Rath'],
                'Departure': ['06:00', '08:30', '15:45', '23:55', '11:30'],
                'Arrival': ['14:30', '13:00', '06:30', '13:40', '00:45'],
                'Duration': ['8h 30m', '4h 30m', '14h 45m', '13h 45m', '13h 15m'],
                'Available Seats': [42, 16, 8, 65, 27]
            })
            
            st.write(f"Showing trains from {from_station} to {to_station} on {journey_date}")
            st.dataframe(sample_trains)
            
            # Allow booking selection
            selected_train = st.selectbox("Select Train to Book", sample_trains['Train Name'])
            selected_class = st.selectbox("Select Class", 
                                        ["AC First Class (1A)", "AC 2-Tier (2A)", "AC 3-Tier (3A)", 
                                         "Sleeper (SL)", "Second Sitting (2S)"])
            
            if st.button("Proceed to Booking"):
                if st.session_state.logged_in:
                    st.session_state.booking_train = selected_train
                    st.session_state.booking_class = selected_class
                    st.session_state.from_station = from_station
                    st.session_state.to_station = to_station
                    st.session_state.journey_date = journey_date
                    st.success(f"Selected {selected_train} in {selected_class}. Please navigate to the Booking page.")
                else:
                    st.warning("Please login first to book tickets")
        else:
            st.error("Source and destination stations cannot be the same")

# Booking page
elif page == "Booking":
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
                                         ["Senior Citizen", "Student", "Disabled", "Freedom Fighter"])
            concession_id = st.text_input("Concession ID / Document Number")
        
        # Berth preference
        berth_preference = st.selectbox("Berth Preference", 
                                      ["No Preference", "Lower", "Middle", "Upper", "Side Lower", "Side Upper"])
        
        # Meals preference
        meals = st.checkbox("Opt for Meals")
        
        # Payment options
        st.subheader("Payment Details")
        
        fare_details = {
            "Base Fare": "₹ 1,240.00",
            "Reservation Charges": "₹ 40.00",
            "Superfast Charges": "₹ 45.00",
            "GST (5%)": "₹ 66.25",
            "Total Fare": "₹ 1,391.25"
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
            st.info(f"Your PNR number is: {pnr}")
            st.info("Ticket details have been sent to your email.")

# PNR Status page
elif page == "PNR Status":
    st.header("Check PNR Status")
    
    pnr_number = st.text_input("Enter PNR Number")
    
    if st.button("Check Status"):
        if pnr_number and len(pnr_number) == 10 and pnr_number.isdigit():
            # In a real app, this would query your database
            # For demo, we'll create sample data
            st.success("PNR Found")
            
            pnr_data = {
                "PNR Number": pnr_number,
                "Train": "12309 Rajdhani Express",
                "From": "Delhi (NDLS)",
                "To": "Mumbai (CSTM)",
                "Date of Journey": "15-Apr-2025",
                "Class": "AC 3-Tier (3A)",
                "Status": "Confirmed (B2, 42)",
                "Passenger 1": "John Doe (Confirmed)",
                "Passenger 2": "Jane Doe (Confirmed)"
            }
            
            for field, value in pnr_data.items():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**{field}:**")
                with col2:
                    st.write(value)
        else:
            st.error("Please enter a valid 10-digit PNR number")

# Cancellation page
elif page == "Cancellation":
    st.header("Cancel Tickets")
    
    if not st.session_state.logged_in:
        st.warning("Please login to cancel tickets")
    else:
        pnr_number = st.text_input("Enter PNR Number to Cancel")
        
        if st.button("Search Ticket"):
            if pnr_number and len(pnr_number) == 10 and pnr_number.isdigit():
                # In a real app, this would query your database
                # For demo, we'll create sample data
                st.success("Ticket Found")
                
                ticket_data = {
                    "PNR Number": pnr_number,
                    "Train": "12309 Rajdhani Express",
                    "From": "Delhi (NDLS)",
                    "To": "Mumbai (CSTM)",
                    "Date of Journey": "15-Apr-2025",
                    "Class": "AC 3-Tier (3A)",
                }
                
                for field, value in ticket_data.items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(f"**{field}:**")
                    with col2:
                        st.write(value)
                
                passengers = [
                    {"name": "John Doe", "age": 35, "gender": "Male", "status": "Confirmed (B2, 42)"},
                    {"name": "Jane Doe", "age": 32, "gender": "Female", "status": "Confirmed (B2, 44)"}
                ]
                
                st.subheader("Passengers")
                for i, passenger in enumerate(passengers):
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
                    with col1:
                        st.write(passenger["name"])
                    with col2:
                        st.write(passenger["age"])
                    with col3:
                        st.write(passenger["gender"])
                    with col4:
                        st.write(passenger["status"])
                    with col5:
                        st.checkbox(f"Select", key=f"cancel_passenger_{i}")
                
                reason = st.selectbox("Reason for Cancellation", 
                                    ["Change of plans", "Emergency", "Duplicate booking", "Other"])
                
                st.warning("Cancellation Charges: ₹ 348.00")
                st.success("Refund Amount: ₹ 1,043.25")
                
                if st.button("Confirm Cancellation"):
                    st.success("Ticket cancelled successfully!")
                    st.info("Refund has been initiated and will be credited within 5-7 working days.")
            else:
                st.error("Please enter a valid 10-digit PNR number")

# My Bookings page
elif page == "My Bookings":
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

# Admin Panel page
elif page == "Admin Panel":
    st.header("Admin Panel")
    
    if not st.session_state.logged_in:
        st.warning("Please login as admin to access this panel")
    elif st.session_state.role != "admin":
        st.error("You don't have permission to access the admin panel")
    else:
        # Admin tabs
        admin_tab = st.tabs(["Dashboard", "Manage Trains", "Manage Schedules", "Manage Fares", "System Users"])
        
        with admin_tab[0]:
            st.subheader("Dashboard")
            
            # Mock statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Bookings Today", value="1,245", delta="+12%")
            with col2:
                st.metric(label="Revenue Today", value="₹ 8.2L", delta="+8%")
            with col3:
                st.metric(label="Active Waitlists", value="436", delta="-5%")
            
            # Mock charts
            chart_data = pd.DataFrame({
                'date': pd.date_range(start='2025-03-01', periods=30, freq='D'),
                'bookings': [random.randint(800, 1500) for _ in range(30)],
                'revenue': [random.randint(500000, 1000000) for _ in range(30)]
            })
            
            st.subheader("Booking Trends")
            st.line_chart(chart_data.set_index('date')['bookings'])
            
            st.subheader("Revenue Trends")
            st.line_chart(chart_data.set_index('date')['revenue'])
            
            # Busiest routes
            st.subheader("Busiest Routes")
            busiest_routes = pd.DataFrame({
                'Route': ['Delhi-Mumbai', 'Mumbai-Bengaluru', 'Chennai-Delhi', 
                         'Kolkata-Delhi', 'Hyderabad-Chennai'],
                'Passengers': [4528, 3982, 3541, 3125, 2987]
            })
            st.dataframe(busiest_routes)
        
        with admin_tab[1]:
            st.subheader("Manage Trains")
            
            # Add new train form
            with st.expander("Add New Train"):
                col1, col2 = st.columns(2)
                with col1:
                    train_number = st.text_input("Train Number")
                    train_name = st.text_input("Train Name")
                    train_type = st.selectbox("Train Type", ["Rajdhani", "Shatabdi", "Duronto", "Superfast", "Express", "Passenger"])
                
                with col2:
                    source = st.selectbox("Source Station", ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru"])
                    destination = st.selectbox("Destination Station", ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"])
                    total_seats = st.number_input("Total Seats", min_value=100, max_value=2000, value=1000)
                
                st.subheader("Class Configuration")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    has_1ac = st.checkbox("AC First Class (1A)")
                    if has_1ac:
                        seats_1ac = st.number_input("1A Seats", min_value=1, max_value=100, value=18)
                
                with col2:
                    has_2ac = st.checkbox("AC 2-Tier (2A)")
                    if has_2ac:
                        seats_2ac = st.number_input("2A Seats", min_value=1, max_value=200, value=46)
                
                with col3:
                    has_3ac = st.checkbox("AC 3-Tier (3A)")
                    if has_3ac:
                        seats_3ac = st.number_input("3A Seats", min_value=1, max_value=500, value=72)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    has_sl = st.checkbox("Sleeper (SL)")
                    if has_sl:
                        seats_sl = st.number_input("SL Seats", min_value=1, max_value=1000, value=288)
                
                with col2:
                    has_2s = st.checkbox("Second Sitting (2S)")
                    if has_2s:
                        seats_2s = st.number_input("2S Seats", min_value=1, max_value=1000, value=576)
                
                if st.button("Add Train"):
                    st.success(f"Train {train_number} {train_name} added successfully")
            
            # List existing trains
            st.subheader("Existing Trains")
            existing_trains = pd.DataFrame({
                'Train Number': ['12309', '12951', '12910', '12301', '12259'],
                'Train Name': ['Rajdhani Express', 'Shatabdi Express', 'Duronto Express', 'Howrah Mail', 'Garib Rath'],
                'Source': ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bengaluru'],
                'Destination': ['Mumbai', 'Delhi', 'Delhi', 'Delhi', 'Chennai'],
                'Type': ['Rajdhani', 'Shatabdi', 'Duronto', 'Superfast', 'Express'],
                'Status': ['Active', 'Active', 'Active', 'Active', 'Active']
            })
            
            st.dataframe(existing_trains)
            
            # Edit selected train
            selected_train_number = st.selectbox("Select Train to Edit", existing_trains['Train Number'])
            if st.button("Edit Selected Train"):
                st.info(f"Editing train {selected_train_number}")
        
        with admin_tab[2]:
            st.subheader("Manage Schedules")
            
            # Schedule management interface here
            train_for_schedule = st.selectbox("Select Train", ['12309 Rajdhani Express', '12951 Shatabdi Express'])
            
            # Add station to route
            with st.expander("Add Station to Route"):
                col1, col2 = st.columns(2)
                with col1:
                    station = st.selectbox("Station", ["Delhi", "Mumbai", "Chennai", "Kolkata", "Nagpur", "Jaipur"])
                    arrival = st.time_input("Arrival Time", datetime.now().time())
                
                with col2:
                    sequence = st.number_input("Sequence Number", min_value=1, max_value=20, value=1)
                    departure = st.time_input("Departure Time", (datetime.now() + timedelta(minutes=10)).time())
                
                distance = st.number_input("Distance from Source (km)", min_value=0, max_value=5000, value=0)
                
                if st.button("Add Station"):
                    st.success(f"Station {station} added to route at sequence {sequence}")
            
            # View current route
            st.subheader("Current Route")
            route_data = pd.DataFrame({
                'Seq': [1, 2, 3, 4],
                'Station': ['Delhi', 'Mathura', 'Kota', 'Mumbai'],
                'Arrival': ['--:--', '08:25', '11:35', '16:50'],
                'Departure': ['06:55', '08:30', '11:40', '--:--'],
                'Distance': ['0', '150', '458', '1386']
            })
            
            st.dataframe(route_data)
        
        with admin_tab[3]:
            st.subheader("Manage Fares")
            
            col1, col2 = st.columns(2)
            with col1:
                train_for_fare = st.selectbox("Select Train", ['12309 Rajdhani Express', '12951 Shatabdi Express'], key='fare_train')
            with col2:
                class_for_fare = st.selectbox("Select Class", ["AC First Class (1A)", "AC 2-Tier (2A)", "AC 3-Tier (3A)"])
            
            st.subheader("Base Fare Settings")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                base_fare = st.number_input("Base Fare per KM", min_value=0.1, max_value=10.0, value=1.8, step=0.1)
            with col2:
                reservation_charge = st.number_input("Reservation Charge", min_value=0, max_value=100, value=40)
            with col3:
                superfast_charge = st.number_input("Superfast Charge", min_value=0, max_value=100, value=45)
            
            gst = st.slider("GST Percentage", min_value=0, max_value=18, value=5)
            
            if st.button("Update Fare Structure"):
                st.success("Fare structure updated successfully")
            
            # Fare preview
            st.subheader("Fare Preview")
            st.info(f"For a 1000 km journey on {train_for_fare} in {class_for_fare}")
            
            fare_calculation = {
                "Base Fare (1000 km × ₹1.8)": "₹ 1,800.00",
                "Reservation Charges": f"₹ {reservation_charge}.00",
                "Superfast Charges": f"₹ {superfast_charge}.00",
                f"GST ({gst}%)": f"₹ {round((1800 + reservation_charge + superfast_charge) * gst/100, 2)}",
                "Total Fare": f"₹ {round((1800 + reservation_charge + superfast_charge) * (1 + gst/100), 2)}"
            }
            
            for item, amount in fare_calculation.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(item)
                with col2:
                    st.write(amount)
        
        with admin_tab[4]:
            st.subheader("System Users")
            
            # User management interface
            user_tab1, user_tab2 = st.tabs(["User List", "Add User"])
            
            with user_tab1:
                users = pd.DataFrame({
                    'User ID': [1001, 1002, 9001, 9002],
                    'Username': ['user', 'john_doe', 'admin', 'manager'],
                    'Role': ['passenger', 'passenger', 'admin', 'manager'],
                    'Status': ['Active', 'Active', 'Active', 'Inactive'],
                    'Last Login': ['2025-04-13 09:45:22', '2025-04-12 18:32:11', '2025-04-13 10:05:17', '2025-04-05 14:22:33']
                })
                
                st.dataframe(users)
                
                col1, col2 = st.columns(2)
                with col1:
                    user_to_edit = st.selectbox("Select User", users['Username'])
                with col2:
                    action = st.selectbox("Action", ["Reset Password", "Deactivate", "Change Role"])
                
                if st.button("Apply Action"):
                    st.success(f"Action '{action}' applied to user '{user_to_edit}'")
            
            with user_tab2:
                col1, col2 = st.columns(2)
                with col1:
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                
                with col2:
                    new_role = st.selectbox("Role", ["passenger", "manager", "admin"])
                    new_status = st.selectbox("Status", ["Active", "Inactive"])
                
                if st.button("Add User"):
                    if new_password == confirm_password:
                        st.success(f"User '{new_username}' added successfully")
                    else:
                        st.error("Passwords do not match")

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