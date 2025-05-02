import streamlit as st
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Initialize session state with default values
def init_session_state():
    defaults = {
        'incident': {},
        'team': [],
        'actions': [],
        'evidence': [],
        'checklist': {},
        'remedies': {},
        'post_review': {},
        'start_time': datetime.datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Generate PDF report function
def generate_pdf_report():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph("Incident Response Report", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Incident Details
    story.append(Paragraph("1. Incident Details", styles['Heading2']))
    for key, value in st.session_state.incident.items():
        story.append(Paragraph(f"<b>{key.title()}:</b> {value}", styles['Normal']))
    
    # Team Members
    story.append(Spacer(1, 12))
    story.append(Paragraph("2. Response Team", styles['Heading2']))
    for member in st.session_state.team:
        story.append(Paragraph(f"{member['role']}: {member['name']}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main app configuration
st.set_page_config(page_title="Incident Response App", layout="wide")
st.title(" Incident Response Simulation System")

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", [
        "Incident Reporting", 
        "Team Assignment", 
        "Response Workflow",
        "Evidence Collection", 
        "Checklist", 
        "Remedies", 
        "Post-Incident Review", 
        "Generate Report"
    ])
    
    st.divider()
    if 'start_time' in st.session_state:
        st.write(f" Elapsed time: {datetime.datetime.now() - st.session_state['start_time']}")

# Incident Reporting Page
if page == "Incident Reporting":
    st.header(" Incident Reporting")
    
    col1, col2 = st.columns(2)
    with col1:
        incident_type = st.selectbox(
            "Incident Type",
            ["Phishing", "Ransomware", "SQL Injection", "DDoS", 
             "Credential Theft", "Malware", "Insider Threat", "Other"],
            index=0
        )
        
    with col2:
        severity = st.select_slider(
            "Severity Level",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium"
        )
    
    description = st.text_area(
        "Incident Description",
        placeholder="Provide detailed information about the incident..."
    )
    
    reported_time = st.date_input(
        "Date Reported",
        datetime.date.today()
    )
    
    if st.button("Submit Incident", type="primary"):
        if not description:
            st.error("Please provide an incident description")
        else:
            st.session_state.incident = {
                "type": incident_type,
                "severity": severity,
                "description": description,
                "reported_time": str(reported_time),
                "status": "Open"
            }
            st.success("Incident submitted successfully!")
            st.rerun()

# Team Assignment Page
elif page == "Team Assignment":
    st.header(" Team Assignment")
    
    roles = [
        "Incident Handler", 
        "Forensic Analyst", 
        "Containment Lead", 
        "Recovery Lead", 
        "Communication Officer"
    ]
    
    with st.form("team_assignment_form"):
        team = []
        for role in roles:
            name = st.text_input(f"{role}", key=f"team_{role}")
            if name:
                team.append({"role": role, "name": name})
        
        if st.form_submit_button("Assign Team", type="primary"):
            st.session_state.team = team
            st.success("Team assigned successfully!")
            st.rerun()
    
    st.divider()
    st.subheader("Current Team")
    if not st.session_state.team:
        st.warning("No team members assigned yet")
    else:
        for member in st.session_state.team:
            st.write(f" **{member['role']}**: {member['name']}")

# Response Workflow Page
elif page == "Response Workflow":
    st.header(" Response Workflow")
    
    tab1, tab2 = st.tabs(["Log Actions", "Action Timeline"])
    
    with tab1:
        with st.form("action_log_form"):
            step = st.selectbox(
                "Response Phase",
                ["Detection", "Analysis", "Containment", "Eradication", "Recovery"]
            )
            
            action = st.text_area(
                "Action Taken",
                placeholder="Describe the action taken in this phase..."
            )
            
            if st.form_submit_button("Log Action", type="primary"):
                if not action:
                    st.error("Please describe the action taken")
                else:
                    st.session_state.actions.append({
                        "step": step,
                        "action": action,
                        "timestamp": str(datetime.datetime.now())
                    })
                    st.success("Action logged successfully!")
                    st.rerun()
    
    with tab2:
        if not st.session_state.actions:
            st.warning("No actions logged yet")
        else:
            for action in st.session_state.actions:
                with st.expander(f"{action['step']} @ {action['timestamp']}"):
                    st.write(action['action'])

# Evidence Collection Page
elif page == "Evidence Collection":
    st.header(" Evidence Collection")
    
    tab1, tab2 = st.tabs(["Upload Evidence", "Evidence List"])
    
    with tab1:
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=["png", "jpg", "pdf", "txt", "log", "csv"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                file_details = {
                    "filename": file.name,
                    "type": file.type,
                    "size": f"{len(file.getvalue()) / 1024:.2f} KB",
                    "timestamp": str(datetime.datetime.now())
                }
                st.session_state.evidence.append(file_details)
            st.success(f"{len(uploaded_files)} files uploaded successfully!")
            st.rerun()
    
    with tab2:
        if not st.session_state.evidence:
            st.warning("No evidence collected yet")
        else:
            for idx, evidence in enumerate(st.session_state.evidence, 1):
                st.write(f"{idx}. **{evidence['filename']}**")
                st.caption(f"Type: {evidence['type']} | Size: {evidence['size']} | Uploaded: {evidence['timestamp']}")

# Checklist Page
elif page == "Checklist":
    st.header(" Response Checklist")
    
    tasks = {
        "Initial Response": [
            "Isolate affected systems",
            "Preserve evidence",
            "Notify stakeholders"
        ],
        "Containment": [
            "Block malicious IPs",
            "Disable compromised accounts",
            "Update firewall rules"
        ],
        "Recovery": [
            "Restore from backups",
            "Patch vulnerabilities",
            "Monitor for recurrence"
        ]
    }
    
    for category, items in tasks.items():
        st.subheader(category)
        for item in items:
            key = f"checklist_{category}_{item}"
            if key not in st.session_state.checklist:
                st.session_state.checklist[key] = False
            st.session_state.checklist[key] = st.checkbox(
                item,
                value=st.session_state.checklist[key],
                key=key
            )
    
    # Calculate completion percentage
    total = sum(len(items) for items in tasks.values())
    completed = sum(st.session_state.checklist.values())
    progress = completed / total if total > 0 else 0
    
    st.progress(progress, text=f"Completion: {int(progress*100)}%")

# Remedies Page
elif page == "Remedies":
    st.header("🛡 Recommended Remedies")
    
    remedies_data = {
        "Phishing": {
            "description": "Deceptive emails attempting to steal credentials",
            "remedies": [
                "Implement DMARC/DKIM/SPF email authentication",
                "Conduct regular phishing simulation training",
                "Enable multi-factor authentication (MFA)"
            ]
        },
        "Ransomware": {
            "description": "Malware that encrypts files for ransom",
            "remedies": [
                "Maintain offline, immutable backups",
                "Implement application whitelisting",
                "Disable macro scripts in Office files"
            ]
        }
    }
    
    selected = st.selectbox(
        "Select Attack Type",
        list(remedies_data.keys())
    )
    
    if selected:
        st.subheader(selected)
        st.write(remedies_data[selected]["description"])
        
        st.subheader("Recommended Remedies")
        for remedy in remedies_data[selected]["remedies"]:
            st.write(f" {remedy}")
        
        st.session_state.remedies[selected] = remedies_data[selected]

# Post-Incident Review Page
elif page == "Post-Incident Review":
    st.header(" Post-Incident Review")
    
    with st.form("post_review_form"):
        st.subheader("What worked well?")
        successes = st.text_area("Successes", key="successes")
        
        st.subheader("What challenges were faced?")
        challenges = st.text_area("Challenges", key="challenges")
        
        st.subheader("Lessons Learned")
        lessons = st.text_area("Improvements for next time", key="lessons")
        
        if st.form_submit_button("Submit Review", type="primary"):
            st.session_state.post_review = {
                "successes": successes,
                "challenges": challenges,
                "lessons": lessons,
                "timestamp": str(datetime.datetime.now())
            }
            st.session_state.incident["status"] = "Closed"
            st.success("Review submitted successfully!")
            st.rerun()
    
    if st.session_state.post_review:
        st.divider()
        st.subheader("Current Review")
        st.json(st.session_state.post_review)

# Generate Report Page
elif page == "Generate Report":
    st.header(" Generate Final Report")
    
    if not st.session_state.incident:
        st.warning("No incident data available. Please start with Incident Reporting.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Report Summary")
            st.write(f"**Incident Type**: {st.session_state.incident.get('type', 'N/A')}")
            st.write(f"**Severity**: {st.session_state.incident.get('severity', 'N/A')}")
            st.write(f"**Status**: {st.session_state.incident.get('status', 'Open')}")
            st.write(f"**Date Reported**: {st.session_state.incident.get('reported_time', 'N/A')}")
            
            pdf_report = generate_pdf_report()
            st.download_button(
                label="Download PDF Report",
                data=pdf_report,
                file_name="incident_report.pdf",
                mime="application/pdf"
            )
        
        with col2:
            st.subheader("Quick Stats")
            st.metric("Team Members", len(st.session_state.team))
            st.metric("Logged Actions", len(st.session_state.actions))
            st.metric("Evidence Items", len(st.session_state.evidence))
            
            if st.session_state.post_review:
                st.success("Post-incident review completed")
            else:
                st.warning("Post-incident review pending")
        
        st.divider()
        
        tabs = st.tabs([
            "Incident Details", "Team", "Actions", 
            "Evidence", "Checklist", "Remedies", "Review"
        ])
        
        with tabs[0]:
            st.json(st.session_state.incident)
        
        with tabs[1]:
            st.json(st.session_state.team)
        
        with tabs[2]:
            st.json(st.session_state.actions)
        
        with tabs[3]:
            st.json(st.session_state.evidence)
        
        with tabs[4]:
            st.json(st.session_state.checklist)
        
        with tabs[5]:
            st.json(st.session_state.remedies)
        
        with tabs[6]:
            st.json(st.session_state.post_review)

# Add some custom CSS
st.markdown("""
    <style>
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .st-b7 {
            background-color: #f0f2f6;
        }
        .st-cb {
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)
