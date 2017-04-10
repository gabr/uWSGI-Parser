import argparse
import os.path
from datetime import datetime
from uwsgi import getNextLogEntry, UwsgiLogEntry


def getStatistics(logPath, startTime, endTime):
    """
    Returns statistics calculated from given log file path.
    Calculated statistics:
        - request count
        - request per second count
        - individual response codes count
        - average response package size
    """
    try:
        logFile = open(logPath, 'r')
        count = 0
        firstEntry = None
        lastEntry = None
        seconds = 1
        response_codes = {}

        count_200 = 0
        size_200 = 0.0

        logEntry = getNextLogEntry(logFile)
        while logEntry is not None:
            if (logEntry.type == "ENTRY" and
                (startTime is None or logEntry.date_time >= startTime) and
                (endTime is None or logEntry.date_time <= endTime)):

                if firstEntry is None:
                    firstEntry = logEntry
                lastEntry = logEntry

                if not response_codes.has_key(logEntry.response_code):
                    response_codes[logEntry.response_code] = 0
                response_codes[logEntry.response_code] += 1

                count += 1

                if (logEntry.response_code >= 200 and
                    logEntry.response_code < 300):
                    count_200 += 1
                    size_200 += logEntry.bytes_count

            logEntry = getNextLogEntry(logFile)

        if (firstEntry is not None and lastEntry is not None):
            seconds = (lastEntry.date_time - firstEntry.date_time).seconds
            seconds = seconds if seconds > 0 else 1
    finally:
        logFile.close()
        return (count, float(count)/float(seconds), response_codes,
                size_200/count_200/1024.0 if count_200 != 0 else 0)


def parseTime(timeString):
    try:
        startTime = datetime.strptime(timeString, "%d-%m-%Y_%H-%M-%S")
        return startTime
    except Exception:
        print("ERROR: Given date time format is invalid: {0}".format(timeString))
        return None


def main():
    """
    Main parser function.
    Parses gien log file and returns statistics.
    """
    parser = argparse.ArgumentParser(
        description='Calculates statistics from uWSGI logs')
    parser.add_argument('logPath', help='path to uWSGI log file')
    parser.add_argument("--from", dest="startTime", help='start time, e.g 20-11-2016_11-23-11')
    parser.add_argument("--to", dest="endTime", help='end time, e.g 20-11-2016_11-23-11')

    args = parser.parse_args()

    # validating arguments
    if not os.path.isfile(args.logPath):
        print("ERROR: Given file not found: {0}".format(args.logPath))
        return

    startTime = None
    if args.startTime is not None:
        startTime = parseTime(args.startTime)
        if startTime is None:
            return

    endTime = None
    if args.endTime is not None:
        endTime = parseTime(args.endTime)
        if endTime is None:
            return

    # calculating statistics
    count, avr, codes, size = getStatistics(args.logPath, startTime, endTime)
    print("Zapytan: {0}".format(count))
    print("Zapytania/sec: {0:.1f}".format(avr))
    print("Odpowiedzi {0}".format(codes).replace("{", "(").replace("}", ")"))
    print("Sredni rozmiar zapytan z kodem 2xx: {0:.2f} Mb".format(size))


if __name__ == "__main__":
    main()


