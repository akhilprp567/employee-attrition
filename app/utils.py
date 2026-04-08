"""
Utility functions for the Employee Attrition System
"""

from datetime import datetime
from app.models.employee import Employee
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def calculate_attrition_risk(employee):
    """
    Calculate attrition risk score for an employee based on various factors
    
    Args:
        employee: Employee object
        
    Returns:
        float: Risk score between 0 and 1
    """
    if not employee:
        return None
    
    # Initialize risk score components
    risk_score = 0
    weight_sum = 0
    
    # Factor 1: Years at company (lower is riskier)
    if employee.years_at_company is not None:
        # New hires are at higher risk
        years_factor = max(0, 3 - employee.years_at_company) / 3
        risk_score += years_factor * 0.20
        weight_sum += 0.20
    
    # Factor 2: Job satisfaction (lower satisfaction = higher risk)
    if employee.years_at_company is not None:
        satisfaction_factor = 1 - (employee.job_satisfaction / 4)
        risk_score += satisfaction_factor * 0.25
        weight_sum += 0.25
    
    # Factor 3: Work-life balance (poor balance = higher risk)
    if employee.work_life_balance is not None:
        balance_factor = 1 - (employee.work_life_balance / 4)
        risk_score += balance_factor * 0.20
        weight_sum += 0.20
    
    # Factor 4: Salary (lower salary = higher risk to leave)
    if employee.monthly_income is not None:
        avg_salary = Employee.query.filter(
            Employee.monthly_income.isnot(None)
        ).all()
        if avg_salary:
            avg = sum(e.monthly_income for e in avg_salary) / len(avg_salary)
            salary_factor = 1 - (min(employee.monthly_income, avg) / avg)
            risk_score += salary_factor * 0.15
            weight_sum += 0.15
    
    # Factor 5: Distance from home (longer distance = higher risk)
    if employee.distance_from_home is not None:
        distance_factor = min(employee.distance_from_home / 50, 1)
        risk_score += distance_factor * 0.10
        weight_sum += 0.10
    
    # Factor 6: Promotion history (no recent promotion = higher risk)
    if employee.years_since_last_promotion is not None:
        promotion_factor = min(employee.years_since_last_promotion / 5, 1)
        risk_score += promotion_factor * 0.10
        weight_sum += 0.10
    
    # Normalize risk score
    if weight_sum > 0:
        risk_score = risk_score / weight_sum
    
    # Clip to 0-1 range
    risk_score = max(0, min(1, risk_score))
    
    return round(risk_score, 3)

def get_risk_category(risk_score):
    """
    Get risk category based on risk score
    
    Args:
        risk_score: float between 0 and 1
        
    Returns:
        str: 'Low Risk', 'Medium Risk', or 'High Risk'
    """
    if risk_score is None:
        return 'Unknown'
    elif risk_score < 0.33:
        return 'Low Risk'
    elif risk_score < 0.67:
        return 'Medium Risk'
    else:
        return 'High Risk'

def get_retention_recommendations(employee):
    """
    Get retention recommendations for an employee
    
    Args:
        employee: Employee object
        
    Returns:
        list: List of recommended actions
    """
    recommendations = []
    
    if employee.work_life_balance and employee.work_life_balance <= 1:
        recommendations.append('Improve work-life balance through flexible arrangements')
    
    if employee.job_satisfaction and employee.job_satisfaction <= 1:
        recommendations.append('Schedule career development discussion')
    
    if employee.years_at_company and employee.years_at_company <= 1:
        recommendations.append('Assign mentorship program for new employee retention')
    
    if employee.distance_from_home and employee.distance_from_home >= 40:
        recommendations.append('Consider remote work options')
    
    if employee.years_since_last_promotion and employee.years_since_last_promotion >= 4:
        recommendations.append('Plan career advancement or promotion opportunities')
    
    if not recommendations:
        recommendations.append('Continue regular engagement and development programs')
    
    return recommendations

def format_currency(amount):
    """Format amount as Indian Rupees"""
    if amount is None:
        return 'N/A'
    return f'₹{amount:,.0f}'

def format_percentage(value):
    """Format value as percentage"""
    if value is None:
        return 'N/A'
    return f'{value:.1f}%'

def get_employment_status_badge(status):
    """Get badge class for employment status"""
    status_map = {
        'Active': 'bg-success',
        'Attrited': 'bg-danger',
        'On Leave': 'bg-warning'
    }
    return status_map.get(status, 'bg-secondary')

def get_age_group(age):
    """Get age group category"""
    if age is None:
        return 'Unknown'
    elif age <= 25:
        return '18-25'
    elif age <= 35:
        return '26-35'
    elif age <= 45:
        return '36-45'
    elif age <= 55:
        return '46-55'
    else:
        return '55+'

def calculate_department_attrition_rate(department):
    """Calculate attrition rate for a department"""
    employees = Employee.query.filter_by(department=department).all()
    if not employees:
        return 0
    
    attrited = sum(1 for e in employees if e.attrition)
    return (attrited / len(employees)) * 100
