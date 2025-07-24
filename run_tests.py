import pytest
import sys
import os

# Add root directory to sys.path so `app` is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

pytest.main(["-v", "tests"])
