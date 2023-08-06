# anlogger

A python3 module to assist in setting up logging.

## Install

```shell
python3 -m pip install anlogger
```

## Usage

```python
from anlogger import Logger
logger_obj = Logger(name="appname", default_loglevel="INFO", fmt=None, syslog=None, syslog_facility=None, log_to_console=True, console_stream='stderr')
logger = logger_obj.get()
logger.info("Message on info-level")
```

`name` is application name used in logging (REQUIRED).

`default_loglevel` is the logging level which is used unless `LOGLEVEL` environment variable is set.

`fmt` is the format used for formatting the logger. Se python's logging module documentation for formattion options.

`syslog` is the syslog configuration. Set to `True` to use local syslog, or a tuple of `("ipaddress-string", port-int)` for remote logging.

`syslog_facility` is one of well-known syslog facilities. If syslog is used but `syslog_facility` is not set, the `user` facility is used by default.

`log_to_console` defines whether the logging is also outputted to the console. Default is `True`.

`console_stream` defines which output stream to use for console logging. Accepted values are `stderr` (default) and `stdout`.

See `logger.Logger` class code for additional details.
