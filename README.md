# Customer Support Dashboard

A comprehensive web-based ticketing system designed for network support teams, featuring integrated knowledge base and real-time analytics dashboard.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Introduction](#-introduction)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Introduction

Customer Support Dashboard is a powerful web application designed specifically for network support engineers and IT helpdesk teams. This comprehensive tool streamlines the entire support workflow, from ticket creation to resolution, while providing valuable insights through analytics and maintaining a searchable knowledge base.

Built with network support environments in mind, this application handles common networking scenarios including WiFi connectivity issues, VLAN misconfigurations, DHCP problems, VPN connection failures, and hardware troubleshooting. The system provides real-time ticket tracking, priority management, and performance analytics to help support teams deliver exceptional customer service.

The dashboard features an intuitive interface that allows support engineers to quickly access troubleshooting guides, manage ticket assignments, and track resolution metrics. With its focus on networking environments, the knowledge base includes detailed guides for Cisco Meraki devices, common network protocols, and industry best practices.

Whether you're a network support engineer, IT helpdesk technician, or team lead, this dashboard provides a complete solution to manage customer support operations with efficiency and professionalism.

## ✨ Features

### 🎫 **Advanced Ticket Management**
- **Create & Track Tickets**: Submit detailed support requests with rich descriptions and attachments
- **Priority System**: Four-tier priority levels (Critical, High, Medium, Low) with color-coded badges
- **Status Tracking**: Real-time status updates (Open, In Progress, Resolved, Closed)
- **Category Organization**: Network-specific categories (WiFi, VLAN, DHCP, VPN, Hardware, Security)
- **Assignment System**: Assign tickets to specific engineers with role-based permissions
- **Advanced Filtering**: Multi-criteria search and filtering capabilities
- **Timeline View**: Detailed activity timeline for each ticket with audit trail

### 📚 **Comprehensive Knowledge Base**
- **Rich Content Editor**: Create detailed troubleshooting guides with formatting support
- **Categorized Articles**: Organized by network technology and issue type
- **Tag System**: Flexible tagging for improved searchability
- **Full-Text Search**: Powerful search across titles, content, and tags
- **Version Control**: Track article updates and revisions
- **Related Articles**: Smart suggestions based on ticket categories

### 📊 **Real-Time Analytics Dashboard**
- **Live Statistics**: Real-time ticket counts and status distribution
- **Performance Metrics**: Average resolution times and team productivity
- **Visual Charts**: Interactive pie charts and bar graphs using Chart.js
- **Trend Analysis**: Historical data visualization and reporting
- **Priority Distribution**: Visual breakdown of ticket priorities
- **Category Insights**: Most common issue types and resolution patterns

### 🔐 **User Management & Security**
- **Role-Based Access Control**: Admin, Senior Engineer, Network Engineer, Support Specialist roles
- **Secure Authentication**: Password hashing with industry-standard security
- **Session Management**: Secure user sessions with automatic timeout
- **User Profiles**: Individual user settings and preferences
- **Activity Logging**: Comprehensive audit trail for all user actions

### 🎨 **Modern User Interface**
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Dark/Light Themes**: User preference theme switching
- **Interactive Elements**: Smooth animations and hover effects
- **Accessibility**: WCAG 2.1 compliant with screen reader support
- **Progressive Web App**: Offline capabilities and mobile app-like experience

### 🔧 **Network-Specific Features**
- **Protocol Troubleshooting**: Guides for TCP/IP, DNS, DHCP, and routing issues
- **Hardware Diagnostics**: Step-by-step hardware troubleshooting procedures
- **Network Monitoring**: Integration points for monitoring tools and alerts
- **Configuration Templates**: Pre-built configs for common network scenarios
- **Escalation Procedures**: Automated escalation based on priority and time

## 🛠️ Tech Stack

Customer Support Dashboard is built using modern web technologies to ensure reliability, scalability, and ease of maintenance:

### Backend
* **Python 3.8+**: High-level programming language known for its simplicity and extensive libraries
* **Flask 2.0+**: Lightweight and flexible web framework for building robust REST APIs
* **SQLAlchemy**: Powerful SQL toolkit and Object-Relational Mapping (ORM) library
* **SQLite**: Lightweight, serverless database engine (PostgreSQL/MySQL support available)
* **Flask-Login**: User session management and authentication
* **Werkzeug**: Comprehensive WSGI utility library for password hashing and security

### Frontend
* **HTML5**: Modern semantic markup with accessibility features
* **CSS3**: Advanced styling with CSS Grid, Flexbox, and custom properties
* **JavaScript (ES6+)**: Modern JavaScript with async/await and module support
* **Bootstrap 5**: Responsive CSS framework with utility classes
* **Chart.js**: Interactive and responsive charts for data visualization
* **Bootstrap Icons**: Comprehensive icon library for UI elements

### Development Tools
* **Git**: Version control with branching strategy and commit conventions
* **Virtual Environment**: Isolated Python environment for dependency management
* **Flask Debug Toolbar**: Development debugging and profiling tools
* **SQLite Browser**: Database administration and query tools

### Deployment Options
* **Docker**: Containerized deployment with multi-stage builds
* **Gunicorn**: Production WSGI server for Python applications
* **Nginx**: Reverse proxy and static file serving
* **Heroku**: Cloud platform deployment with automatic scaling
* **AWS/DigitalOcean**: VPS deployment with custom configurations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- Virtual environment tool (venv, virtualenv, or conda)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/support-dashboard.git
   cd support-dashboard
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   cd backend
   python init_db.py
   ```

5. **Start the Application**
   ```bash
   python app.py
   ```

6. **Access the Dashboard**
   - Open your browser and navigate to `http://localhost:8000`
   - Login with default credentials: `admin` / `admin123`

### Alternative Installation Methods

#### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8000
```

#### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with debug mode
export FLASK_ENV=development
python app.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///support_dashboard.db
# For PostgreSQL: postgresql://user:password@localhost/support_dashboard
# For MySQL: mysql://user:password@localhost/support_dashboard

# Application Settings
APP_NAME=Customer Support Dashboard
APP_VERSION=1.0.0
MAX_CONTENT_LENGTH=16777216  # 16MB file upload limit

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Security Settings
SESSION_COOKIE_SECURE=False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY=True
WTF_CSRF_ENABLED=True
```

### Database Configuration

The application supports multiple database backends:

#### SQLite (Default)
```python
# No additional configuration needed
DATABASE_URL=sqlite:///support_dashboard.db
```

#### PostgreSQL
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update .env file
DATABASE_URL=postgresql://username:password@localhost/support_dashboard
```

#### MySQL
```bash
# Install MySQL adapter
pip install pymysql

# Update .env file
DATABASE_URL=mysql://username:password@localhost/support_dashboard
```

### Customization Options

#### Branding
- Update `frontend/static/css/style.css` for custom colors and fonts
- Replace logo in `frontend/templates/base.html`
- Modify application name in configuration

#### Features
- Enable/disable modules in `config.py`
- Customize ticket categories and priorities
- Add custom fields to models

## 💻 Usage

### User Roles and Permissions

#### Administrator
- Full system access and configuration
- User management and role assignment
- System settings and maintenance
- Analytics and reporting access

#### Senior Engineer
- Advanced ticket management
- Knowledge base article creation/editing
- Team performance oversight
- Escalation handling

#### Network Engineer
- Ticket assignment and resolution
- Knowledge base contributions
- Category-specific expertise
- Customer communication

#### Support Specialist
- Basic ticket handling
- Knowledge base access
- Customer interaction
- Issue documentation

#### Junior Engineer
- Ticket observation and learning
- Knowledge base reading
- Supervised ticket handling
- Training and development

### Workflow Examples

#### Creating a Support Ticket
1. Navigate to "Create New Ticket"
2. Fill in required information:
   - **Title**: Brief description of the issue
   - **Priority**: Based on business impact
   - **Category**: Network technology affected
   - **Description**: Detailed problem description
3. Submit ticket for assignment
4. Track progress through status updates

#### Managing Tickets
1. View ticket dashboard for overview
2. Use filters to find specific tickets
3. Click on ticket for detailed view
4. Update status, priority, or assignment
5. Add comments and resolution notes

#### Knowledge Base Management
1. Create articles for common issues
2. Organize by category and tags
3. Keep content updated and accurate
4. Link articles to related tickets

## 📁 Project Structure

```
support-dashboard/
├── backend/                    # Flask backend application
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models and schemas
│   ├── init_db.py            # Database initialization script
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   └── support_dashboard.db  # SQLite database file
├── frontend/                  # Frontend assets and templates
│   ├── templates/            # Jinja2 HTML templates
│   │   ├── base.html        # Base template with navigation
│   │   ├── dashboard.html   # Main dashboard page
│   │   ├── tickets.html     # Ticket management page
│   │   ├── ticket_detail.html # Individual ticket view
│   │   ├── ticket_form.html # New ticket creation form
│   │   ├── knowledge_base.html # Knowledge base listing
│   │   └── knowledge_article.html # Article view
│   └── static/              # Static assets (CSS, JS, images)
│       ├── css/
│       │   └── style.css    # Custom styles and themes
│       ├── js/
│       │   └── dashboard.js # Interactive functionality
│       └── images/          # Application images and icons
├── docs/                    # Documentation and guides
│   ├── API.md              # API documentation
│   ├── DEPLOYMENT.md       # Deployment instructions
│   └── CONTRIBUTING.md     # Contribution guidelines
├── tests/                  # Test suites and fixtures
│   ├── test_models.py     # Database model tests
│   ├── test_routes.py     # API endpoint tests
│   └── test_utils.py      # Utility function tests
├── docker-compose.yml     # Docker development environment
├── Dockerfile            # Container build instructions
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # Project documentation
```

## 🔌 API Documentation

### Authentication
All API endpoints require authentication. Include the session cookie or API key in requests.

### Endpoints

#### Tickets API
```http
GET    /api/tickets              # List all tickets
POST   /api/tickets              # Create new ticket
GET    /api/tickets/{id}         # Get specific ticket
PUT    /api/tickets/{id}         # Update ticket
DELETE /api/tickets/{id}         # Delete ticket
```

#### Knowledge Base API
```http
GET    /api/knowledge-base       # List articles
POST   /api/knowledge-base       # Create article
GET    /api/knowledge-base/{id}  # Get specific article
PUT    /api/knowledge-base/{id}  # Update article
DELETE /api/knowledge-base/{id}  # Delete article
```

#### Analytics API
```http
GET    /api/dashboard/stats      # Dashboard statistics
GET    /api/reports/tickets      # Ticket reports
GET    /api/reports/performance  # Performance metrics
```

### Request/Response Examples

#### Create Ticket
```bash
curl -X POST http://localhost:8000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "WiFi connectivity issue in Conference Room A",
    "description": "Users unable to connect to WiFi network",
    "priority": "High",
    "category": "WiFi",
    "customer_email": "user@company.com"
  }'
