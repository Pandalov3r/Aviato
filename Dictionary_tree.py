# Dictionary_tree.py
import streamlit as st
from Database import (
    get_departments, get_parent_departments, get_sub_departments,
    add_department, update_department, get_users_by_department, get_users_by_sub_department
)

def dictionary_ui():
    st.title("📂 Department Dictionary Tree")

    # Create Department or Sub Department
    st.subheader("Create New Department or Sub-Department")
    parent_depts = get_parent_departments()
    options = ["None (Top-Level Department)"] + [d[1] for d in parent_depts]

    with st.form("add_department_form"):
        dept_name = st.text_input("New Department / Sub-Department Name")
        parent_choice = st.selectbox("Parent Department", options)
        submit = st.form_submit_button("Add")

    if submit and dept_name:
        parent_id = None
        if parent_choice != "None (Top-Level Department)":
            parent_id = next((d[0] for d in parent_depts if d[1] == parent_choice), None)
        add_department(dept_name, parent_id)
        st.success(f"Added department: {dept_name}")
        st.rerun()

    st.divider()
    st.subheader("📁 Departments and Users")

    # Build tree
    parents = get_parent_departments()
    if not parents:
        st.info("No departments created yet.")
        return

    for pid, pname in parents:
        with st.expander(f"🏢 {pname}", expanded=False):
            users = get_users_by_department(pname)
            if users:
                st.markdown("**Users in this Department:**")
                for u in users:
                    st.write(f"👤 {u[0]} {u[1]} — {u[2]} (Sub: {u[3] or 'None'})")
            else:
                st.info("No users assigned.")

            subs = get_sub_departments(pid)
            if subs:
                st.markdown("**Sub-Departments:**")
                for sid, sname in subs:
                    with st.expander(f"📂 {sname}", expanded=False):
                        sub_users = get_users_by_sub_department(sname)
                        if sub_users:
                            for su in sub_users:
                                st.write(f"👤 {su[0]} {su[1]} — {su[2]}")
                        else:
                            st.info("No users in this sub-department.")

            # Edit option
            new_name = st.text_input(f"Edit name ({pname})", key=f"edit_{pid}")
            if st.button(f"💾 Save {pname}", key=f"save_{pid}"):
                update_department(pid, new_name)
                st.success("Updated successfully!")
                st.rerun()
