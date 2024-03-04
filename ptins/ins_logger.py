from collections import defaultdict,OrderedDict
from .inspect import format_summary
class InsLogger:
    def __init__(self, rank=None, combine_stragety="none") -> None:
        self._events = OrderedDict()
        self._history = []

    def _record(self, name, item):
        if name not in self._events:
            self._events[name] = {"name":name}
        self._events[name][item[0]] = item[1]

    def _log_str(self):
        return "".join([f"{name}: {message}\n" for name, message in self._events.items()])

    def log(self):
        log_str = self._log_str()
        print(log_str)

    def summary(self):
        ret = list(self._events.values())
        return ret

    def write(self, filename):
        s = self.summary()
        with open(filename,"w") as f:
            f.write(format_summary(s))

    def flush(self):
        self._history.append(self._events)
        self._events = OrderedDict()

    def __call__(self, name, message):
        self._record(name, message)


    
        

    
  

    
