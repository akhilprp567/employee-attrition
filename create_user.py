from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(
        username="demo",
        email="demo@gmail.com",
        full_name="Demo User",
        department="IT",
        role="admin"
    )

    user.set_password("demo123")

    db.session.add(user)
    db.session.commit()

    print("✅ Fresh user created")