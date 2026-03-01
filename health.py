import streamlit as st
import sqlite3
import random

# ---------- DATABASE ----------
conn = sqlite3.connect("healthcare.db", check_same_thread=False)
c = conn.cursor()

# ---------- TABLES ----------
c.execute("CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY, patient TEXT, doctor TEXT, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS staff(id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS equipment(id INTEGER PRIMARY KEY, device TEXT, condition TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS alerts(id INTEGER PRIMARY KEY, system TEXT, level TEXT)")
conn.commit()

st.title("🏥 Smart Healthcare IT Infrastructure Management System")

menu = [
    "Patient Management",
    "Appointment System",
    "Staff Management",
    "Medical Equipment",
    "System Alerts",
    "Infrastructure Monitoring"
]

choice = st.sidebar.selectbox("Select Module", menu)

# ================= PATIENT MANAGEMENT =================
if choice == "Patient Management":
    st.header("👨‍⚕️ Patient Records")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", step=1, format="%d")

    if st.button("Add Patient"):
        c.execute("INSERT INTO patients(name,age) VALUES(?,?)",(name,age))
        conn.commit()
        st.success("Patient Added")

    data = c.execute("SELECT * FROM patients").fetchall()
    st.table(data)

# ================= APPOINTMENT SYSTEM =================
elif choice == "Appointment System":
    st.header("📅 Appointment Scheduling")

    patient = st.text_input("Patient Name")
    doctor = st.text_input("Doctor Name")

    if st.button("Book Appointment"):
        c.execute("INSERT INTO appointments(patient,doctor,status) VALUES(?,?,?)",
                  (patient,doctor,"Scheduled"))
        conn.commit()
        st.success("Appointment Booked")

    app_id = st.number_input("Appointment ID", min_value=1, step=1, format="%d")
    status = st.selectbox("Update Status",["Scheduled","Completed","Cancelled"])

    if st.button("Update Appointment"):
        c.execute("UPDATE appointments SET status=? WHERE id=?",(status,app_id))
        conn.commit()
        st.success("Appointment Updated")

    data = c.execute("SELECT * FROM appointments").fetchall()
    st.table(data)

# ================= STAFF MANAGEMENT =================
elif choice == "Staff Management":
    st.header("👩‍💼 Hospital Staff Management")

    name = st.text_input("Staff Name")
    role = st.selectbox("Role",["Doctor","Nurse","Technician","Admin"])

    if st.button("Add Staff"):
        c.execute("INSERT INTO staff(name,role) VALUES(?,?)",(name,role))
        conn.commit()
        st.success("Staff Added")

    data = c.execute("SELECT * FROM staff").fetchall()
    st.table(data)

# ================= EQUIPMENT MANAGEMENT =================
elif choice == "Medical Equipment":
    st.header("🩺 Medical Equipment Tracking")

    device = st.text_input("Equipment Name")
    condition = st.selectbox("Condition",["Working","Maintenance","Out of Service"])

    if st.button("Add Equipment"):
        c.execute("INSERT INTO equipment(device,condition) VALUES(?,?)",
                  (device,condition))
        conn.commit()
        st.success("Equipment Added")

    data = c.execute("SELECT * FROM equipment").fetchall()
    st.table(data)

# ================= SYSTEM ALERTS =================
elif choice == "System Alerts":
    st.header("🚨 Healthcare System Alerts")

    system = st.text_input("System Name")
    level = st.selectbox("Alert Level",["Low","Medium","High","Critical"])

    if st.button("Generate Alert"):
        c.execute("INSERT INTO alerts(system,level) VALUES(?,?)",(system,level))
        conn.commit()
        st.warning("Alert Generated")

    data = c.execute("SELECT * FROM alerts").fetchall()
    st.table(data)

# ================= INFRASTRUCTURE MONITORING =================
elif choice == "Infrastructure Monitoring":
    st.header("🖥️ Hospital IT Infrastructure Monitoring")

    cpu = random.randint(20,95)
    ram = random.randint(30,95)
    server = random.choice(["Online","Offline"])

    st.write("CPU Usage:", cpu,"%")
    st.write("RAM Usage:", ram,"%")
    st.write("Server Status:", server)

    if cpu > 85 or ram > 85 or server == "Offline":
        st.error("⚠️ Critical Infrastructure Issue")
    else:
        st.success("✅ Systems Running Normally")