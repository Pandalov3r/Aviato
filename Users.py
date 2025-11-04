# Users.py
import streamlit as st
import pandas as pd
from Database import add_user, get_recent_users, get_parent_departments, get_sub_departments

def users_ui():
    st.title("👥 User Management")

    st.subheader("Add New User")
    parents = get_parent_departments()
    parent_names = [p[1] for p in parents]

    selected_parent = st.selectbox("Department", parent_names if parent_names else ["None"])

    sub_departments = []
    if selected_parent and selected_parent != "None":
        parent_id = next((p[0] for p in parents if p[1] == selected_parent), None)
        subs = get_sub_departments(parent_id)
        sub_departments = [s[1] for s in subs]

    selected_sub = st.selectbox("Sub-Department", sub_departments if sub_departments else ["None"])

    with st.form("add_user_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        role = st.text_input("Role")
        submit_user = st.form_submit_button("Add User")

    if submit_user:
        if first_name and last_name and email:
            add_user(first_name, last_name, email, role, selected_parent, selected_sub)
            st.success(f"Added user: {first_name} {last_name}")
            st.rerun()
        else:
            st.warning("Please fill all fields.")

    st.divider()
    st.subheader("Recently Added Users")
    users = get_recent_users(10)
    df_users = pd.DataFrame(users, columns=["First Name", "Last Name", "Email", "Department", "Sub-Department", "Created"])
    st.dataframe(df_users, use_container_width=True)
