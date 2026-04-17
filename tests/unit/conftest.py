from unittest.mock import Mock

import allure
import pytest

from tests.unit import UNIT_TESTS_OUT_DIR
from tests.unit.fixtures import *  # noqa: F403, type: ignore


def pytest_configure(config):
    UNIT_TESTS_OUT_DIR.mkdir(exist_ok=True)
    allure_dir = UNIT_TESTS_OUT_DIR / "allure-results"
    config.option.allure_report_dir = str(allure_dir)
    config.option.capture = 'tee-sys'


def pytest_runtest_setup(item):
    allure.dynamic.label("layer", "unit")


@pytest.fixture(autouse=True)
def mock_vlm_service(monkeypatch):
    from app.services.vlm_client_service import VLMClientService

    mock_service = Mock(spec=VLMClientService)
    monkeypatch.setattr(
        'app.services.vlm_client_service._vlm_service_instance',
        mock_service
    )

    yield mock_service
