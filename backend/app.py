from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
import os
from functools import wraps

# Initialize Flask app with correct template and static folder paths
app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///support_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize database AFTER app configuration
from models import db, Ticket, KnowledgeBase, User
db.init_app(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """Main dashboard page"""
    # Get dashboard statistics
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    in_progress = Ticket.query.filter_by(status='In Progress').count()
    resolved_tickets = Ticket.query.filter_by(status='Resolved').count()
    closed_tickets = Ticket.query.filter_by(status='Closed').count()
    
    # Get recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.created_date.desc()).limit(5).all()
    
    # Get priority distribution
    critical_count = Ticket.query.filter_by(priority='Critical').count()
    high_count = Ticket.query.filter_by(priority='High').count()
    medium_count = Ticket.query.filter_by(priority='Medium').count()
    low_count = Ticket.query.filter_by(priority='Low').count()
    
    # Get current user
    current_user = User.query.get(session['user_id'])
    
    stats = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress': in_progress,
        'resolved_tickets': resolved_tickets,
        'closed_tickets': closed_tickets,
        'critical_count': critical_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count
    }
    
    return render_template('dashboard.html', stats=stats, recent_tickets=recent_tickets, current_user=current_user)

@app.route('/tickets')
@login_required
def tickets():
    """Tickets page"""
    return render_template('tickets.html')

@app.route('/tickets/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    """Ticket detail page"""
    return render_template('ticket_detail.html')

@app.route('/tickets/new')
@login_required
def new_ticket():
    """New ticket page"""
    return render_template('ticket_form.html')

@app.route('/knowledge-base')
@login_required
def knowledge_base():
    """Knowledge base page"""
    return render_template('knowledge_base.html')

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("✅ Database tables ready!")
        print("🚀 Starting Customer Support Dashboard...")
        print("📍 Access the application at: http://localhost:8000")
        print("🔐 Login with: admin / admin123")
    
    # Run the Flask development server
    app.run(debug=True, host='127.0.0.1', port=8000)
