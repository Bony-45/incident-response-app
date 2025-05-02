import streamlit as st
import datetime
import json
import os

# Initialize session state
if 'incident' not in st.session_state:
    st.session_state.incident = {}

if 'team' not in st.session_state:
    st.session_state.team = []

if 'actions' not in st.session_state:
    st.session_state.actions = []

if 'evidence' not in st.session_state:
    st.session_state.evidence = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = {}

if 'remedies' not in st.session_state:
    st.session_state.remedies = {}

if 'post_review' not in st.session_state:
    st.session_state.post_review = {}

st.set_page_config(page_title="Incident Response App", layout="wide")
st.title("Incident Response Simulation System")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "Incident Reporting", "Team Assignment", "Incident Response Workflow",
    "Evidence Collection", "Checklist", "Remedies", "Post-Incident Review", "Generate Report"])

if page == "Incident Reporting":
    st.header("Incident Reporting")
    incident_type = st.selectbox("Incident Type", ["Phishing", "Ransomware", "SQL Injection", "DDoS", "Credential Theft", "Malware", "Insider Threat", "Other"])
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Describe the incident")
    reported_time = st.date_input("Date", datetime.date.today())

    if st.button("Submit Incident"):
        st.session_state.incident = {
            "type": incident_type,
            "severity": severity,
            "description": description,
            "reported_time": str(reported_time)
        }
        st.success("Incident submitted successfully!")

elif page == "Team Assignment":
    st.header("Assign Response Team")
    roles = ["Incident Handler", "Forensic Analyst", "Containment Lead", "Recovery Lead", "Communication Officer"]
    team = []
    for role in roles:
        name = st.text_input(f"Enter name for {role}", key=role)
        if name:
            team.append({"role": role, "name": name})

    if st.button("Assign Team"):
        st.session_state.team = team
        st.success("Team assigned successfully")

elif page == "Incident Response Workflow":
    st.header("Response Workflow")
    step = st.selectbox("Select Step", ["Detection", "Analysis", "Containment", "Eradication", "Recovery"])
    action = st.text_area("Action taken")
    if st.button("Log Action"):
        st.session_state.actions.append({"step": step, "action": action, "time": str(datetime.datetime.now())})
        st.success("Action logged")

    st.subheader("Logged Actions")
    for a in st.session_state.actions:
        st.write(f"**{a['step']}**: {a['action']} @ {a['time']}")

elif page == "Evidence Collection":
    st.header("Evidence Upload")
    uploaded = st.file_uploader("Upload evidence", type=["png", "jpg", "log", "txt", "pdf"])
    if uploaded:
        file_details = {"filename": uploaded.name, "timestamp": str(datetime.datetime.now())}
        st.session_state.evidence.append(file_details)
        st.success(f"Uploaded {uploaded.name}")

    st.subheader("Uploaded Evidence")
    for e in st.session_state.evidence:
        st.write(f"{e['filename']} uploaded at {e['timestamp']}")

elif page == "Checklist":
    st.header("Checklist for Response")
    tasks = ["Isolate system", "Notify stakeholders", "Backup data", "Initiate recovery", "Update firewall rules", "Run antivirus scan"]
    for task in tasks:
        done = st.checkbox(task, key=task)
        st.session_state.checklist[task] = done

elif page == "Remedies":
    st.header(" Recommended Remedies for Common Cyberattacks")
    remedies_map = {
        "Phishing": "Conduct user awareness training, enable multi-factor authentication, deploy email filters.",
        "Ransomware": "Maintain regular backups, update antivirus and software, isolate infected systems.",
        "SQL Injection": "Use parameterized queries, validate user input, implement web application firewalls.",
        "DDoS": "Use rate limiting, deploy anti-DDoS services, monitor network traffic anomalies.",
        "Credential Theft": "Implement strong password policies, MFA, and login monitoring.",
        "Malware": "Install endpoint protection, scan regularly, block suspicious files.",
        "Insider Threat": "Implement access controls, monitor user behavior, enforce least privilege policy."
    }

    selected = st.selectbox("Select Attack Type", list(remedies_map.keys()))
    if selected:
        remedy = remedies_map[selected]
        st.session_state.remedies[selected] = remedy
        st.write(f"### Remedy for {selected}")
        st.write(remedy)

elif page == "Post-Incident Review":
    st.header("Post-Incident Review")
    success = st.text_area("What went well?", key="success")
    challenges = st.text_area("What were the challenges?", key="challenges")
    improvement = st.text_area("Suggestions for improvement", key="improve")
    if st.button("Save Review"):
        st.session_state.post_review = {
            "success": success,
            "challenges": challenges,
            "improvement": improvement
        }
        st.success("Review saved")

elif page == "Generate Report":
    st.header("Incident Report Summary")
    st.subheader("Incident Details")
    st.json(st.session_state.incident)

    st.subheader("Team Assigned")
    st.json(st.session_state.team)

    st.subheader("Response Actions")
    st.json(st.session_state.actions)

    st.subheader("Evidence")
    st.json(st.session_state.evidence)

    st.subheader("Checklist Completion")
    st.json(st.session_state.checklist)

    st.subheader("Remedies Suggested")
    st.json(st.session_state.remedies)

    st.subheader("Post-Incident Review")
    st.json(st.session_state.post_review)

    st.success("Report ready. Use 'Save as PDF' from your browser to export.")
