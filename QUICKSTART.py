"""
Quick Start Guide for Employee Attrition Prediction System
"""

# QUICK START STEPS

print("""
╔════════════════════════════════════════════════════════════════════╗
║     EMPLOYEE ATTRITION PREDICTION & HR ANALYTICS SYSTEM             ║
║                        QUICK START GUIDE                            ║
╚════════════════════════════════════════════════════════════════════╝

STEP 1: INSTALL DEPENDENCIES
────────────────────────────────────────────────────────────────────
    pip install -r requirements.txt

STEP 2: INITIALIZE DATABASE
────────────────────────────────────────────────────────────────────
    python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database created!')
    "

STEP 3: SEED SAMPLE DATA
────────────────────────────────────────────────────────────────────
    python run.py seed_db

STEP 4: RUN THE APPLICATION
────────────────────────────────────────────────────────────────────
    python run.py

STEP 5: OPEN IN BROWSER
────────────────────────────────────────────────────────────────────
    http://localhost:5000

default CREDENTIALS
────────────────────────────────────────────────────────────────────
    Username: demo
    Password: demo123

KEY FEATURES
────────────────────────────────────────────────────────────────────
    ✓ User Authentication (Sign up / Login)
    ✓ Main Dashboard with KPIs
    ✓ Employee Management System
    ✓ Advanced Analytics
    ✓ Risk Assessment
    ✓ Department Analysis
    ✓ Salary Insights
    ✓ Export Capabilities

FOLDER STRUCTURE
────────────────────────────────────────────────────────────────────
    Employee/
    ├── app/
    │   ├── static/          (CSS, JS, Images)
    │   ├── templates/       (HTML Templates)
    │   ├── models/          (Database Models)
    │   ├── routes/          (Flask Routes)
    │   └── utils.py         (Utilities)
    ├── ml_model/            (ML Models)
    ├── dataset/             (Data Files)
    ├── run.py               (Entry Point)
    ├── config.py            (Configuration)
    └── requirements.txt     (Dependencies)

API ENDPOINTS
────────────────────────────────────────────────────────────────────
    Authentication:
      • GET  /auth/signup       - Registration page
      • POST /auth/signup       - Create account
      • GET  /auth/login        - Login page
      • POST /auth/login        - Authenticate
      • GET  /auth/logout       - Logout

    Dashboard:
      • GET /dashboard/                    - Main dashboard
      • GET /dashboard/employees           - Employee list
      • GET /dashboard/employee/<id>       - Employee details
      • GET /dashboard/analytics           - Analytics page
      • GET /dashboard/api/dashboard-stats - API stats

DATABASE MODELS
────────────────────────────────────────────────────────────────────
    User Model:
      - username, email, password_hash, full_name
      - role (hr_staff, manager, admin), department
      - is_active, created_at, last_login

    Employee Model:
      - employee_id, name, age, gender, department
      - job_role, monthly_income
      - job_satisfaction, work_life_balance (1-4 scale)
      - years_at_company, years_in_current_role
      - years_since_last_promotion, distance_from_home
      - education, attrition, attrition_risk_score
      - employment_status (Active/Attrited/On Leave)

ATTRITION RISK LEVELS
────────────────────────────────────────────────────────────────────
    Risk Score    Category        Color      Action
    0.00 - 0.33   Low Risk        Green      Standard engagement
    0.33 - 0.67   Medium Risk     Yellow     Monitor and support
    0.67 - 1.00   High Risk       Red        Immediate intervention

FRONT-END TECHNOLOGIES
────────────────────────────────────────────────────────────────────
    ✓ HTML5 / CSS3
    ✓ Bootstrap 5
    ✓ Chart.js (Data Visualization)
    ✓ JavaScript (Interactive)

BACK-END TECHNOLOGIES
────────────────────────────────────────────────────────────────────
    ✓ Flask 2.3.2
    ✓ SQLAlchemy (ORM)
    ✓ SQLite Database
    ✓ Flask-Login (Authentication)
    ✓ Werkzeug (Security)

TROUBLESHOOTING
────────────────────────────────────────────────────────────────────
    Problem: "Module not found"
    Solution: pip install -r requirements.txt

    Problem: "Database locked"
    Solution: Delete employee_attrition.db and restart

    Problem: "Address already in use"
    Solution: Run on different port - python run.py --port 5001

NEXT STEPS
────────────────────────────────────────────────────────────────────
    1. Explore the dashboard with sample data
    2. Add your own employee data
    3. Review analytics and insights
    4. Create retention strategies
    5. Monitor employee attrition trends

FOR DEVELOPMENT
────────────────────────────────────────────────────────────────────
    Install dev dependencies:
      pip install -r requirements-dev.txt

    Run with debug mode:
      FLASK_DEBUG=1 python run.py

    Access Flask shell:
      flask shell

DOCUMENTATION
────────────────────────────────────────────────────────────────────
    See README.md for detailed documentation

═════════════════════════════════════════════════════════════════════
    Happy Coding! For more info, check README.md
═════════════════════════════════════════════════════════════════════
""")
