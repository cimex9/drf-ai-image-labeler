import allure

from tests.unit import UNIT_TESTS_OUT_DIR
from tests.unit.fixtures import *  # type: ignore


def pytest_configure(config):
    UNIT_TESTS_OUT_DIR.mkdir(exist_ok=True)
    allure_dir = UNIT_TESTS_OUT_DIR / "allure-results"
    config.option.allure_report_dir = str(allure_dir)
    config.option.capture = 'tee-sys'


def pytest_runtest_setup(item):
    allure.dynamic.label("layer", "unit")
