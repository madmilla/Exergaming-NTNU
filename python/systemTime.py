import time
import ntplib
from datetime import datetime

class SystemTime:
    def get_datetime(self, display=''):
        if display:
            return time.strftime(display)
        else:
            return time.localtime()
  
    def get_idatetime(self):
        ntp = ntplib.NTPClient()
        resp = ntp.request('0.pool.ntp.org', version=3)
        return resp.tx_time
  
    def set_datetime(self, dt=''):
        dt = dt if dt else self.get_idatetime()
        e = shell_cs('date -s @%s' % dt)
        if e[0] != 0:
            raise Exception('System time could not be set. Error: %s' % str(e[1]))
  
    def get_serial_time(self):
        return time.strftime('%Y%m%d%H%M%S')
  
    def get_date(self):
        return time.strftime('%d %b %Y')
  
    def get_time(self):
        return time.strftime('%H:%M')
  
    def get_offset(self):
        ntp = ntplib.NTPClient()
        resp = ntp.request('0.pool.ntp.org', version=3)
        return resp.offset