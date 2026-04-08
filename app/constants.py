"""
Configuration for ML models and utilities
"""

import pickle
import json
from pathlib import Path
from sklearn.preprocessing import StandardScaler

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'dataset'
MODEL_DIR = PROJECT_ROOT / 'ml_model'
LOG_DIR = PROJECT_ROOT / 'logs'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Feature names for ML model
FEATURE_NAMES = [
    'age',
    'job_satisfaction',
    'work_life_balance',
    'years_at_company',
    'years_in_current_role',
    'years_since_last_promotion',
    'distance_from_home',
    'monthly_income'
]

# Employee attributes
EMPLOYEE_ATTRIBUTES = {
    'age': 'Age (years)',
    'gender': 'Gender',
    'department': 'Department',
    'job_role': 'Job Role',
    'monthly_income': 'Monthly Income (₹)',
    'job_satisfaction': 'Job Satisfaction (1-4)',
    'work_life_balance': 'Work-Life Balance (1-4)',
    'years_at_company': 'Tenure (years)',
    'years_in_current_role': 'Years in Role',
    'years_since_last_promotion': 'Years Since Promotion',
    'distance_from_home': 'Distance from Home (km)',
    'education': 'Education'
}

# Risk thresholds
RISK_THRESHOLDS = {
    'low': (0.0, 0.33),
    'medium': (0.33, 0.67),
    'high': (0.67, 1.0)
}

# Department list
DEPARTMENTS = [
    'Human Resources',
    'Sales',
    'IT',
    'Finance',
    'Operations',
    'Marketing'
]

# Job roles
JOB_ROLES = [
    'Senior Developer',
    'Junior Developer',
    'Manager',
    'Executive',
    'Analyst',
    'Specialist',
    'Coordinator',
    'Director'
]

# Education levels
EDUCATION_LEVELS = [
    'High School',
    'Bachelor',
    'Master',
    'PhD'
]

# Employment statuses
EMPLOYMENT_STATUSES = [
    'Active',
    'Attrited',
    'On Leave'
]

# Role types in system
USER_ROLES = [
    'hr_staff',
    'manager',
    'admin'
]
