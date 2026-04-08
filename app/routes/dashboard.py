from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.employee import Employee
from app.models.contact import Contact
from sqlalchemy import func
from app.ml_model import predict

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# ================= DASHBOARD =================
@dashboard_bp.route('/')
@login_required
def index():
    employees = Employee.query.all()

    total = len(employees)

    # 🔥 ATTRITION (>= 0.25)
    attrited = len([e for e in employees if (e.attrition_risk_score or 0) >= 0.25])
    attrition_rate = (attrited / total * 100) if total else 0

    # 🔥 RISK SEGMENTATION
    high_risk = len([e for e in employees if (e.attrition_risk_score or 0) >= 0.6])
    medium_risk = len([e for e in employees if 0.25 <= (e.attrition_risk_score or 0) < 0.6])
    low_risk = len([e for e in employees if (e.attrition_risk_score or 0) < 0.25])

    # AVG SALARY
    avg_salary = db.session.query(func.avg(Employee.monthly_income)).scalar() or 0

    # AGE GROUPS
    age_groups = {"20-30": 0, "30-40": 0, "40-50": 0, "50+": 0}
    for e in employees:
        if e.age:
            if e.age < 30:
                age_groups["20-30"] += 1
            elif e.age < 40:
                age_groups["30-40"] += 1
            elif e.age < 50:
                age_groups["40-50"] += 1
            else:
                age_groups["50+"] += 1

    # DEPARTMENT COUNT
    dept_data = dict(db.session.query(
        Employee.department,
        func.count(Employee.id)
    ).group_by(Employee.department).all())

    # SALARY BY DEPT
    salary_data_dept = {
        d[0]: float(d[1] or 0)
        for d in db.session.query(
            Employee.department,
            func.avg(Employee.monthly_income)
        ).group_by(Employee.department).all()
    }

    # TOP RISK
    at_risk_employees = Employee.query \
        .filter(Employee.attrition_risk_score != None) \
        .order_by(Employee.attrition_risk_score.desc()) \
        .limit(5).all()

    return render_template(
        'dashboard.html',
        total_employees=total,
        total_attrited=attrited,
        attrition_rate=round(attrition_rate, 2),
        high_risk_count=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        avg_salary=round(avg_salary, 2),
        age_groups=age_groups,
        dept_data=dept_data,
        salary_data_dept=salary_data_dept,
        at_risk_employees=at_risk_employees,
        employees=employees
    )


# ================= ANALYTICS (🔥 NEW FULL PAGE) =================
@dashboard_bp.route('/analytics')
@login_required
def analytics():
    employees = Employee.query.all()

    total = len(employees)
    attrited = len([e for e in employees if (e.attrition_risk_score or 0) >= 0.25])

    avg_salary = db.session.query(func.avg(Employee.monthly_income)).scalar() or 0

    # JOB ROLE ANALYSIS
    role_data = db.session.query(
        Employee.job_role,
        func.count(Employee.id),
        func.avg(Employee.attrition_risk_score)
    ).group_by(Employee.job_role).all()

    role_labels = [r[0] for r in role_data]
    role_counts = [r[1] for r in role_data]
    role_risk = [round((r[2] or 0) * 100, 2) for r in role_data]

    # SALARY DISTRIBUTION
    salary_brackets = {"0-20K": 0, "20K-40K": 0, "40K-60K": 0, "60K+": 0}
    for e in employees:
        if e.monthly_income:
            if e.monthly_income < 20000:
                salary_brackets["0-20K"] += 1
            elif e.monthly_income < 40000:
                salary_brackets["20K-40K"] += 1
            elif e.monthly_income < 60000:
                salary_brackets["40K-60K"] += 1
            else:
                salary_brackets["60K+"] += 1

    # EXPERIENCE DATA
    experience_data = {}
    for e in employees:
        yrs = int(e.years_at_company or 0)
        experience_data[yrs] = experience_data.get(yrs, 0) + 1

    return render_template(
        'analytics.html',
        total=total,
        attrited=attrited,
        avg_salary=round(avg_salary, 2),
        role_labels=role_labels,
        role_counts=role_counts,
        role_risk=role_risk,
        salary_brackets=salary_brackets,
        experience_data=experience_data
    )


# ================= EMPLOYEES =================
@dashboard_bp.route('/employees')
@login_required
def employees():
    employees = Employee.query.all()
    departments = [d[0] for d in db.session.query(Employee.department).distinct().all() if d[0]]

    return render_template('employees.html', employees=employees, departments=departments)


# ================= ADD EMPLOYEE =================
@dashboard_bp.route('/add-employee', methods=['POST'])
@login_required
def add_employee():
    try:
        data = {
            "Age": int(request.form.get("age", 30)),
            "MonthlyIncome": float(request.form.get("monthly_income", 30000)),
            "JobSatisfaction": int(request.form.get("job_satisfaction", 3)),
            "WorkLifeBalance": int(request.form.get("work_life_balance", 3)),
            "YearsAtCompany": int(request.form.get("years_at_company", 3)),
            "YearsInCurrentRole": int(request.form.get("years_in_role", 2)),
            "YearsSinceLastPromotion": int(request.form.get("years_since_promotion", 1)),
            "DistanceFromHome": int(request.form.get("distance", 5)),
            "JobRole": request.form.get("job_role"),
            "Department": request.form.get("department")
        }

        pred, prob, reason = predict(data)

        emp = Employee(
            employee_id=request.form.get('employee_id'),
            name=request.form.get('name'),
            age=data["Age"],
            department=data["Department"],
            job_role=data["JobRole"],
            monthly_income=data["MonthlyIncome"],
            years_at_company=data["YearsAtCompany"],
            attrition=True if prob >= 0.25 else False,
            attrition_risk_score=float(prob),
            employment_status="Active",
            attrition_reason=reason
        )

        db.session.add(emp)
        db.session.commit()

        flash(f"🤖 Risk: {round(prob*100,2)}% | {reason}", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ {str(e)}", "danger")

    return redirect(url_for('dashboard.index'))


# ================= CONTACT =================
@dashboard_bp.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        try:
            contact = Contact(
                name=request.form.get('name'),
                email=request.form.get('email'),
                message=request.form.get('message')
            )

            db.session.add(contact)
            db.session.commit()

            flash("✅ Message sent successfully!", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"❌ {str(e)}", "danger")

        return redirect(url_for('dashboard.contact'))

    return render_template('contact.html')


# ================= ABOUT =================
@dashboard_bp.route('/about')
@login_required
def about():
    return render_template('about.html')

# ================= DELETE =================
@dashboard_bp.route('/delete-employee/<int:id>')
@login_required
def delete_employee(id):
    try:
        emp = Employee.query.get_or_404(id)
        db.session.delete(emp)
        db.session.commit()

        flash("🗑️ Employee deleted successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ {str(e)}", "danger")

    return redirect(url_for('dashboard.employees'))

# ================= EDIT EMPLOYEE =================
@dashboard_bp.route('/edit-employee/<int:id>', methods=['POST'])
@login_required
def edit_employee(id):
    try:
        emp = Employee.query.get_or_404(id)

        emp.name = request.form.get('name')
        emp.age = int(request.form.get('age', 0))
        emp.department = request.form.get('department')
        emp.job_role = request.form.get('job_role')
        emp.monthly_income = float(request.form.get('monthly_income', 0))

        db.session.commit()

        flash("✅ Employee updated successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ {str(e)}", "danger")

    return redirect(url_for('dashboard.employees'))