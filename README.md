# uWSGI logs parser
Python 3.5 script for uWSGI logs paring.

## Usage

    usage: parser.py [-h] [--from STARTTIME] [--to ENDTIME] logPath

    Calculates statistics from uWSGI logs

    positional arguments:
      logPath           path to uWSGI log file

    optional arguments:
      -h, --help        show this help message and exit
      --from STARTTIME  start time, e.g 20-11-2016_11-23-11
      --to ENDTIME      end time, e.g 20-11-2016_11-23-11

## Example usage and calculated statistics:

    $ python .\parser.py ..\data\logfile.log --from 21-11-2014_17-50-20
    Zapytan: 173
    Zapytania/sec: 0.4
    Odpowiedzi (200: 163, 500: 1, 404: 3, 301: 1, 302: 5)
    Sredni rozmiar zapytan z kodem 2xx: 40.93 Mb

## Logs example

    [DEBUG] [base] Configuring Raven for host: <raven.conf.remote.RemoteConfig object at 0x7fdeb1e10b38>
    [INFO] [base] Raven is not configured (logging is disabled). Please see the documentation for more information.
    WSGI app 0 (mountpoint='') ready in 2 seconds on interpreter 0x2187ba0 pid: 16992 (default app)
    *** uWSGI is running in multiple interpreter mode ***
    spawned uWSGI worker 1 (and the only) (pid: 16992, cores: 1)
    [pid: 16992|app: 0|req: 1/1] 127.0.0.1 () {44 vars in 833 bytes} [Mon Nov 21 17:50:21 2016] GET /admin => generated 23614 bytes in 993 msecs (HTTP/1.1 404) 3 headers in 94 bytes (1 switches on core 0)
    [pid: 16992|app: 0|req: 2/2] 127.0.0.1 () {44 vars in 857 bytes} [Mon Nov 21 17:50:25 2016] GET /admin/sonel_core/ => generated 23650 bytes in 389 msecs (HTTP/1.1 404) 3 headers in 94 bytes (1 switches on core 0)
    [pid: 16992|app: 0|req: 3/3] 127.0.0.1 () {44 vars in 823 bytes} [Mon Nov 21 17:50:28 2016] GET / => generated 28462 bytes in 766 msecs (HTTP/1.1 200) 6 headers in 251 bytes (1 switches on core 0)


