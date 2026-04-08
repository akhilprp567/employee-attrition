from app import login_manager
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for login manager"""
    return User.query.get(int(user_id))
