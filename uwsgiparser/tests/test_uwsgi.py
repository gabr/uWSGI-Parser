import unittest
from uwsgiparser.uwsgi import getNextLogEntry, UwsgiLogEntry


class TestUwsgi(unittest.TestCase):
    def setUp(self):
        self.TEST_LOGS = {
            "DEBUG":  """[DEBUG] [base] Configuring Raven for host:
                         <raven.conf.remote.RemoteConfig object at
                         0x7fdeb1e10b38>""",
            "INFO_LOG": """[INFO] [base] Raven is not configured (logging is
                           disabled). Please see the documentation for more
                           information.""",
            "ENTRY_LOG": """[pid: 16992|app: 0|req: 1/1] 127.0.0.1 () {44 vars
                            in 833 bytes} [Mon Nov 21 17:50:21 2016] GET /admin
                            => generated 23614 bytes in 993 msecs
                            (HTTP/1.1 404) 3 headers in 94 bytes
                            (1 switches on core 0)""" 
        }

        self.LOG_FILE = open('data/logfile.log', 'r')

    def tearDown(self):
        self.LOG_FILE.close()

    def test_has_given_log_line(self):
        for k in self.TEST_LOGS.keys():
            line = self.TEST_LOGS[k]
            self.assertEqual(line, UwsgiLogEntry(line).line)

