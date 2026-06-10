# 🚀 CareerAgent AI

Welcome to **CareerAgent AI**, an intelligent AI-powered career development platform designed to help students, job seekers, and professionals optimize their resumes, improve ATS compatibility, identify skill gaps, and accelerate career growth.

CareerAgent AI goes beyond traditional resume analysis by combining resume parsing, ATS score analysis, job role matching, career roadmap generation, interview preparation, and professional PDF reporting into a single interactive platform.

Built using Python, Streamlit, MySQL, NLP-based skill extraction, and interactive analytics to deliver a modern and engaging user experience.

---

# Project Structure

```bash
CareerAgent_AI/
│
├── app.py
├── config.py
├── init_db.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── logo.png
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── models.py
│
├── parser/
│   ├── __init__.py
│   ├── resume_parser.py
│   └── skill_matcher.py
│
├── utils/
│   ├── email_verifier.py
│   ├── pdf_generator.py
│   └── similarity.py
│
└── data/
    ├── job_descriptions.json
    └── skill_keywords.txt
```

---

# Tech Stack

### Frontend & Dashboard

* Streamlit
* Custom HTML & CSS Styling
* Interactive UI Components
* Responsive Dashboard Layout

### Backend

* Python
* SQLAlchemy
* MySQL

### Artificial Intelligence & NLP

* Resume Parsing
* Skill Extraction Engine
* ATS Score Calculation
* Job Role Matching
* Skill Gap Analysis
* Career Recommendation System

### Data Visualization

* Plotly
* Interactive Gauge Charts
* Skill Distribution Analytics
* ATS Performance Dashboard

### Authentication & Security

* User Registration
* Secure Login System
* Email Verification
* Password Encryption
* Session Persistence

### Reporting

* Automated PDF Report Generation
* Career Assessment Reports
* Downloadable Analysis Reports

---

# Features

## 🔐 Authentication System

* User Registration
* Secure Login
* Email Verification via OTP
* Persistent Login Sessions
* Account Management
* Logout Functionality

## 📄 Resume Analysis

* PDF Resume Support
* DOCX Resume Support
* TXT Resume Support
* Automatic Resume Parsing
* Skill Extraction
* Resume Intelligence Processing

## 🎯 ATS Score Analysis

* ATS Compatibility Score
* Resume Readiness Assessment
* Skill Matching Analysis
* Missing Skills Detection

## 💼 Job Role Matching

* Search Job Roles
* Intelligent Role Recommendations
* Job-Specific Skill Matching
* Career Readiness Evaluation

## 📊 Interactive Analytics Dashboard

* ATS Score Metrics
* Interactive Gauge Visualization
* Skills Breakdown Charts
* Resume Performance Analytics
* Career Growth Insights

## 🤖 AI Career Insights

* Skill Gap Detection
* Personalized Learning Recommendations
* Career Development Suggestions
* Professional Growth Guidance

## 🛣 Career Roadmap Generator

* Career Readiness Assessment
* Estimated Learning Timeline
* Recommended Skills to Learn
* Goal-Oriented Career Planning

## 🎤 Interview Preparation

* Role-Based Interview Guidance
* Technical Interview Preparation
* Career Readiness Evaluation

## 📑 Professional Reports

* Downloadable PDF Reports
* Resume Analysis Summary
* ATS Performance Reports
* Career Development Reports

---

# Dashboard Preview
<img width="1918" height="958" alt="image" src="https://github.com/user-attachments/assets/a9649c8c-6981-4600-a570-4d5a02725573" />

### CareerAgent AI Dashboard Includes:

* Resume Upload & Analysis
* ATS Score Dashboard
* Skill Gap Analysis
* Job Matching System
* Career Roadmap Generator
* AI Career Insights
* Interview Preparation Support
* Professional PDF Reports

---

# Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/CareerAgent_AI.git
```

### 2. Open Project Directory

```bash
cd CareerAgent_AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

DB_USERNAME=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=resume_analyzer

SECRET_KEY=your_secret_key
BASE_URL=http://localhost:8501
```

### 5. Initialize Database

```bash
python init_db.py
```

### 6. Run Application

```bash
streamlit run app.py
```

---

# Usage

CareerAgent AI can be used for:

* Resume Optimization
* ATS Score Improvement
* Career Readiness Assessment
* Skill Gap Analysis
* Interview Preparation
* Career Planning
* Student Career Development
* Professional Growth Tracking

Simply upload a resume, choose a target job role, and receive detailed AI-powered career insights.

---

# Future Enhancements

* AI Career Chatbot
* Resume Version History
* Personalized Learning Paths
* LinkedIn Profile Analysis
* AI Mock Interview Simulator
* Job Recommendation Engine
* Cloud-Based Resume Storage
* Advanced Career Analytics
* Multi-Language Support

---

# System Requirements

### Hardware Requirements

* Processor: Intel Core i3 or above
* RAM: Minimum 4 GB
* Storage: 500 MB Free Space

### Software Requirements

* Python 3.10+
* MySQL 8.0+
* Streamlit
* Modern Web Browser

---

# License

This project is licensed under the MIT License.

Copyright (c) 2026 Ayan Ali

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to use, modify, and distribute the software subject to the conditions specified in the license.

---

## Contact

* 📧 Email: [ayanali0249@gmail.com](mailto:ayanali0249@gmail.com)
* 💼 LinkedIn: https://linkedin.com/in/ayanali0249
* 💻 GitHub: https://github.com/ayanali0249
* 🌐 Portfolio: https://ayan-ali-0249.netlify.app

---

<p align="center">
  <strong>🚀 Designed & Developed by Ayan Ali</strong>
</p>
