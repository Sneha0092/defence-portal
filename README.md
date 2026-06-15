# 🪖 Defence Career Guidance Portal

**Author:** Sneha
**Affiliation:** Govindrao Wanjari College of Engineering & Technology, Nagpur
**University:** Dr. Babasaheb Ambedkar Technological University (DBATU)
**Date:** June 2026

🌐 **Live Demo:** [defence-career-portal.onrender.com](https://defence-career-portal.onrender.com)
🔗 **GitHub:** [github.com/Sneha0092/defence-portal](https://github.com/Sneha0092/defence-portal)

---

## Abstract

The Defence Career Guidance Portal is a full-stack web application designed to assist Indian students and aspirants in exploring career opportunities across the Indian Army, Navy, and Air Force. Many students lack awareness about the variety of entry schemes, eligibility criteria, physical standards, and salary structures offered by the Indian Armed Forces. This portal addresses that gap by providing a centralized, interactive platform. The system features a smart eligibility checker that matches user profiles to over 20 real entry schemes based on age, gender, education, stream, and height. A fitness tracker evaluates physical readiness against official Army, Navy, and Air Force standards with pass/fail analysis and improvement tips. Additional features include user authentication, bookmark saving, a contact query system, and a personal dashboard. The application is built using Python Flask for the backend, SQLite for data persistence, and HTML5/CSS3/JavaScript for the frontend. It is deployed on Render.com and available as a live web application.

---

## 1. Introduction

### 1.1 Background

The Indian Armed Forces — comprising the Army, Navy, and Air Force — are among the most prestigious career paths in India. However, a large number of students, especially from rural and semi-urban backgrounds, are unaware of the variety of entry schemes available, their eligibility criteria, physical requirements, and career growth paths.

### 1.2 Motivation

Existing government websites such as `joinindianarmy.nic.in`, `joinindiannavy.gov.in`, and `careerindianairforce.cdac.in` are informative but are spread across multiple platforms and lack personalization. Students often struggle to identify which entry scheme matches their specific profile — age, education, gender, height, and stream.

### 1.3 Objectives

- Provide a single platform covering all three Indian Armed Forces
- Build a smart eligibility checker that personalizes entry scheme recommendations
- Include a fitness tracker that compares user performance against official standards
- Allow users to register, save bookmarks, and track their eligibility history
- Deploy the application as a live, accessible web portal

---

## 2. Literature Review

### 2.1 Existing Solutions

| Platform | Limitation |
|---|---|
| joinindianarmy.nic.in | Only covers Army; no personalization |
| joinindiannavy.gov.in | Navy-specific; no eligibility matching |
| careerindianairforce.cdac.in | Air Force only; no fitness tracker |
| YouTube/blogs | Outdated; not interactive |

### 2.2 Related Technologies

- **Flask Framework:** Grinberg, M. (2018). *Flask Web Development*. O'Reilly Media. Flask is a lightweight WSGI web framework in Python widely used for building REST APIs and web applications.
- **SQLAlchemy ORM:** Bayer, M. (2012). *SQLAlchemy — The Database Toolkit for Python*. SQLAlchemy provides an ORM layer that abstracts SQL queries into Python objects.
- **Werkzeug Security:** Used for password hashing using PBKDF2-SHA256 algorithm, ensuring secure storage of user credentials.
- **Agnipath Scheme (2022):** Government of India introduced the Agniveer short-service scheme for all three forces, changing entry criteria for airmen and soldiers — incorporated in this portal.
- **Supreme Court Ruling (2021):** Women were permitted to appear for NDA examination, a change reflected in our eligibility logic.

---

## 3. Methodology

The portal follows a three-tier architecture: presentation layer (HTML/CSS/JS), application layer (Flask), and data layer (SQLite). When a user submits the eligibility form, the backend applies a rule-based matching algorithm that compares the user's age, gender, education level, stream, and height against a curated dataset of 20+ real entry schemes. An education hierarchy ensures that higher qualifications automatically qualify for lower-level entries. The fitness tracker computes BMI from height and weight, then evaluates run time, push-ups, and sit-ups against official standards for the selected force. Results are stored in the database for logged-in users, enabling progress tracking over time. User passwords are hashed using Werkzeug before storage, and sessions manage login state securely.

---

## 4. Implementation

### 4.1 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Backend Framework | Flask 3.0 |
| Database | SQLite via SQLAlchemy ORM |
| Password Security | Werkzeug PBKDF2-SHA256 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Google Fonts (Rajdhani, Libre Baskerville, IBM Plex Mono) |
| Deployment | Render.com (Gunicorn WSGI server) |
| Version Control | Git + GitHub |

### 4.2 Database Schema

```
User            → id, name, email, password, created_at
Bookmark        → id, user_id, force, entry_name, entry_tag, saved_at
EligibilityResult → id, user_id, age, gender, edu, stream, height, results, checked_at
FitnessLog      → id, user_id, force, run_time, pushups, situps, height, weight, pass/fail fields, logged_at
Query           → id, user_id, name, email, message, submitted_at
```

### 4.3 Project Structure

```
defence-portal/
├── app.py                  ← Flask app, routes, models, logic
├── requirements.txt        ← Python dependencies
├── Procfile                ← Render deployment config
└── templates/
    ├── base.html           ← Common layout and navigation
    ├── index.html          ← Home page with full portal content
    ├── login.html          ← User login
    ├── register.html       ← User registration
    ├── eligibility.html    ← Smart eligibility checker
    ├── fitness.html        ← Fitness tracker
    ├── dashboard.html      ← User dashboard
    └── contact.html        ← Contact/query form
```

### 4.4 Key Features

- **User Authentication** — Register, login, logout with hashed passwords
- **Eligibility Checker** — Matches profile to 20+ real entry schemes with official links
- **Fitness Tracker** — Pass/fail vs Army/Navy/Air Force standards with gap analysis
- **Bookmarks** — Save and manage entry schemes
- **Dashboard** — View eligibility history, fitness logs, and queries
- **Contact Form** — Submit queries stored in database
- **Responsive Design** — Works on mobile, tablet, and desktop

---

## 5. Results and Discussion

### 5.1 Eligibility Checker Output

The eligibility checker correctly identifies matching entry schemes based on user profile:

| Test Profile | Matches Found |
|---|---|
| Male, 18y, 12th PCM, 170cm | 10 entries (NDA, TES, Agniveer X/Y, etc.) |
| Female, 21y, Graduate, 155cm | 7 entries (OTA, INET, AFCAT, AFMS, etc.) |
| Male, 21y, Engineering, 168cm | 12 entries across all three forces |
| Female, 23y, Law, 150cm | 2 entries (JAG, AFMS) |
| Male, 17y, 10th pass, 162cm | 2 entries (Soldier GD, Navy MR) |

### 5.2 Fitness Tracker Output

The tracker evaluates 4 parameters against official standards:

| Force | Run (1.6km) | Push-ups | Sit-ups | BMI |
|---|---|---|---|---|
| Army | ≤ 7.5 min | ≥ 40 | ≥ 30 | 18–25 |
| Navy | ≤ 7.0 min | ≥ 35 | ≥ 25 | 18–25 |
| Air Force | ≤ 6.5 min | ≥ 40 | ≥ 30 | 18–25 |

### 5.3 Live Deployment

The application is successfully deployed at:
🔗 [https://defence-career-portal.onrender.com](https://defence-career-portal.onrender.com)

---

## 6. Limitations

- **SQLite in production:** SQLite is not ideal for concurrent users at scale. A PostgreSQL database would be more robust for production deployment.
- **Static entry data:** Entry scheme data is hardcoded in `app.py`. It requires manual updates when government notifications change.
- **No email verification:** User registration does not include email OTP verification, which could allow fake accounts.
- **Free tier hosting:** Render free tier spins down after inactivity, causing a 30–50 second cold start delay on first visit.
- **No admin panel:** There is no admin interface to view and manage all users and their data from the browser.
- **Physical standards:** Standards shown are for male officers. Female-specific and JCO/OR standards are simplified.

---

## 7. Future Scope

- **PostgreSQL integration** for scalable production database
- **Admin dashboard** to manage users, queries, and entry data
- **Email notifications** for new exam notifications via UPSC/Army/Navy/IAF
- **SSB Interview Prep module** with psychological test tips, GTO tasks, and interview questions
- **Exam countdown timers** for NDA, CDS, AFCAT with notification alerts
- **Defence Quiz** with 500+ MCQs on GK, current affairs, and defence knowledge
- **Mobile app** using Flutter or React Native wrapping the Flask API
- **Multi-language support** — Hindi, Marathi for regional aspirants
- **AI Chatbot** integration to answer career queries in real time
- **Automated data scraping** from official sites to keep entry data up to date

---

## 8. Conclusion

The Defence Career Guidance Portal successfully addresses the information gap faced by Indian Armed Forces aspirants. By combining a smart eligibility checker, fitness tracker, user authentication, and bookmark system in a single full-stack web application, it provides personalized, actionable career guidance. The portal covers 20+ real entry schemes across the Army, Navy, and Air Force with accurate 2024–25 eligibility data including recent changes such as the Agnipath/Agniveer scheme and women's NDA eligibility. Built using Python Flask and SQLite and deployed on Render.com, the project demonstrates practical application of full-stack web development skills. It serves as both a useful public resource and a strong portfolio project showcasing database design, backend development, and deployment expertise.

---

## References

[1] Ministry of Defence, Government of India. "Join Indian Army." *joinindianarmy.nic.in*. https://joinindianarmy.nic.in

[2] Indian Navy. "Join Indian Navy." *joinindiannavy.gov.in*. https://joinindiannavy.gov.in

[3] Indian Air Force. "Career Indian Air Force." *careerindianairforce.cdac.in*. https://careerindianairforce.cdac.in

[4] Union Public Service Commission. "UPSC — Combined Defence Services Examination." *upsc.gov.in*. https://upsc.gov.in

[5] Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.

[6] SQLAlchemy Documentation. "SQLAlchemy — The Database Toolkit for Python." https://docs.sqlalchemy.org

[7] Government of India. "Agnipath Scheme — Agniveer Vayu." *agnipathvayu.cdac.in*. https://agnipathvayu.cdac.in

[8] Supreme Court of India. *Kush Kalra vs Union of India* — Petition allowing women to appear in NDA examination. 2021.

[9] Armed Forces Medical Services. "AFMS Recruitment." *afms.nic.in*. https://afms.nic.in

[10] Werkzeug Documentation. "Werkzeug Security Helpers." https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security

[11] Render.com. "Deploy a Flask App." https://render.com/docs/deploy-flask
