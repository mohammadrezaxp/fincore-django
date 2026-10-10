"""
Django project settings for fincore-django.
Split into base/dev/prod for clean configuration management.
"""

from .base import *

# ── dev overrides ──
from .dev import *  # noqa: F401, F403

# ── prod overrides ──
# from .prod import *  # noqa: F401, F403