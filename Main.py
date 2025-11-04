# Main.py
import streamlit as st
from Database import init_db
from Ui_dashboard import home_ui, devices_ui
from Users import users_ui
from Dictionary_tree import dictionary_ui

# Initialize DB
init_db()

st.set_page_config(page_title="Company Admin Dashboard", layout="wide")

st.sidebar.title("📊 Dashboard Menu")
menu = st.sidebar.radio("Navigation", ["Home", "Dictionary Tree", "Users", "Devices"])

if menu == "Home":
    home_ui()
elif menu == "Dictionary Tree":
    dictionary_ui()
elif menu == "Users":
    users_ui()
elif menu == "Devices":
    devices_ui()
