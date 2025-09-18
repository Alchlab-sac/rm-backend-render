#!/usr/bin/env python
"""
Django management command to keep Render service alive
Run this as a background task to prevent 15-minute inactivity sleep
"""

import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Keep Render service alive by pinging itself'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=300,  # 5 minutes
            help='Interval in seconds between pings (default: 300)'
        )
        parser.add_argument(
            '--url',
            type=str,
            help='URL to ping (default: uses ALLOWED_HOSTS)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        url = options.get('url')
        
        if not url:
            # Try to construct URL from settings
            if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
                host = settings.ALLOWED_HOSTS[0]
                if host != '*':
                    url = f"https://{host}/"
                else:
                    self.stdout.write(
                        'ERROR: Cannot determine URL from ALLOWED_HOSTS'
                    )
                    return
            else:
                self.stdout.write(
                    'ERROR: Please provide --url parameter'
                )
                return

        self.stdout.write(
            'SUCCESS: Starting keep-alive service...'
        )
        self.stdout.write(f'Pinging: {url}')
        self.stdout.write(f'Interval: {interval} seconds')

        while True:
            try:
                response = requests.get(url, timeout=10)
                self.stdout.write(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S")} - '
                    f'Ping successful: {response.status_code}'
                )
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    f'WARNING: {time.strftime("%Y-%m-%d %H:%M:%S")} - '
                    f'Ping failed: {e}'
                )
            
            time.sleep(interval)
