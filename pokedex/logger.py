import json, logging
from logging import handlers

class CustomFileHandler(handlers.RotatingFileHandler):

    def emit(self, record): 
        if type(record.msg).__name__ == "dict":
            try:
                record.msg = f' -_- {json.dumps(record.msg)}'
            except:
                pass
        with self.lock:
            try:
                if self.shouldRollover(record):
                    self.doRollover()
                super().emit(record)
            except Exception as e: 
                self.handleError(record)
 