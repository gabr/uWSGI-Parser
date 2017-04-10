import unittest
from datetime import datetime
from uwsgiparser.uwsgi import getNextLogEntry, UwsgiLogEntry


class TestUwsgi(unittest.TestCase):
    def setUp(self):
        self.TEST_LOGS = {
            "DEBUG": "[DEBUG] [base] Configuring Raven for host:" +
                      "<raven.conf.remote.RemoteConfig object at " +
                      "0x7fdeb1e10b38>",
            "INFO":  "[INFO] [base] Raven is not configured (logging is " +
                      "disabled). Please see the documentation for more " +
                      "information.",
            "ENTRY": "[pid: 16992|app: 0|req: 1/1] 127.0.0.1 () {44 vars " +
                      "in 833 bytes} [Mon Nov 21 17:50:21 2016] GET /admin " +
                      "=> generated 23614 bytes in 993 msecs (HTTP/1.1 404) " +
                      "3 headers in 94 bytes (1 switches on core 0)",
            "ERROR": "[ERROR] [base] Internal Server Error: " +
                      "/sonel_core/product/765/\n " +
                      "Traceback (most recent call last):\n " +
                        "File \"/home/vagrant/.pyenv/versions/3.5.2/ " +
                        "envs/cms/lib/python3.5/site-packages/parler/ " +
                        "forms.py\", line 123, in _clean_translation_model\n " +
                          "exclude=exclude, validate_unique=False)",
            "UNKNOWN": "alskdjfalksj"
        }

        self.LOG_FILE = open('data/logfile.log', 'r')

    def tearDown(self):
        self.LOG_FILE.close()

    def test_has_given_log(self):
        for k in self.TEST_LOGS.keys():
            line = self.TEST_LOGS[k]
            self.assertEqual(line, UwsgiLogEntry(line).log)

    def test_has_correct_entry_type(self):
        for k in self.TEST_LOGS.keys():
            line = self.TEST_LOGS[k]
            self.assertEqual(k, UwsgiLogEntry(line).type)

    def test_extracts_ip_address(self):
        self.assertEqual(
            "127.0.0.1",
            UwsgiLogEntry(self.TEST_LOGS["ENTRY"]).ip_address)

    def test_extracts_date_time(self):
        # Mon Nov 21 17:50:21 2016
        self.assertEqual(
            datetime(2016, 11, 21, 17, 50, 21),
            UwsgiLogEntry(self.TEST_LOGS["ENTRY"]).date_time)

    def test_extracts_bytes_count(self):
        self.assertEqual(
            23614 ,
            UwsgiLogEntry(self.TEST_LOGS["ENTRY"]).bytes_count)

    def test_extracts_response_code(self):
        self.assertEqual(
            404,
            UwsgiLogEntry(self.TEST_LOGS["ENTRY"]).response_code)

    def test_returns_next_log_entries_from_file(self):
        self.assertEqual("DEBUG", getNextLogEntry(self.LOG_FILE).type)
        self.assertEqual("INFO", getNextLogEntry(self.LOG_FILE).type)
        self.assertEqual("ENTRY", getNextLogEntry(self.LOG_FILE).type)

        entry = getNextLogEntry(self.LOG_FILE)
        self.assertEqual("ENTRY", entry.type)
        self.assertEqual("127.0.0.1", entry.ip_address)
        self.assertEqual(datetime(2016, 11, 21, 17, 50, 25), entry.date_time)
        self.assertEqual(23650 , entry.bytes_count)
        self.assertEqual(404, entry.response_code)


