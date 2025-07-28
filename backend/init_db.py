import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
import random

# Set up paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'support_dashboard.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Ticket, KnowledgeBase, User

db.init_app(app)

def create_sample_users():
    """Create sample users with different roles"""
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
    
    created_users = []
    for user_data in users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            full_name=user_data['full_name'],
            password_hash=generate_password_hash(user_data['password']),
            role=user_data['role']
        )
        db.session.add(user)
        created_users.append(user_data['full_name'])
    
    print(f"✅ Created {len(users)} sample users")
    return created_users

def create_sample_tickets(engineers):
    """Create realistic sample tickets with various scenarios"""
    ticket_scenarios = [
        {
            'title': 'WiFi keeps disconnecting in Conference Room B',
            'description': 'Employees in Conference Room B are experiencing frequent WiFi disconnections during video calls. The issue started this morning around 9 AM. Signal strength appears normal but connections drop every 10-15 minutes.',
            'priority': 'High',
            'status': 'Open',
            'category': 'WiFi',
            'customer_email': 'facilities@company.com',
            'days_ago': 0
        },
        {
            'title': 'DHCP scope exhausted on VLAN 100',
            'description': 'DHCP server showing scope exhaustion alerts for VLAN 100 (Marketing department). New devices cannot obtain IP addresses. Current lease time is set to 24 hours.',
            'priority': 'Critical',
            'status': 'In Progress',
            'category': 'DHCP',
            'customer_email': 'marketing@company.com',
            'days_ago': 1
        },
        {
            'title': 'VPN connection timeout for remote employees',
            'description': 'Multiple remote employees reporting VPN connection timeouts when trying to access internal resources. Issue affects both Windows and Mac clients. Started after weekend maintenance.',
            'priority': 'High',
            'status': 'In Progress',
            'category': 'VPN',
            'customer_email': 'hr@company.com',
            'days_ago': 2
        },
        {
            'title': 'Switch port gi0/24 not forwarding traffic',
            'description': 'Port gi0/24 on switch SW-FL2-01 is not passing traffic. Connected printer in accounting department is unreachable. Port shows as up/up but no data transmission.',
            'priority': 'Medium',
            'status': 'Resolved',
            'category': 'Hardware',
            'customer_email': 'accounting@company.com',
            'days_ago': 3
        },
        {
            'title': 'Guest network not providing internet access',
            'description': 'Guest WiFi network allows connection but clients cannot reach internet. DNS resolution fails. Internal VLAN routing appears correct.',
            'priority': 'Medium',
            'status': 'Open',
            'category': 'WiFi',
            'customer_email': 'reception@company.com',
            'days_ago': 1
        },
        {
            'title': 'VLAN 200 inter-VLAN routing issue',
            'description': 'Devices on VLAN 200 (Engineering) cannot communicate with VLAN 300 (QA). Same-VLAN communication works fine. Routing table appears correct on core switch.',
            'priority': 'High',
            'status': 'Closed',
            'category': 'VLAN',
            'customer_email': 'engineering@company.com',
            'days_ago': 5
        },
        {
            'title': 'Slow internet speed in Building C',
            'description': 'Users in Building C reporting significantly slower internet speeds since Tuesday. Speed tests show 50% reduction from normal. Other buildings unaffected.',
            'priority': 'Medium',
            'status': 'Open',
            'category': 'Performance',
            'customer_email': 'buildingc@company.com',
            'days_ago': 2
        },
        {
            'title': 'Firewall blocking legitimate traffic',
            'description': 'Security appliance appears to be blocking legitimate HTTPS traffic to external partners. Users cannot access partner portal. Rules review needed.',
            'priority': 'High',
            'status': 'In Progress',
            'category': 'Security',
            'customer_email': 'sales@company.com',
            'days_ago': 1
        },
        {
            'title': 'Access point AP-FL1-12 frequent reboots',
            'description': 'Access point AP-FL1-12 in lobby area rebooting every 2-3 hours. PoE switch port cycling power. Hardware replacement may be needed.',
            'priority': 'Medium',
            'status': 'Resolved',
            'category': 'Hardware',
            'customer_email': 'facilities@company.com',
            'days_ago': 4
        },
        {
            'title': 'DHCP reservation conflicts',
            'description': 'Multiple DHCP reservation conflicts detected for printers and servers. Some devices getting wrong IP addresses. Reservation cleanup required.',
            'priority': 'Low',
            'status': 'Open',
            'category': 'DHCP',
            'customer_email': 'it@company.com',
            'days_ago': 3
        },
        {
            'title': 'QoS policy not prioritizing voice traffic',
            'description': 'VoIP calls experiencing quality issues during peak hours. QoS policies configured but voice traffic not being prioritized properly.',
            'priority': 'Medium',
            'status': 'In Progress',
            'category': 'QoS',
            'customer_email': 'communications@company.com',
            'days_ago': 2
        },
        {
            'title': 'Network monitoring alerts false positives',
            'description': 'SNMP monitoring system generating excessive false positive alerts for switch CPU utilization. Threshold adjustment needed.',
            'priority': 'Low',
            'status': 'Closed',
            'category': 'Monitoring',
            'customer_email': 'netops@company.com',
            'days_ago': 6
        }
    ]
    
    created_tickets = []
    for i, ticket_data in enumerate(ticket_scenarios):
        # Assign tickets to engineers
        assigned_engineer = engineers[i % len(engineers)]
        
        # Calculate creation date
        created_date = datetime.now(timezone.utc) - timedelta(days=ticket_data['days_ago'])
        updated_date = created_date + timedelta(hours=random.randint(1, 48))
        
        ticket = Ticket(
            title=ticket_data['title'],
            description=ticket_data['description'],
            priority=ticket_data['priority'],
            status=ticket_data['status'],
            category=ticket_data['category'],
            assigned_to=assigned_engineer,
            customer_email=ticket_data['customer_email'],
            created_date=created_date,
            updated_date=updated_date
        )
        
        db.session.add(ticket)
        created_tickets.append(ticket_data['title'])
    
    print(f"✅ Created {len(ticket_scenarios)} sample tickets")
    return created_tickets

