from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This will be imported from app.py
db = SQLAlchemy()

class Ticket(db.Model):
    """
    Ticket model for storing support tickets
    """
    __tablename__ = 'tickets'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic ticket information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Classification fields
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    status = db.Column(db.String(20), nullable=False, default='Open')
    category = db.Column(db.String(50), nullable=False, default='Other')
    
    # Assignment and contact
    assigned_to = db.Column(db.String(100), nullable=True)
    customer_email = db.Column(db.String(200), nullable=True)
    
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    
    def __init__(self, title, description, priority='Medium', status='Open', 
                 category='Other', assigned_to=None, customer_email=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.category = category
        self.assigned_to = assigned_to
        self.customer_email = customer_email
        self.created_date = datetime.utcnow()
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.title} ({self.status})>'
    
    def to_dict(self):
        """Convert ticket to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'assigned_to': self.assigned_to,
            'customer_email': self.customer_email,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None
        }
    
    @staticmethod
    def get_priority_choices():
        """Get available priority levels"""
        return ['Low', 'Medium', 'High', 'Critical']
    
    @staticmethod
    def get_status_choices():
        """Get available status options"""
        return ['Open', 'In Progress', 'Resolved', 'Closed']
    
    @staticmethod
    def get_category_choices():
        """Get available category options"""
        return ['WiFi', 'VLAN', 'DHCP', 'VPN', 'Hardware', 'Security', 'Other']
    
    def is_overdue(self, hours=24):
        """Check if ticket is overdue based on creation time"""
        if self.status in ['Resolved', 'Closed']:
            return False
        
        time_diff = datetime.utcnow() - self.created_date
        return time_diff.total_seconds() > (hours * 3600)
    
    def get_age_in_hours(self):
        """Get ticket age in hours"""
        time_diff = datetime.utcnow() - self.created_date
        return int(time_diff.total_seconds() / 3600)
    
    def update_status(self, new_status):
        """Update ticket status and set updated_date"""
        if new_status in self.get_status_choices():
            self.status = new_status
            self.updated_date = datetime.utcnow()
            return True
        return False


class KnowledgeBase(db.Model):
    """
    Knowledge Base model for storing troubleshooting articles and guides
    """
    __tablename__ = 'knowledge_base'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Article information
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    
    # Metadata
    author = db.Column(db.String(100), nullable=False, default='System Admin')
    views = db.Column(db.Integer, nullable=False, default=0)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    
    # Status
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    
    def __init__(self, title, content, category, tags=None, author='System Admin'):
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags
        self.author = author
        self.created_date = datetime.utcnow()
        self.views = 0
        self.is_published = True
    
    def __repr__(self):
        return f'<KnowledgeBase {self.id}: {self.title}>'
    
    def to_dict(self):
        """Convert knowledge base article to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'author': self.author,
            'views': self.views,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None,
            'is_published': self.is_published
        }
    
    def increment_views(self):
        """Increment article view count"""
        self.views += 1
        db.session.commit()
    
    def get_tags_list(self):
        """Get tags as a list instead of comma-separated string"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def set_tags_from_list(self, tags_list):
        """Set tags from a list of strings"""
        if tags_list:
            self.tags = ', '.join(tags_list)
        else:
            self.tags = None
    
    @staticmethod
    def get_category_choices():
        """Get available category options"""
        return [
            'WiFi Troubleshooting',
            'VLAN Configuration', 
            'DHCP Issues',
            'VPN Setup',
            'Hardware Problems',
            'Security Configuration',
            'Network Monitoring',
            'General Networking',
            'Meraki Devices',
            'Other'
        ]
    
    @classmethod
    def search(cls, query):
        """Search articles by title, content, or tags"""
        return cls.query.filter(
            db.or_(
                cls.title.contains(query),
                cls.content.contains(query),
                cls.tags.contains(query)
            )
        ).filter_by(is_published=True).all()
    
    @classmethod
    def get_by_category(cls, category):
        """Get all articles in a specific category"""
        return cls.query.filter_by(category=category, is_published=True).all()
    
    @classmethod
    def get_popular_articles(cls, limit=5):
        """Get most viewed articles"""
        return cls.query.filter_by(is_published=True).order_by(cls.views.desc()).limit(limit).all()


class User(db.Model):
    """
    User model for authentication and user management
    """
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User information
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    
    # Authentication
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role and permissions
    role = db.Column(db.String(50), nullable=False, default='support_agent')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, username, email, full_name, password_hash, role='support_agent'):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password_hash = password_hash
        self.role = role
        self.created_date = datetime.utcnow()
        self.is_active = True
    
    def __repr__(self):
        return f'<User {self.username}: {self.full_name}>'
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization (excluding sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @staticmethod
    def get_role_choices():
        """Get available user roles"""
        return ['admin', 'supervisor', 'support_agent', 'read_only']
    
    def has_permission(self, permission):
        """Check if user has specific permission based on role"""
        permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'manage_users'],
            'supervisor': ['create', 'read', 'update', 'delete'],
            'support_agent': ['create', 'read', 'update'],
            'read_only': ['read']
        }
        return permission in permissions.get(self.role, [])
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()


# Database utility functions
def init_database():
    """Initialize database with tables"""
    db.create_all()
    print("Database tables created successfully!")

def drop_all_tables():
    """Drop all database tables (use with caution!)"""
    db.drop_all()
    print("All database tables dropped!")

def get_database_stats():
    """Get basic database statistics"""
    stats = {
        'total_tickets': Ticket.query.count(),
        'total_kb_articles': KnowledgeBase.query.count(),
        'total_users': User.query.count(),
        'open_tickets': Ticket.query.filter_by(status='Open').count(),
        'resolved_tickets': Ticket.query.filter_by(status='Resolved').count()
    }
    return stats