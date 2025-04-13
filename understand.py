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
    
conn = connect_to_db()
if conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * from booking;')
    result = cursor.fetchall()
    db = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
    print(db)
    cursor.close()