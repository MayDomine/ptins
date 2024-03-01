from collections import defaultdict,OrderedDict
class InsLogger:
    def __init__(self):
        self._events = OrderedDict()
        self._history = []

    def _record(self, name, message):
        if type(message) is not str:
            message = str(message)
        self._events[name] = message

    def _log_str(self):
        return "".join([f"{name}: {message}\n" for name, message in self._events.items()])

    def log(self):
        log_str = self._log_str()
        print(log_str)

    def write(self, filename):
        log_str = self._log_str()
        with open(filename,"w") as f:
            f.write(log_str)

    def flush(self):
        self._history.append(self._events)
        self._events = OrderedDict()

    def __call__(self, name, message):
        self._record(name, message)


    
        

    
  

    
