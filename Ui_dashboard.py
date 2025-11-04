# Ui_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from Database import (
    get_recent_users, get_user_growth,
    add_device, get_all_devices, update_device, delete_device
)

def home_ui():
    st.title("🏠 Home Dashboard")

    # User Growth Chart
    st.subheader("📈 User Growth (Past 6 Months)")
    growth_data = get_user_growth()
    if growth_data:
        df = pd.DataFrame(growth_data, columns=["Date", "User Count"])
        fig = px.line(df, x="Date", y="User Count", markers=True, title="User Growth Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No users yet to display growth.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧍 Recently Added Users")
        users = get_recent_users()
        for u in users:
            st.write(f"**{u[0]} {u[1]}** — {u[2]} ({u[3]})")

    with col2:
        st.subheader("💻 Recently Added Devices")
        devices = get_all_devices()[:5]
        for d in devices:
            st.write(f"**{d[2]}** - {d[3]} (S/N: {d[1]})")

def devices_ui():
    st.title("📱 Device Management")

    st.subheader("Add New Device")

    # --- Dynamic Model Dropdown Fix ---
    device_type = st.selectbox("Device Type", ["Phone", "PC", "Mac"], key="device_type")

    model_options = {
        "Phone": ["iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15", "iPhone 16", "iPhone 17"],
        "PC": ["HP 840 G6", "HP 840 G7", "HP 840 G8", "HP 840 G9", "HP 840 G10"],
        "Mac": ["MacBook Pro M1", "MacBook Pro M2", "MacBook Pro M3", "MacBook Pro M4", "MacBook Pro M5"],
    }

    model = st.selectbox("Model", model_options[device_type], key=f"model_{device_type}")
    serial_number = st.text_input("Serial Number / IMEI")

    if st.button("Add Device"):
        if serial_number:
            add_device(serial_number, device_type, model)
            st.success(f"Added {device_type}: {model}")
            st.rerun()
        else:
            st.warning("Please enter a valid serial number.")

    st.divider()
    st.subheader("All Devices")

    devices = get_all_devices()
    df = pd.DataFrame(devices, columns=["ID", "Serial", "Type", "Model", "Created"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Edit or Remove Device")
    if devices:
        ids = [str(d[0]) for d in devices]
        selected_id = st.selectbox("Select Device ID", ids)
        selected = next((d for d in devices if str(d[0]) == selected_id), None)

        if selected:
            with st.form("edit_device_form"):
                new_serial = st.text_input("Serial Number", selected[1])
                new_type = st.selectbox("Device Type", ["Phone", "PC", "Mac"], index=["Phone", "PC", "Mac"].index(selected[2]), key="edit_type")
                new_model = st.selectbox("Model", model_options[new_type], key=f"edit_model_{new_type}")
                col1, col2 = st.columns(2)
                with col1:
                    update = st.form_submit_button("💾 Save Changes")
                with col2:
                    delete = st.form_submit_button("🗑️ Delete Device")

            if update:
                update_device(selected[0], new_serial, new_type, new_model)
                st.success("Device updated!")
                st.rerun()
            if delete:
                delete_device(selected[0])
                st.warning("Device deleted!")
                st.rerun()
