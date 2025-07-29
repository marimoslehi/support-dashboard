@app.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    """Create new ticket page"""
    if request.method == 'POST':
        ticket = Ticket(
            title=request.form['title'],
            description=request.form['description'],
            priority=request.form['priority'],
            status='Open',
            category=request.form['category'],
            customer_email=request.form['customer_email'],
            created_date=datetime.now(timezone.utc)
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('tickets'))
    
    return render_template('ticket_form.html')
