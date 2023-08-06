# anlogger

A python3 module to assist in setting up logging.

## Install

```shell
python3 -m pip install anlogger
```

## Usage

```python
from anlogger import Logger
logger_obj = Logger(name="appname", default_loglevel="INFO", fmt=None, syslog=None)
logger = logger_obj.get()
logger.info("Message on info-level")
```

`name` is application name used in logging (REQUIRED).

`default_loglevel` is the logging level which is used unless `LOGLEVEL` environment variable is set.

`fmt` is the format used for formatting the logger. Se python's logging module documentation for formattion options.

`syslog` is the syslog configuration. Set to `True` to use local syslog, or a tuple of `("ipaddress-string", port-int)` for remote logging.

See `logger.Logger` class code for additional details.
