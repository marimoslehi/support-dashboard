from app import app, db, KnowledgeBase
from datetime import datetime, timezone

with app.app_context():
    # Check if knowledge base is empty
    if KnowledgeBase.query.count() == 0:
        # Create sample articles
        articles = [
            {
                'title': 'WiFi Connectivity Troubleshooting Guide',
                'content': '''**Common WiFi Issues and Solutions**

1. **Check Signal Strength**
   - Ensure you're within range of the access point
   - Signal should be -65 dBm or better

2. **Restart Network Adapter**
   - Disable and re-enable WiFi adapter
   - Try "forget" and reconnect to network

3. **Check Network Settings**
   - Ensure correct SSID and password
   - Verify security type (WPA2/WPA3)

4. **Advanced Troubleshooting**
   - Clear DNS cache: ipconfig /flushdns
   - Reset network stack: netsh winsock reset''',
                'category': 'WiFi',
                'tags': 'wifi, connectivity, troubleshooting, wireless',
                'author': 'John Smith'
            },
            {
                'title': 'DHCP Server Configuration Best Practices',
                'content': '''**DHCP Setup Guidelines**

1. **Scope Planning**
   - Plan IP ranges carefully
   - Reserve ranges for static devices
   - Set appropriate lease times

2. **Common Settings**
   - Lease time: 8 hours for corporate, 1 hour for guest
   - DNS servers: Primary and secondary
   - Default gateway configuration

3. **Troubleshooting DHCP Issues**
   - Check scope exhaustion
   - Verify DHCP relay configuration
   - Monitor lease conflicts''',
                'category': 'DHCP',
                'tags': 'dhcp, ip address, configuration, networking',
                'author': 'Mary Johnson'
            }
        ]
        
        for article_data in articles:
            article = KnowledgeBase(
                title=article_data['title'],
                content=article_data['content'],
                category=article_data['category'],
                tags=article_data['tags'],
                author=article_data['author'],
                created_date=datetime.now(timezone.utc)
            )
            db.session.add(article)
        
        db.session.commit()
        print("✅ Sample knowledge base articles created!")
    else:
        print(f"Knowledge base already has {KnowledgeBase.query.count()} articles")