def create_knowledge_base():
    """Create comprehensive knowledge base articles"""
    kb_articles = [
        {
            'title': 'DHCP Scope Exhaustion Troubleshooting',
            'content': '''**Problem**: DHCP scope exhaustion prevents new devices from obtaining IP addresses.

**Symptoms**:
- New devices cannot connect to network
- DHCP server logs show "scope exhausted" messages
- Existing devices maintain connectivity

**Troubleshooting Steps**:
1. Check current DHCP scope utilization in server console
2. Review lease time settings (default 8 days may be too long)
3. Identify unused reservations that can be removed
4. Look for devices holding multiple leases
5. Consider expanding scope range if physically possible

**Resolution**:
- Reduce lease time to 4 hours for guest networks, 1 day for corporate
- Remove unused static reservations
- Add exclusion ranges for network equipment
- Consider implementing DHCP snooping for security

**Prevention**:
- Monitor DHCP utilization regularly (alert at 80%)
- Implement proper IP address management (IPAM)
- Use shorter lease times for guest networks''',
            'category': 'DHCP',
            'tags': 'dhcp, ip address, troubleshooting, scope exhaustion',
            'author': 'John Smith'
        },
        {
            'title': 'WiFi Connectivity Issues - Step by Step Guide',
            'content': '''**Common WiFi Problems and Solutions**

**Problem**: Frequent disconnections or poor performance

**Initial Checks**:
1. Verify signal strength at problem location (-65 dBm or better)
2. Check for interference using WiFi analyzer
3. Review access point logs for errors
4. Test with different client devices

**Advanced Troubleshooting**:
1. **Channel Overlap**: Switch to non-overlapping channels (1, 6, 11 for 2.4GHz)
2. **Power Settings**: Adjust AP power to prevent co-channel interference  
3. **Client Load**: Check connected client count per AP (max 25-30)
4. **VLAN Assignment**: Verify correct SSID to VLAN mapping

**5GHz vs 2.4GHz**:
- Use 5GHz for high-bandwidth applications
- 2.4GHz for IoT devices and longer range
- Enable band steering when possible

**Security Considerations**:
- Use WPA3 when all clients support it
- WPA2-Enterprise for corporate networks
- Regular password rotation for PSK networks''',
            'category': 'WiFi',
            'tags': 'wifi, wireless, troubleshooting, interference, signal strength',
            'author': 'Mary Johnson'
        },
        {
            'title': 'VLAN Configuration and Troubleshooting',
            'content': '''**VLAN Best Practices and Common Issues**

**Planning Phase**:
- Document VLAN assignments and purposes
- Use consistent VLAN IDs across all switches
- Reserve VLAN 1 for management only
- Plan IP subnets to align with VLANs

**Configuration Steps**:
1. Create VLAN on all switches in path
2. Configure access ports for end devices
3. Set up trunk ports between switches
4. Configure inter-VLAN routing on Layer 3 device

**Common Problems**:
- **Native VLAN mismatch**: Ensure consistent native VLAN on trunks
- **Missing VLAN**: Create VLAN on all switches in path
- **Trunk configuration**: Verify allowed VLANs list
- **STP issues**: Check for blocked ports

**Verification Commands**:
- show vlan brief
- show interfaces trunk
- show interfaces switchport
- show spanning-tree vlan [vlan-id]

**Inter-VLAN Routing**:
- Configure SVIs on Layer 3 switch
- Set up default gateway for each VLAN
- Verify routing table entries''',
            'category': 'VLAN',
            'tags': 'vlan, switching, trunking, inter-vlan routing',
            'author': 'Bob Wilson'
        },
        {
            'title': 'VPN Connection Troubleshooting Guide',
            'content': '''**VPN Connection Issues - Systematic Approach**

**Client-Side Checks**:
1. Verify internet connectivity without VPN
2. Check client software version and updates
3. Test with different connection protocols (IKEv2, OpenVPN, etc.)
4. Review client-side firewall settings

**Server-Side Investigation**:
1. Check VPN server resource utilization
2. Review authentication logs
3. Verify certificate validity and chain
4. Monitor concurrent connection limits

**Network Path Analysis**:
- Test from different networks/ISPs
- Check for ISP blocking VPN protocols
- Verify port forwarding on firewall
- Consider NAT traversal issues

**Common Solutions**:
- Update client certificates
- Adjust MTU size (try 1200 bytes)
- Enable NAT-T for devices behind NAT
- Configure split tunneling if appropriate

**Security Considerations**:
- Implement certificate-based authentication
- Use strong encryption algorithms
- Regular security policy reviews
- Monitor for unusual connection patterns''',
            'category': 'VPN',
            'tags': 'vpn, remote access, authentication, encryption',
            'author': 'Sara Garcia'
        },
        {
            'title': 'Network Hardware Diagnostics',
            'content': '''**Hardware Troubleshooting Methodology**

**Switch Port Issues**:
1. Check physical cable connections
2. Test with known good cable
3. Verify port configuration (speed, duplex)
4. Review port statistics for errors
5. Check PoE power budget if applicable

**Access Point Problems**:
- Verify PoE power delivery (minimum 15.4W for 802.11ac)
- Check environmental factors (temperature, humidity)
- Review firmware version and update if needed
- Test with different mounting location

**Cable Testing**:
- Use cable tester for wire map and length
- Check for electromagnetic interference
- Verify cable category meets requirements
- Test termination quality

**Environmental Factors**:
- Monitor equipment temperature
- Check power supply stability
- Ensure proper ventilation
- Consider electrical interference sources

**Documentation**:
- Maintain hardware inventory
- Track warranty information
- Log configuration changes
- Keep network diagrams current''',
            'category': 'Hardware',
            'tags': 'hardware, diagnostics, cable testing, switch, access point',
            'author': 'John Smith'
        },
        {
            'title': 'Network Security Best Practices',
            'content': '''**Essential Network Security Measures**

**Access Control**:
- Implement 802.1X for wired and wireless
- Use MAC address filtering as secondary measure
- Regular access review and cleanup
- Strong password policies

**Network Segmentation**:
- Separate guest and corporate networks
- Isolate IoT devices on dedicated VLAN
- Implement microsegmentation where possible
- Use ACLs to control inter-VLAN communication

**Monitoring and Logging**:
- Enable logging on all network devices
- Implement SIEM for log correlation
- Monitor for unusual traffic patterns
- Regular security audits

**Firewall Configuration**:
- Default deny policy
- Specific allow rules only
- Regular rule review and cleanup
- Geo-blocking for suspicious countries

**Wireless Security**:
- WPA3 encryption when possible
- Regular SSID password changes
- Hide management SSIDs
- Wireless intrusion detection

**Update Management**:
- Regular firmware updates
- Security patch management
- Configuration backup before changes
- Change control procedures''',
            'category': 'Security',
            'tags': 'security, firewall, access control, monitoring, wireless',
            'author': 'Mary Johnson'
        }
    ]
    
    created_articles = []
    for article_data in kb_articles:
        # Create articles with dates spread over the past month
        created_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
        
        article = KnowledgeBase(
            title=article_data['title'],
            content=article_data['content'],
            category=article_data['category'],
            tags=article_data['tags'],
            author=article_data['author'],
            created_date=created_date
        )
        
        db.session.add(article)
        created_articles.append(article_data['title'])
    
    print(f"✅ Created {len(kb_articles)} knowledge base articles")
    return created_articles

