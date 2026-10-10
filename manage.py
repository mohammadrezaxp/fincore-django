#!/usr/bin/env python3
import os
import sys

# Ensure the project root is on sys.path so `config` module is findable
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

"""Django's command-line utility for administrative tasks."""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)