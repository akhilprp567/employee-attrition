from app import create_app, db
from app.models.user import User

app = create_app()

# 🔥 AUTO CREATE DB + DEMO USER
with app.app_context():
    try:
        db.create_all()
        print("✅ Database created")

        # Create demo user if not exists
        user = User.query.filter_by(username="demo").first()

        if not user:
            demo_user = User(
                username="demo",
                email="demo@gmail.com",
                full_name="Demo User",
                department="IT",
                role="admin"
            )
            demo_user.set_password("demo123")

            db.session.add(demo_user)
            db.session.commit()

            print("✅ Demo user created (demo/demo123)")
        else:
            print("ℹ️ Demo user already exists")

    except Exception as e:
        print("❌ DB ERROR:", e)
        db.session.rollback()


if __name__ == "__main__":
    app.run(debug=True)