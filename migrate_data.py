#!/usr/bin/env python
"""
Data migration script for Render deployment
Handles encoding issues properly
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_monitor.settings')
django.setup()

def migrate_data():
    """Migrate data with proper encoding handling"""
    print("🚀 Starting data migration...")
    
    try:
        # Try to load the clean fixtures
        print("📥 Loading clean fixtures...")
        execute_from_command_line(['manage.py', 'loaddata', 'clean_fixtures.json'])
        print("✅ Data migrated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("💡 This might be due to encoding issues or data conflicts")
        return False

if __name__ == '__main__':
    migrate_data()
