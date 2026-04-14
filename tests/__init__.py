from pathlib import Path as _Path

PROJECT_ROOT = _Path(__file__).resolve().parent.parent
TESTS_BASE_DIR = _Path(__file__).resolve().parent

__all__ = [
    'PROJECT_ROOT',
    'TESTS_BASE_DIR'
]
