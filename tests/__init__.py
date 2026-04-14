from pathlib import Path as _Path

TESTS_BASE_DIR = _Path(__file__).resolve().parent

__all__ = [
    'TESTS_BASE_DIR'
]
