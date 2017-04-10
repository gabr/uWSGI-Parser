import argparse
from uwsgi import getNextLogEntry, UwsgiLogEntry

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
    print args.logPath
    print args.startTime
    print args.endTime


if __name__ == "__main__":
    main()