def main():
    print("🚀 Initializing Customer Support Dashboard Database...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Drop existing tables and recreate (for clean start)
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            print("\n👥 Creating sample users...")
            engineers = create_sample_users()
            
            print("\n🎫 Creating sample tickets...")
            tickets = create_sample_tickets(engineers)
            
            print("\n📚 Creating knowledge base articles...")
            articles = create_knowledge_base()
            
            # Commit all changes
            db.session.commit()
            print("\n💾 All data committed to database!")
            
            # Print summary
            print("\n" + "=" * 60)
            print("📊 DATABASE INITIALIZATION SUMMARY")
            print("=" * 60)
            print(f"👤 Users created: {len(engineers)}")
            print(f"🎫 Tickets created: {len(tickets)}")
            print(f"📖 KB articles created: {len(articles)}")
            print("\n🔐 Default Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n💡 Other test accounts:")
            print("   jsmith/password123 (Senior Engineer)")
            print("   mjohnson/password123 (Network Engineer)")
            print("   bwilson/password123 (Support Specialist)")
            print("   sgarcia/password123 (Junior Engineer)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\n🎉 Initialization completed successfully!")
        print("📝 You can now run your Flask application and explore the dashboard.")
    else:
        print("\n💥 Initialization failed!")
        sys.exit(1)