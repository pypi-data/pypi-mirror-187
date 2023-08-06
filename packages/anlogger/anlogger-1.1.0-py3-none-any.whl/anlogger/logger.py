import logging
import logging.handlers
import os

class Logger(object):

  def __init__(self, name, default_loglevel='INFO', fmt=None, syslog=None, syslog_facility=None):
    self.name   = name
    self.syslog = syslog
    self.syslog_facility = syslog_facility
    self.fmt = fmt if fmt is not None else "%(asctime)-15s %(name)s %(levelname)s %(message)s"

    if 'LOGLEVEL' in os.environ:
      self.level = os.environ['LOGLEVEL'].upper()
    else:
      self.level = default_loglevel.upper()

    logging.basicConfig(format=self.fmt)
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(self.level)

    if self.syslog is not None and self.syslog not in (False, 0):
      if isinstance(self.syslog, (list, tuple)):
        _addr = tuple(self.syslog)
      elif isinstance(self.syslog, str):
        _addr = self.syslog
      else:
        _addr = "/dev/log" if os.path.exists("/dev/log") else None

      if _addr is not None:
        handler = logging.handlers.SysLogHandler(
          address=_addr,
          facility=syslog_facility
        )
        self.logger.addHandler(handler)


  def get(self):
    return self.logger
