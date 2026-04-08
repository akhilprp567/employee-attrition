
# Employee Attrition Prediction & HR Analytics System

A comprehensive machine learning-based HR analytics platform for predicting employee attrition and providing actionable insights to HR departments.

## 📋 Features

### ✅ Authentication System
- User registration (signup)
- Secure login with password hashing
- Role-based access control (HR Staff, Manager, Admin)
- Session management

### 📊 Dashboard
- Real-time employee attrition metrics
- Visual analytics with interactive charts
- Key performance indicators (KPIs)
- Department-wise employee distribution
- Age group analysis
- Risk assessment overview

### 👥 Employee Management
- Complete employee database with 30+ attributes
- Advanced filtering and search
- Individual employee detail pages
- Attrition risk scoring and categorization
- Employment status tracking

### 📈 Advanced Analytics
- Job role analysis
- Salary bracket analysis
- Experience-based attrition trends
- Interactive data visualizations
- Exportable insights

### 🚨 Risk Assessment
- Machine learning-based risk prediction
- Three-tier risk categorization (Low, Medium, High)
- Probability scores (0-1 scale)
- Actionable recommendations for HR

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.2
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with secure password hashing
- **Migration**: Flask-Migrate

### Frontend
- **HTML5/CSS3**: Custom responsive design
- **Bootstrap 5**: UI components and grid system
- **JavaScript**: Interactive features
- **Chart.js**: Data visualization

### Machine Learning & Data Science
- **Scikit-learn**: ML algorithms
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib & Seaborn**: Data visualization

## 📦 Project Structure

```
Employee/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User model (authentication)
│   │   └── employee.py            # Employee model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                # Login/Signup routes
│   │   └── dashboard.py           # Dashboard routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Custom styles
│   │   ├── js/                    # JavaScript files
│   │   └── images/                # Image assets
│   └── templates/
│       ├── base.html              # Base template
│       ├── login.html             # Login page
│       ├── signup.html            # Registration page
│       ├── dashboard.html         # Main dashboard
│       ├── employees.html         # Employees list
│       ├── employee_detail.html   # Employee details
│       └── analytics.html         # Analytics page
├── ml_model/                       # ML models (for future)
├── dataset/                        # Data files
├── config.py                       # Configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone or extract the project**
   ```bash
   cd Employee
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python run.py
   # Then run in another terminal:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   flask seed-db  # Add sample data
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Open browser and go to: `http://localhost:5000`
   - Default credentials:
     - **Username**: demo
     - **Password**: demo123

## 📊 Database Schema

### Users Table
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- full_name
- role (hr_staff, manager, admin)
- department
- is_active
- created_at
- last_login
```

### Employees Table
```sql
- id (Primary Key)
- employee_id (Unique)
- name
- age
- gender
- department
- job_role
- monthly_income
- job_satisfaction (1-4)
- work_life_balance (1-4)
- years_at_company
- years_in_current_role
- years_since_last_promotion
- distance_from_home
- education
- attrition (Boolean)
- attrition_risk_score (0-1)
- employment_status
- hire_date
- created_at
- updated_at
```

## 🔐 Security Features

- Password hashing with werkzeug
- Session management with Flask-Login
- CSRF protection on forms
- SQLAlchemy ORM prevents SQL injection
- Environment-based configuration
- Input validation and sanitization

## 📈 Attrition Risk Scoring

Risk scores are calculated on a scale of 0 to 1:

| Score Range | Category | Action |
|------------|----------|--------|
| 0.00 - 0.33 | Low Risk | Standard engagement |
| 0.33 - 0.67 | Medium Risk | Monitor and support |
| 0.67 - 1.00 | High Risk | Immediate intervention |

## 🎯 Key Metrics Tracked

- **Total Employees**: Complete headcount
- **Attrition Rate**: Percentage of employees who left
- **High-Risk Count**: Employees scoring >= 0.67
- **Retention Rate**: Employees likely to stay
- **Average Salary**: Department-wise compensation
- **Department Distribution**: Employee count by department
- **Experience Analysis**: Correlation between tenure and attrition

## 🔧 Configuration

Edit `.env` file to configure:

```env
FLASK_ENV=development          # development or production
FLASK_DEBUG=True               # Enable debug mode
SECRET_KEY=your-key            # Flask secret key
DATABASE_URL=sqlite:///employee_attrition.db
```

## 📝 API Endpoints

### Authentication
- `GET /auth/signup` - Sign up page
- `POST /auth/signup` - Create new account
- `GET /auth/login` - Login page
- `POST /auth/login` - Authenticate user
- `GET /auth/logout` - Logout user

### Dashboard
- `GET /dashboard/` - Main dashboard
- `GET /dashboard/employees` - Employees list
- `GET /dashboard/employee/<id>` - Employee details
- `GET /dashboard/analytics` - Advanced analytics
- `GET /dashboard/api/dashboard-stats` - API for stats

## 🤖 Future Enhancements

- [ ] Advanced ML models (Random Forest, XGBoost, Neural Networks)
- [ ] Real-time data ingestion
- [ ] Automated retention recommendations
- [ ] Mobile application
- [ ] REST API
- [ ] Integration with HRIS systems
- [ ] Export reports (PDF, Excel)
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Dark mode UI

## 📊 Sample Data

The application comes with pre-loaded sample employees for testing. Use the `flask seed-db` command to populate sample data.

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm employee_attrition.db
flask db init
flask db migrate
flask db upgrade
flask seed-db
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Run on different port
python run.py --port 5001
```

## 📄 License

This project is confidential and proprietary. Unauthorized copying or distribution is prohibited.

## 👥 Author

HR Analytics Development Team

## 📞 Support

For issues or suggestions, please contact the development team.

---

**Last Updated**: April 2026
**Version**: 1.0.0
