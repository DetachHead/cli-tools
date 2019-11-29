import logging
import unittest

import pytest

from codemagic_cli_tools.apple.app_store_connect import AppStoreConnectApiClient


@pytest.mark.usefixtures('class_api_client', 'class_logger')
class OperationsTestsBase(unittest.TestCase):
    api_client: AppStoreConnectApiClient
    logger: logging.Logger
