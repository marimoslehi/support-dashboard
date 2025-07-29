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
    current_user = User.query.filter_by(id=session['user_id']).first()
    
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
    """Tickets management page"""
    # Get filter parameters
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Build query
    query = Ticket.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)
    if search_query:
        query = query.filter(Ticket.title.contains(search_query) | 
                           Ticket.description.contains(search_query))
    
    tickets_list = query.order_by(Ticket.created_date.desc()).all()
    
    # Get unique categories for filter dropdown
    categories = db.session.query(Ticket.category.distinct()).all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('tickets.html', 
                         tickets=tickets_list,
                         categories=categories,
                         current_status=status_filter,
                         current_priority=priority_filter,
                         current_category=category_filter,
                         search_query=search_query)

@app.route('/tickets/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    """Individual ticket detail page"""
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Get engineers for assignment dropdown
    engineers = User.query.filter(
        User.role.in_(['Senior Engineer', 'Network Engineer', 'Support Specialist', 'Junior Engineer', 'Admin'])
    ).all()

    return render_template('ticket_detail.html', ticket=ticket, engineers=engineers)

@app.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    """Create new ticket page"""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title')
            description = request.form.get('description')
            priority = request.form.get('priority')
            category = request.form.get('category')
            customer_email = request.form.get('customer_email')
            
            # Validate required fields
            if not all([title, description, priority, category, customer_email]):
                flash('Please fill in all required fields.', 'error')
                return render_template('ticket_form.html')
            
            # Create new ticket
            ticket = Ticket(
                title=title,
                description=description,
                priority=priority,
                status='Open',
                category=category,
                customer_email=customer_email,
                created_date=datetime.now(timezone.utc)
            )
            
            # Save to database
            db.session.add(ticket)
            db.session.commit()
            
            flash(f'Ticket #{ticket.id} created successfully!', 'success')
            return redirect(url_for('tickets'))
            
        except Exception as e:
            flash(f'Error creating ticket: {str(e)}', 'error')
            db.session.rollback()
            return render_template('ticket_form.html')
    
    # GET request - show the form
    return render_template('ticket_form.html')

@app.route('/knowledge-base')
@login_required
def knowledge_base():
    """Knowledge base page"""
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    query = KnowledgeBase.query
    
    if search_query:
        query = query.filter(KnowledgeBase.title.contains(search_query) | 
                           KnowledgeBase.content.contains(search_query) |
                           KnowledgeBase.tags.contains(search_query))
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    articles = query.order_by(KnowledgeBase.created_date.desc()).all()
    
    # Get unique categories for filter dropdown
    categories = db.session.query(KnowledgeBase.category.distinct()).all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('knowledge_base.html', 
                         articles=articles,
                         categories=categories,
                         current_category=category_filter,
                         search_query=search_query)

@app.route('/knowledge-base/new', methods=['GET', 'POST'])
@login_required
def new_knowledge_article():
    """Create new knowledge base article"""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title')
            content = request.form.get('content')
            category = request.form.get('category')
            tags = request.form.get('tags', '')
            author = session.get('full_name', 'Unknown')
            
            # Validate required fields
            if not all([title, content, category]):
                flash('Please fill in all required fields.', 'error')
                return render_template('knowledge_base.html')
            
            # Create new article
            article = KnowledgeBase(
                title=title,
                content=content,
                category=category,
                tags=tags,
                author=author,
                created_date=datetime.now(timezone.utc)
            )
            
            # Save to database
            db.session.add(article)
            db.session.commit()
            
            flash(f'Article "{title}" created successfully!', 'success')
            return redirect(url_for('knowledge_base'))
            
        except Exception as e:
            flash(f'Error creating article: {str(e)}', 'error')
            db.session.rollback()
            return redirect(url_for('knowledge_base'))
    
    return redirect(url_for('knowledge_base'))

@app.route('/knowledge-base/<int:article_id>')
@login_required
def knowledge_article(article_id):
    """View individual knowledge base article"""
    article = KnowledgeBase.query.get_or_404(article_id)
    return render_template('knowledge_article.html', article=article)

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/tickets/<int:ticket_id>/update', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    """Update ticket via form submission"""
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if 'status' in request.form:
        ticket.status = request.form['status']
    if 'priority' in request.form:
        ticket.priority = request.form['priority']
    if 'assigned_to' in request.form:
        ticket.assigned_to = request.form['assigned_to']
    
    ticket.updated_date = datetime.now(timezone.utc)
    db.session.commit()
    
    flash('Ticket updated successfully!', 'success')
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))


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
