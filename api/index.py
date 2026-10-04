"""
Vercel Serverless Function Entrypoint for Investor ScamShield.
Exposes the Flask WSGI application instance `app`.
"""

import sys
import os

# Add root directory to sys.path so modules (analyzer, ocr, app) can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app  # noqa: E402

# Standard WSGI entrypoints for Vercel Python runtime
application = app

__all__ = ['app', 'application']
