# tests/conftest.py

import sys
import os

# Add the src directory to sys.path so the tests can import modules from there
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
