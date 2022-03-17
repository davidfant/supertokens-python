import json
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch

from supertokens_python.constants import VERSION
from supertokens_python.logger import streamFormatter, streamHandler


class LoggerUtilsTests(TestCase):
    @patch('supertokens_python.logger._get_log_timestamp', return_value='timestamp')
    def test_json_msg_format(self, mock_timestamp: MagicMock):  # pylint: disable=unused-argument
        with self.assertLogs(level='DEBUG') as captured:
            logging.info("API replied with status 200")

        record = captured.records[0]
        streamHandler.transform(record)
        out = json.loads(record.msg)
        filename = out.pop('file').split(':')[0]

        assert filename.endswith('tests/test_logger.py')
        assert out == {'t': 'timestamp', 'sdkVer': VERSION, 'message': 'API replied with status 200'}

    def test_stream_formatter_format(self):
        assert streamFormatter._fmt == "com.supertokens {message} +{relative}ms"  # pylint: disable=protected-access
