#!/usr/bin/env python
"""
Startup script to run keep-alive service
This can be used as a background process to prevent Render sleep
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_monitor.settings')
django.setup()

if __name__ == '__main__':
    # Get the Render URL from environment or use a default
    render_url = os.environ.get('RENDER_URL', 'https://your-app-name.onrender.com')
    
    # Run the keep-alive command
    execute_from_command_line([
        'manage.py', 
        'keep_alive',
        '--url', f'{render_url}/api/health/',
        '--interval', '300'  # 5 minutes
    ])
