from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Clear existing users
    User.query.delete()
    
    # Create sample users
    users = [
        {
            'username': 'admin',
            'email': 'admin@company.com',
            'full_name': 'System Administrator',
            'password': 'admin123',
            'role': 'Admin'
        },
        {
            'username': 'jsmith',
            'email': 'john.smith@company.com',
            'full_name': 'John Smith',
            'password': 'password123',
            'role': 'Senior Engineer'
        },
        {
            'username': 'mjohnson',
            'email': 'mary.johnson@company.com',
            'full_name': 'Mary Johnson',
            'password': 'password123',
            'role': 'Network Engineer'
        },
        {
            'username': 'bwilson',
            'email': 'bob.wilson@company.com',
            'full_name': 'Bob Wilson',
            'password': 'password123',
            'role': 'Support Specialist'
        },
        {
            'username': 'sgarcia',
            'email': 'sara.garcia@company.com',
            'full_name': 'Sara Garcia',
            'password': 'password123',
            'role': 'Junior Engineer'
        }
    ]
    
    for user_data in users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            full_name=user_data['full_name'],
            password_hash=generate_password_hash(user_data['password']),
            role=user_data['role']
        )
        db.session.add(user)
    
    db.session.commit()
    print("✅ Users created successfully!")
    print("🔐 You can now login with:")
    for user_data in users:
        print(f"   {user_data['username']} / {user_data['password']}")
