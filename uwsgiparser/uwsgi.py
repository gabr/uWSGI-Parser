import re


def getNextLogEntry(logFile):
    """
    Searches through opened file for uWSGI log entry.
    Returns UwsgiLogEtnry object representation.
    """
    pass


class UwsgiLogEntry():
    def __parse(self, line):
        p = re.compile("^\[(.+?)\]", re.IGNORECASE)
        m = p.match(line)

        if m is None:
            self.type = "UNKNOWN"
        else:
            t = m.groups()[0].upper()
            if t in self.ENTRIES:
                self.type = t
            else:
                self.type = "ENTRY"

    def __init__(self, line):
        self.line = line
        self.ENTRIES = [
            "UNKNOWN",
            "INFO",
            "ERROR",
            "DEBUG",
            "ENTRY"
        ]

        self.__parse(line)