```

#### Response
```json
{
  "id": 123,
  "title": "WiFi connectivity issue in Conference Room A",
  "status": "Open",
  "priority": "High",
  "created_date": "2024-01-15T10:30:00Z",
  "message": "Ticket created successfully"
}
```

## 📸 Screenshots

### Dashboard Overview
![Dashboard](docs/images/dashboard.png)
*Main dashboard with real-time statistics and recent ticket activity*

### Ticket Management
![Tickets](docs/images/tickets.png)
*Comprehensive ticket listing with advanced filtering and search*

### Ticket Detail View
![Ticket Detail](docs/images/ticket-detail.png)
*Detailed ticket view with timeline, comments, and quick actions*

### Knowledge Base
![Knowledge Base](docs/images/knowledge-base.png)
*Searchable knowledge base with categorized troubleshooting guides*

### Analytics Dashboard
![Analytics](docs/images/analytics.png)
*Real-time analytics with interactive charts and performance metrics*

## 🤝 Contributing

We welcome contributions from the community! Please follow these guidelines:

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Add documentation for new features
- Ensure all tests pass
- Update README.md if needed

### Reporting Issues
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information and logs
- Check for existing issues before creating new ones

### Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for all contributors.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- Bootstrap 5: MIT License
- Chart.js: MIT License
- Bootstrap Icons: MIT License
- Flask: BSD-3-Clause License
- SQLAlchemy: MIT License

## 🏆 Acknowledgments

- **Flask Community**: For the excellent web framework and ecosystem
- **Bootstrap Team**: For the responsive CSS framework
- **Chart.js Contributors**: For the beautiful charting library
- **Network Engineering Community**: For inspiring the networking-focused features
- **Open Source Contributors**: For making this project possible

## 📞 Support

If you encounter any issues or have questions:

1. **Documentation**: Check this README and the docs/ directory
2. **Issues**: Create a GitHub issue for bugs or feature requests
3. **Discussions**: Use GitHub Discussions for general questions
4. **Email**: Contact the maintainers at support@example.com

## 🔮 Roadmap

### Upcoming Features
- [ ] Real-time notifications and alerts
- [ ] Mobile application (React Native)
- [ ] Advanced reporting and analytics
- [ ] Integration with monitoring tools (Nagios, Zabbix)
- [ ] AI-powered ticket classification
- [ ] Multi-tenant support
- [ ] Advanced workflow automation
- [ ] Video call integration for support
- [ ] Customer portal for ticket submission
- [ ] Advanced search with Elasticsearch

### Version History
- **v1.0.0**: Initial release with core features
- **v1.1.0**: Enhanced UI and mobile responsiveness
- **v1.2.0**: Advanced filtering and search capabilities
- **v2.0.0**: API improvements and authentication system

---

⭐ **Star this repository** if you find it helpful!