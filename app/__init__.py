# app/__init__.py
"""Food Vision API - Calorie counting from food photos."""

from app.config import settings

__all__ = ["settings"]  

"""
__all__ = ["settings"]  

This means:

from app import *

will only expose settings, not internal modules.

"""