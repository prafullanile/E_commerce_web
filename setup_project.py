# setup_project.py
from market import app, db
from market.models import User, Item

with app.app_context():

    print("✅ Creating database tables...")
    db.drop_all()               # Remove old tables (safe for development)
    db.create_all()             # Create fresh tables
    print("✅ Tables created successfully!")

    # ----------------------------------
    # Create Admin User
    # ----------------------------------
    print("✅ Creating admin user...")

    admin = User(
        username="admin",
        email_address="admin@example.com",
        password="admin123",     # Auto hashed
        is_admin=True,
        budget=999999
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created!  (username: admin, password: admin123)")

    # ----------------------------------
    # Insert Sample Items
    # ----------------------------------
    print("✅ Adding sample products...")

    items = [
        Item(
            name="Laptop",
            price=800,
            barcode="123456789111",
            description="High-performance laptop suitable for work and gaming."
        ),
        Item(
            name="iPhone 14",
            price=1200,
            barcode="999999999222",
            description="Latest generation smartphone from Apple."
        ),
        Item(
            name="Headphones",
            price=150,
            barcode="888888888333",
            description="Noise-cancelling over-ear headphones."
        ),
        Item(
            name="Smart Watch",
            price=300,
            barcode="777777777444",
            description="Fitness tracker and smartwatch with long battery life."
        ),
    ]

    db.session.add_all(items)
    db.session.commit()

    print("✅ Sample items added!")
    print("\n🎉 Setup completed successfully! Your application is ready.\n")
