from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///support_dashboard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization
from models import Ticket, KnowledgeBase

# ============== WEB ROUTES (Frontend) ==============

@app.route('/')
def dashboard():
    """Main dashboard page"""
    # Get dashboard statistics
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    in_progress = Ticket.query.filter_by(status='In Progress').count()
    resolved_tickets = Ticket.query.filter_by(status='Resolved').count()
    
    # Get recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.created_date.desc()).limit(5).all()
    
    # Get priority distribution
    critical_count = Ticket.query.filter_by(priority='Critical').count()
    high_count = Ticket.query.filter_by(priority='High').count()
    medium_count = Ticket.query.filter_by(priority='Medium').count()
    low_count = Ticket.query.filter_by(priority='Low').count()
    
    stats = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress': in_progress,
        'resolved_tickets': resolved_tickets,
        'critical_count': critical_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count
    }
    
    return render_template('dashboard.html', stats=stats, recent_tickets=recent_tickets)

@app.route('/tickets')
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
    
    return render_template('tickets.html', tickets=tickets_list)

@app.route('/tickets/<int:ticket_id>')
def ticket_detail(ticket_id):
    """Individual ticket detail page"""
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket_detail.html', ticket=ticket)

@app.route('/tickets/new')
def new_ticket():
    """Create new ticket page"""
    return render_template('ticket_form.html')

@app.route('/knowledge-base')
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
    
    return render_template('knowledge_base.html', articles=articles)

# ============== API ROUTES (Backend) ==============

@app.route('/api/tickets', methods=['GET'])
def api_get_tickets():
    """Get all tickets via API"""
    tickets = Ticket.query.order_by(Ticket.created_date.desc()).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'priority': t.priority,
        'status': t.status,
        'category': t.category,
        'created_date': t.created_date.isoformat(),
        'updated_date': t.updated_date.isoformat() if t.updated_date else None,
        'assigned_to': t.assigned_to,
        'customer_email': t.customer_email
    } for t in tickets])

@app.route('/api/tickets', methods=['POST'])
def api_create_ticket():
    """Create new ticket via API"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    ticket = Ticket(
        title=data['title'],
        description=data['description'],
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'Open'),
        category=data.get('category', 'Other'),
        assigned_to=data.get('assigned_to'),
        customer_email=data.get('customer_email'),
        created_date=datetime.utcnow()
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify({
        'id': ticket.id,
        'title': ticket.title,
        'status': ticket.status,
        'message': 'Ticket created successfully'
    }), 201

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def api_get_ticket(ticket_id):
    """Get specific ticket via API"""
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify({
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'priority': ticket.priority,
        'status': ticket.status,
        'category': ticket.category,
        'created_date': ticket.created_date.isoformat(),
        'updated_date': ticket.updated_date.isoformat() if ticket.updated_date else None,
        'assigned_to': ticket.assigned_to,
        'customer_email': ticket.customer_email
    })

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def api_update_ticket(ticket_id):
    """Update ticket via API"""
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'title' in data:
        ticket.title = data['title']
    if 'description' in data:
        ticket.description = data['description']
    if 'priority' in data:
        ticket.priority = data['priority']
    if 'status' in data:
        ticket.status = data['status']
    if 'category' in data:
        ticket.category = data['category']
    if 'assigned_to' in data:
        ticket.assigned_to = data['assigned_to']
    if 'customer_email' in data:
        ticket.customer_email = data['customer_email']
    
    ticket.updated_date = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': ticket.id,
        'message': 'Ticket updated successfully'
    })

@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def api_delete_ticket(ticket_id):
    """Delete ticket via API"""
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    
    return jsonify({'message': 'Ticket deleted successfully'})

@app.route('/api/knowledge-base', methods=['GET'])
def api_get_knowledge_base():
    """Get all knowledge base articles via API"""
    articles = KnowledgeBase.query.order_by(KnowledgeBase.created_date.desc()).all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'category': a.category,
        'tags': a.tags,
        'created_date': a.created_date.isoformat(),
        'author': a.author,
        'views': a.views
    } for a in articles])

@app.route('/api/knowledge-base/search', methods=['GET'])
def api_search_knowledge_base():
    """Search knowledge base articles via API"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    articles = KnowledgeBase.query.filter(
        KnowledgeBase.title.contains(query) |
        KnowledgeBase.content.contains(query) |
        KnowledgeBase.tags.contains(query)
    ).all()
    
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content[:200] + '...' if len(a.content) > 200 else a.content,
        'category': a.category,
        'tags': a.tags
    } for a in articles])

@app.route('/api/dashboard/stats', methods=['GET'])
def api_dashboard_stats():
    """Get dashboard statistics via API"""
    stats = {
        'total_tickets': Ticket.query.count(),
        'open_tickets': Ticket.query.filter_by(status='Open').count(),
        'in_progress': Ticket.query.filter_by(status='In Progress').count(),
        'resolved_tickets': Ticket.query.filter_by(status='Resolved').count(),
        'closed_tickets': Ticket.query.filter_by(status='Closed').count(),
        'priority_distribution': {
            'Critical': Ticket.query.filter_by(priority='Critical').count(),
            'High': Ticket.query.filter_by(priority='High').count(),
            'Medium': Ticket.query.filter_by(priority='Medium').count(),
            'Low': Ticket.query.filter_by(priority='Low').count()
        },
        'category_distribution': {
            'WiFi': Ticket.query.filter_by(category='WiFi').count(),
            'VLAN': Ticket.query.filter_by(category='VLAN').count(),
            'DHCP': Ticket.query.filter_by(category='DHCP').count(),
            'VPN': Ticket.query.filter_by(category='VPN').count(),
            'Hardware': Ticket.query.filter_by(category='Hardware').count(),
            'Other': Ticket.query.filter_by(category='Other').count()
        }
    }
    
    return jsonify(stats)

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ============== APPLICATION STARTUP ==============

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database tables created successfully!")
        print("Starting Customer Support Dashboard...")
        print("Access the application at: http://localhost:5000")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)