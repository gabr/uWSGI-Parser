import re
from datetime import datetime

def getNextLogEntry(logFile):
    """
    Searches through opened file for uWSGI log entry.
    Returns UwsgiLogEtnry object representation if found next log entry.
    """
    pass

# exmaple entry:
# [pid: 16992|app: 0|req: 1/1] 127.0.0.1 () {44 vars in 833 bytes} [Mon Nov 21 17:50:21 2016] GET /admin => generated 23614 bytes in 993 msecs (HTTP/1.1 404) 3 headers in 94 bytes (1 switches on core 0)

class UwsgiLogEntry():
    """
    Represents single uWSGI log entry.
    """

    def __extractEntryData(self, log):
        p = re.compile(
          "^.+?\] (.+?) .+? \[(.+?)\] .+? (\d+) bytes .+? \(HTTP.+? (\d+)\)",
          re.IGNORECASE)
        m = p.match(log)

        ip_address = ""
        date_time = None
        bytes_count = 0
        response_code = ""

        try:
            if m is not None:
                g = m.groups()
                ip_address = g[0]
                date_time = datetime.strptime(g[1], "%a %b %d %H:%M:%S %Y")
                bytes_count = int(g[2])
                response_code = g[3]
        finally:
            return (ip_address, date_time, bytes_count, response_code)

    def __resolveEntryType(self, log):
        p = re.compile("^\[(.+?)\]", re.IGNORECASE)
        m = p.match(log)

        try:
            if m is not None:
                t = m.groups()[0].upper()
                if t in self.ENTRIES:
                    return t
                else:
                    return "ENTRY"
            return "UNKNOWN"
        except Exception:
            return "UNKNOWN"

    def __init__(self, log):
        self.log = log
        self.ENTRIES = [
            "UNKNOWN",
            "INFO",
            "ERROR",
            "DEBUG",
            "ENTRY"
        ]

        self.type = self.__resolveEntryType(log)
        ipaddr, dt, bc, rc = self.__extractEntryData(log)

        self.ip_address = ipaddr
        self.date_time = dt
        self.bytes_count = bc
        self.response_code = rc

