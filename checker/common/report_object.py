from datetime import datetime
import time

class ReportObject:
    def __init__(self):
        self.created_at = time.time()
        self.strategy=''
        self.facilities=[]
        self.duration=0

    def add_facility(self, facility, result):
        fac = f"{facility}:{result}"
        self.facilities.append(fac)

    def to_array(self):
        arr = []
        arr.append(self.created_at)
        arr.append(self.strategy)
        arr.append(','.join(self.facilities))
        arr.append(self.duration)

    def to_string(self):
        t_str = datetime.fromtimestamp(self.created_at).strftime('%Y-%m-%d %H:%M:%S')
        return f"{t_str}: {self.strategy} - [{','.join(self.facilities)}] ({round(self.duration)}s)"