import re
from datetime import datetime

def getNextLogEntry(logFile):
    """
    Searches through opened file for uWSGI log entry.
    Returns UwsgiLogEtnry object representation if found next log entry.
    """
    pass


class UwsgiLogEntry():
    """
    Represents single uWSGI log entry.
    """

    def __extractEntryData(self, log):
        """
        Extracts and returns entry details as a tuple:
        (ip address, date and time, bytes count and response code)
        """
        p = re.compile(
          "^.+?\] (.+?) .+? \[(.+?)\] .+? (\d+) bytes .+? \(HTTP.+? (\d+)\)",
          re.IGNORECASE)
        m = p.match(log)

        # default values returned in case of error
        ip_address = ""
        date_time = None
        bytes_count = 0
        response_code = ""

        try:
            # if match succeeded parse extracted values
            if m is not None:
                g = m.groups()
                ip_address = g[0]
                date_time = datetime.strptime(g[1], "%a %b %d %H:%M:%S %Y")
                bytes_count = int(g[2])
                response_code = g[3]
        finally:
            return (ip_address, date_time, bytes_count, response_code)

    def __resolveEntryType(self, log):
        """
        Determines gven log type.
        """
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

        if self.type == "ENTRY":
            ipaddr, dt, bc, rc = self.__extractEntryData(log)

            self.ip_address = ipaddr
            self.date_time = dt
            self.bytes_count = bc
            self.response_code = rc
        else:
            self.ip_address = ""
            self.date_time = None
            self.bytes_count = 0
            self.response_code = ""

