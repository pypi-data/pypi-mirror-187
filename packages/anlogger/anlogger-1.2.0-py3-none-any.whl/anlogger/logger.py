import logging
import logging.handlers
import os
import sys

class Logger(object):

  def __init__(self,
               name,
               default_loglevel='INFO',
               fmt=None,
               syslog=None,
               syslog_facility=None,
               log_to_console=True,
               console_stream='stderr'):

    self.name   = name
    self.syslog = syslog
    self.syslog_facility = syslog_facility
    self.fmt = fmt if fmt is not None else "%(asctime)-15s %(name)s %(levelname)s %(message)s"
    self.log_to_console = log_to_console

    if 'LOGLEVEL' in os.environ:
      self.level = os.environ['LOGLEVEL'].upper()
    else:
      self.level = default_loglevel.upper()

    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(self.level)

    formatter = logging.Formatter(fmt=self.fmt)

    if self.log_to_console:
      if console_stream == 'stderr':
        console_stream = sys.stderr
      elif console_stream == 'stdout':
        console_stream = sys.stdout
      else:
        raise ValueError(f'Unknown value for console_stream: {console_stream}')

      consoleHandler = logging.StreamHandler(stream=console_stream)
      consoleHandler.setFormatter(formatter)
      self.logger.addHandler(consoleHandler)

    if self.syslog is not None and self.syslog not in (False, 0):
      if isinstance(self.syslog, (list, tuple)):
        _addr = tuple(self.syslog)
      elif isinstance(self.syslog, str):
        _addr = self.syslog
      else:
        _addr = "/dev/log" if os.path.exists("/dev/log") else None

      if _addr is not None:
        syslogHandler = logging.handlers.SysLogHandler(
          address=_addr,
          facility=syslog_facility
        )
        syslogHandler.setFormatter(formatter)
        self.logger.addHandler(syslogHandler)


  def get(self):
    return self.logger
