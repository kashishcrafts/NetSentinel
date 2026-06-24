import sys
from pathlib import Path

# Add backend to path for tests
sys.path.insert(0, str(Path(__file__).parent / "backend"))

pytest_plugins = []
