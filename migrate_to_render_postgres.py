#!/usr/bin/env python
"""
Simple script to migrate data from Railway to Render PostgreSQL
Run this after your Render deployment is live
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_monitor.settings')
django.setup()

def migrate_to_render():
    """Migrate data from Railway to Render PostgreSQL"""
    print("🚀 Migrating data to Render PostgreSQL...")
    
    # Check if we have the fixtures file
    if not os.path.exists('fixtures.json'):
        print("❌ fixtures.json not found!")
        print("💡 Make sure you have the data export file")
        return False
    
    try:
        # Import the data to the new database
        print("📥 Importing data to Render PostgreSQL...")
        execute_from_command_line(['manage.py', 'loaddata', 'fixtures.json'])
        
        print("✅ Data migrated successfully to Render PostgreSQL!")
        print("🎉 Your app is now running on Render with all your data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    migrate_to_render()
