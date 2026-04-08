from app import db
from datetime import datetime


class Employee(db.Model):
    """Employee model for storing employee data"""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)

    # 🔹 BASIC INFO
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)

    # 🔹 JOB DETAILS
    department = db.Column(db.String(100), nullable=True)
    job_role = db.Column(db.String(100), nullable=True)
    monthly_income = db.Column(db.Float, default=0.0)

    # 🔹 PERFORMANCE / HR METRICS
    job_satisfaction = db.Column(db.Integer, default=3)
    work_life_balance = db.Column(db.Integer, default=3)
    years_at_company = db.Column(db.Integer, default=0)
    years_in_current_role = db.Column(db.Integer, default=0)
    years_since_last_promotion = db.Column(db.Integer, default=0)
    distance_from_home = db.Column(db.Integer, default=0)

    # 🔹 EDUCATION
    education = db.Column(db.String(50), nullable=True)

    # 🔥 AI OUTPUT
    attrition = db.Column(db.Boolean, default=False)
    attrition_risk_score = db.Column(db.Float, default=0.0)
    attrition_reason = db.Column(db.String(255), nullable=True)

    # 🔹 STATUS
    employment_status = db.Column(db.String(20), default='Active')

    # 🔹 DATES
    hire_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ================= REPRESENT =================
    def __repr__(self):
        return f'<Employee {self.name}>'

    # ================= RISK CATEGORY =================
    def get_risk_category(self):
        """Return risk category based on ML score"""
        score = self.attrition_risk_score or 0

        if score < 0.25:
            return 'Low'
        elif score < 0.6:
            return 'Medium'
        else:
            return 'High'

    # ================= RISK COLOR (FOR UI) =================
    def get_risk_color(self):
        """Return Bootstrap color class"""
        score = self.attrition_risk_score or 0

        if score < 0.25:
            return 'success'   # Green
        elif score < 0.6:
            return 'warning'   # Yellow
        else:
            return 'danger'    # Red

    # ================= SALARY DISPLAY =================
    def get_salary_display(self):
        """Formatted salary"""
        try:
            return f"₹{int(self.monthly_income):,}" if self.monthly_income else "N/A"
        except:
            return "N/A"

    # ================= RISK PERCENT =================
    def get_risk_percentage(self):
        """Return risk in percentage"""
        score = self.attrition_risk_score or 0
        return round(score * 100, 2)