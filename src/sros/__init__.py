"""SROS - Scientific Research Operating System"""

__version__ = "3.0.0b1"
__author__ = "SROS Team"
__description__ = "AI-native research assistant for academic writing"

# Expose main components
from .cli import app

__all__ = ['app', '__version__', '__description__']