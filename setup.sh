#!/bin/bash

# Employee Attrition Prediction System - Setup Script

echo "=========================================="
echo "Employee Attrition System - Setup Script"
echo "=========================================="
echo ""

# Check Python installation
echo "1. Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "2. Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "3. Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "4. Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create database
echo "5. Initializing database..."
python3 -c "
from app import create_app, db
from app.models.user import User
from app.models.employee import Employee

app = create_app()
with app.app_context():
    db.create_all()
    print('✓ Database tables created')
    
    # Create demo user
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@example.com',
            full_name='Demo User',
            department='Human Resources',
            role='admin'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        print('✓ Demo user created')
"
echo ""

# Summary
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the application:"
echo "     python run.py"
echo "  3. Open browser at http://localhost:5000"
echo ""
echo "Default Credentials:"
echo "  Username: demo"
echo "  Password: demo123"
echo ""
echo "=========================================="
