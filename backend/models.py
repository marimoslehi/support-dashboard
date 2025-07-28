from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), nullable=False, default='Medium')
    status = db.Column(db.String(50), nullable=False, default='Open')
    category = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100))
    customer_email = db.Column(db.String(120), nullable=False)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime)

class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(255))
    author = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
