import streamlit as st
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
   return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255),
            year VARCHAR(10),
            genre VARCHAR(100),
            read_status BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    conn.close()

create_table()