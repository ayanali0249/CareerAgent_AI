import streamlit as st
import json
import os
import time
import hashlib
import pickle
from datetime import datetime
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import User, ResumeHistory
from parser.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from parser.skill_matcher import extract_skills
from utils.similarity import calculate_match_score
from utils.pdf_generator import PDFReport
from utils.email_verifier import (send_verification_email,send_otp_email,otp_storage,generate_otp)
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.graph_objects as go


# ---------------------- MUST BE FIRST ----------------------
st.set_page_config(
    page_title="CareerAgent AI",
    layout="wide",
    page_icon="🚀"
)
st.markdown("""
<style>

[data-testid="stSidebar"]{
    background:#0f172a;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-weight:600;
}

div[data-testid="metric-container"]{
    background:#111827;
    border:1px solid #374151;
    padding:15px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------- Load Data ----------------------
with open("data/skill_keywords.txt", encoding="utf-8") as f:
    skills_list = f.read().splitlines()

with open("data/job_descriptions.json", encoding="utf-8") as f:
    job_data = json.load(f)
    job_titles = list(job_data.keys())

# ---------------------- Utility Functions ----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user and user.password == hash_password(password)

def create_user(username, password, email):
    db = SessionLocal()
    user = User(username=username, password=hash_password(password), email=email)
    db.add(user)
    db.commit()
    db.close()
    send_verification_email(email)

def logout():
    clear_login()
    st.session_state.clear()
    st.rerun()

def update_email(new_email):
    db = SessionLocal()
    user = db.query(User).filter(User.username == st.session_state.username).first()
    if user:
        user.email = new_email
        db.commit()
    db.close()

def delete_account():
    db = SessionLocal()
    user = db.query(User).filter(User.username == st.session_state.username).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    logout()

def save_login(username, email):

    with open("user_session.pkl", "wb") as f:

        pickle.dump(
            {
                "username": username,
                "email": email
            },
            f
        )


def load_login():

    if os.path.exists("user_session.pkl"):

        with open("user_session.pkl", "rb") as f:

            return pickle.load(f)

    return None


def clear_login():

    if os.path.exists("user_session.pkl"):

        os.remove("user_session.pkl")

# ---------------------- Session State ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"
saved_user = load_login()

if saved_user and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.username = saved_user["username"]
    st.session_state.email = saved_user["email"]

# ---------------------- Navigation Bar ----------------------
def nav_bar():

    with st.sidebar:

        st.markdown("""
        <div style="
        text-align:center;
        padding:15px;
        ">
            <h1>🚀</h1>
            <h2>CareerAgent AI</h2>
            <p>AI Career Development Agent</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.active_page = "Dashboard"

        if st.button("👤 Account", use_container_width=True):
            st.session_state.active_page = "Account"

        st.markdown("---")

        st.info(f"Logged in as\n\n**{st.session_state.username}**")

# ---------------------- Login UI ----------------------
def login_ui():
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    padding:30px;
    border-radius:20px;
    text-align:center;
    margin-bottom:25px;
    color:white;
    ">

    <h1>🚀 CareerAgent AI</h1>

    <h4>
    AI-Powered Career Development Agent
    </h4>

    <p>
    Analyze resumes • Find skill gaps • Get career recommendations
    </p>

    </div>
""", unsafe_allow_html=True)
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()

        if user:
            if not user.email_verified:
                st.warning("Your email is not verified. Please complete email verification.")
                # Pre-fill OTP if it was OTP-based verification
                st.session_state.pending_username = user.username
                st.session_state.pending_email = user.email
                st.session_state.pending_password = password  # So they don't have to re-type
                st.session_state.verification_method = "OTP"
                st.session_state.show_otp_input = True
            elif check_password_hash(user.password, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.email = user.email
                save_login(username,user.email)
                st.session_state.email_verified = user.email_verified
                st.success("Logged in successfully!")
                db.close()
                st.rerun()
            else:
                st.error("Incorrect password.")
                db.close()
        else:
            st.error("Username not found.")
            db.close()

# ---------------------- Signup UI ----------------------
def signup_ui():
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    padding:30px;
    border-radius:20px;
    text-align:center;
    margin-bottom:25px;
    color:white;
    ">

    <h1>🚀 CareerAgent AI</h1>

    <h4>
    Create Your Career Profile
    </h4>

    <p>
    Start your journey toward better job opportunities
    </p>

    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("New Username", key="signup_user")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("New Password", type="password", key="signup_pass")

    verification_method = st.radio("Choose Email Verification Method", ["OTP"])

    if st.button("Sign Up"):
        if not username or not email or not password:
            st.error("Please fill in all fields.")
            return

        db = SessionLocal()
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        db.close()

        if existing_user:
            st.error("This username or email is already registered.")
            return

        # Temporarily store in session
        st.session_state.pending_username = username
        st.session_state.pending_email = email
        st.session_state.pending_password = password
        st.session_state.verification_method = verification_method
        st.session_state.show_otp_input = True

        if verification_method == "OTP":
            send_otp_email(email)
            st.success("OTP sent. Please verify.")
        else:
            send_verification_email(email)
            st.success("Verification link sent.")
        st.rerun()

    # OTP or Link Verification UI
    if st.session_state.get("show_otp_input"):
        method = st.session_state.get("verification_method")
        email = st.session_state.get("pending_email")

        if method == "OTP":
            otp_entered = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                otp_data = otp_storage.get(email)
                if otp_data:
                    otp, timestamp = otp_data
                    if time.time() - timestamp < 600 and otp_entered == otp:
                        # Save to DB only after valid OTP
                        db = SessionLocal()
                        try:
                            user = User(
                                username=st.session_state.pending_username,
                                email=st.session_state.pending_email,
                                password=generate_password_hash(st.session_state.pending_password),
                                email_verified=True
                            )
                            db.add(user)
                            db.commit()
                            st.success("Email verified and account created. You can now log in.")
                            st.session_state.show_otp_input = False
                        except Exception as e:
                            st.error("Error while saving user. Try a different username/email.")
                            print("Signup DB error:", e)
                        finally:
                            db.close()
                    else:
                        st.error("Invalid or expired OTP.")

        elif method == "Email Link":
            st.info("Please check your email and click the link to verify.")
            if st.button("Resend Link"):
                send_verification_email(email)
                st.success("Verification link resent.")

# ------------------ Utility to Render Skill Badges with Copy Button ------------------
def render_skills_section(title, skills, color="#f1f3f4", text_color="#202124", key="copy1"):
    if not skills:
        st.write("No skills found.")
        return

    skill_str = ", ".join(skills)

    badge_html = " ".join([
        f"<span style='background:{color}; color:{text_color}; padding:6px 12px; margin:5px; border-radius:15px; display:inline-block; font-size:14px;'>{skill}</span>"
        for skill in skills
    ])

    html_block = f"""
    <div style="margin-top: 10px; margin-bottom: 10px;">
        <div style="margin-bottom: 8px;">{badge_html}</div>
        <button onclick="navigator.clipboard.writeText('{skill_str}')"
            style="padding:8px 14px; background:#1a73e8; color:white; border:none; border-radius:6px; font-size:14px; cursor:pointer;">
            Copy Skills
        </button>
    </div>
    """

    st.markdown(f"<h4 style='margin-bottom: 5px;'>{title}</h4>", unsafe_allow_html=True)
    st.markdown(html_block, unsafe_allow_html=True)

# ---------------------- Resume Analyzer Dashboard ----------------------
def resume_analyzer_dashboard():
    db = SessionLocal()
    user = db.query(User).filter(User.username == st.session_state.username).first()
    if user and not user.email_verified:
        st.warning("Your email is not verified. Please check your inbox.")
    db.close()

    st.markdown(f"""
        <div style="
        padding:20px;
        border-radius:15px;
        background:#111827;
        border:1px solid #374151;
        margin-bottom:20px;
        ">
        <h2>👋 Welcome, {st.session_state.username}</h2>
        <p>
        Analyze your resume, discover skill gaps,
        and boost your ATS score.
        </p>
        </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.info("📄 Resume Analysis")

    with col2:
        st.info("🎯 Job Matching")

    with col3:
        st.info("🚀 Career Growth")

    st.markdown("""
        <h3 style='text-align:center;'>
        📄 Upload Resume & Analyze Career Readiness
        </h3>
        """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "doc", "txt"]
        )

    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext == "pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif ext in ["docx", "doc"]:
            resume_text = extract_text_from_docx(uploaded_file)
        elif ext == "txt":
            resume_text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        extracted_skills = extract_skills(resume_text, skills_list)
        render_skills_section("Extracted Skills", extracted_skills, "#e8f0fe", "#1967d2", key="copy_extracted")

        st.markdown("### Search Job Role")
        job_input = st.text_input("Type job title...").strip()
        filtered_jobs = [job for job in job_titles if job_input.lower() in job.lower()]

        if job_input and filtered_jobs:
            selected_job = st.selectbox("Matching Roles", filtered_jobs)
        else:
            selected_job = st.selectbox("Select Job Role", job_titles)

        job_skills = job_data[selected_job]
        score, breakdown = calculate_match_score(extracted_skills, job_skills, return_details=True)
        matched_skills = breakdown["Matched Skills"]
        missing_skills = breakdown["Missing Skills"]

        st.markdown("## 📊 ATS Analysis")

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "ATS Score",
                f"{score:.1f}%"
            )

        with col2:
            st.metric(
                "Skills Found",
                len(extracted_skills)
            )

        with col3:
            st.metric(
                "Matched",
                len(matched_skills)
            )

        with col4:
            st.metric(
                "Missing",
                len(missing_skills)
            )

        st.progress(score / 100)

        st.markdown("---")

        # Analytics Charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "ATS Score"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#2563EB"
                    }
                }
            ))

            gauge.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

        with chart_col2:

            pie = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Matched Skills",
                            "Missing Skills"
                        ],
                        values=[
                            len(matched_skills),
                            len(missing_skills)
                        ],
                        hole=0.55
                    )
                ]
            )

            pie.update_layout(
                title="Skills Breakdown",
                height=350
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

        st.markdown("---")

        # Skills Section
        render_skills_section(
            "✅ Matched Skills",
            matched_skills,
            "#d0f0c0",
            "#2e7d32",
            key="copy_matched"
        )

        render_skills_section(
            "❌ Missing Skills",
            missing_skills,
            "#ffebee",
            "#c62828",
            key="copy_missing"
        )

        st.markdown("---")

        # AI Insights
        st.markdown("## 🤖 AI Career Insights")

        if len(missing_skills) > 0:

            for skill in missing_skills[:5]:

                st.info(
                    f"🚀 Recommended Learning: {skill}"
                )

        else:

            st.success(
                "Excellent! No major skill gaps detected."
            )

        st.markdown("---")

        # Career Roadmap

        st.markdown("## 🎯 Career Roadmap")

        if score >= 85:
            readiness = "Job Ready"
            timeline = "1-2 Weeks"

        elif score >= 70:
            readiness = "Almost Ready"
            timeline = "4-6 Weeks"

        else:
            readiness = "Needs Improvement"
            timeline = "8-12 Weeks"

        road_col1, road_col2 = st.columns(2)

        with road_col1:
            st.success(
                f"Current Readiness\n\n{readiness}"
            )

        with road_col2:
            st.info(
                f"Estimated Timeline\n\n{timeline}"
            )

        st.markdown(f"""
        ### 🎯 Target Role

        **{selected_job}**
        """)

        st.markdown("### 📚 Recommended Skills To Learn")

        if len(missing_skills) > 0:

            for skill in missing_skills[:10]:

                st.checkbox(
                    skill,
                    value=False,
                    disabled=True
                )

        else:

            st.success(
                "You already have most of the required skills for this role."
            )

        # Score Message

        if score >= 85:
            st.success("Excellent match. You're well qualified for this role.")

        elif score >= 65:
            st.info("Good match. Consider improving your resume by adding missing skills.")

        else:
            st.warning("Weak match. You may want to update your skill set.")

        # PDF Report

        report = PDFReport(
            name=st.session_state.username,
            job_role=selected_job
        )

        pdf_path = report.generate(
            extracted_skills=extracted_skills,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            score=score
        )

        with open(pdf_path, "rb") as f:

            st.download_button(
                label="📥 Download Professional Report",
                data=f,
                file_name="Resume_Analysis_Report.pdf",
                mime="application/pdf"
            )
# ---------------------- Account Settings Page ----------------------

def account_settings_page():

    st.markdown("""
    <h2>👤 Account Settings</h2>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📧 Change Email")

    new_email = st.text_input("New Email Address")

    if st.button("Update Email"):

        if new_email:

            update_email(new_email)

            st.success(
                "Email updated successfully."
            )

        else:

            st.error(
                "Please enter a valid email."
            )

    st.markdown("---")

    st.subheader("🗑️ Delete Account")

    if st.button("Delete My Account"):

        delete_account()

        st.success(
            "Account deleted successfully."
        )

    st.markdown("---")

    st.subheader("🚪 Logout")

    if st.button("Logout"):

        logout()

# ---------------------- Main App Routing ----------------------
if st.session_state.logged_in:
    nav_bar()
    if st.session_state.active_page == "Dashboard":
        resume_analyzer_dashboard()
    elif st.session_state.active_page == "Account":
        account_settings_page()
else:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        login_ui()
    with tab2:
        signup_ui()
# python -m streamlit run app.py