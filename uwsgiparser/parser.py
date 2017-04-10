import argparse
import os.path
from datetime import datetime
from uwsgi import getNextLogEntry, UwsgiLogEntry

def parseTime(timeString):
    try:
        startTime = datetime.strptime(timeString, "%d-%m-%Y_%H-%M-%S")
        return startTime
    except Exception:
        print("ERROR: Given date time format is invalid: %s" % (timeString))
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

    if not os.path.isfile(args.logPath):
        print("ERROR: Given file not found: %s" % (args.logPath))
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


if __name__ == "__main__":
    main()


