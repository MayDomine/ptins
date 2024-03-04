from contextlib import contextmanager
import sys
from typing import Optional, Union, List, Tuple, Literal
from .ins_logger import InsLogger
from .inspect import inspect_model, format_summary
import os
log_file = set()
@contextmanager
def custom_redirection(fileobj):
    if isinstance(fileobj, str):
        if fileobj not in log_file:
            ftmp = open(fileobj,"w")
            ftmp.close()
            log_file.add(fileobj)
        file_handle = open(fileobj,"a") 
    else:
        file_handle = fileobj
    old = sys.stdout
    sys.stdout = file_handle 
    try:
        yield file_handle 
    finally:
        sys.stdout = old
        file_handle.close()

_log = InsLogger()
def hook_wrapper(map_func, key, pre_hook=False):

    def _get_tuple(x):
        key_2 = map_func[0]
        return (key+"_"+key_2, map_func[1](x))

    def _post_hook(layer, _, output):
        try:
            _log(layer.__name__, _get_tuple(output))
        except:
            _log(layer.__name__, _get_tuple(output[0]))

    def _pre_hook(layer, inp):
        try:
            _log(layer.__name__, _get_tuple(inp))
        except:
            _log(layer.__name__, _get_tuple(inp[0]))
    
    if pre_hook:
        return _pre_hook
    else:
        return _post_hook


def register_ins_hook(model, map_func, log_key, layers=set(), pre_hook=False):
    for key,layer in model.named_modules():
        layer.__name__ = key
        hook_func = hook_wrapper(map_func, log_key, pre_hook=pre_hook)
        if layer not in layers:
            layers.add(layer)
        else:
            continue
        if len(layer._modules) !=0:
            if not pre_hook:
                layer.register_forward_hook(hook_func)
            register_ins_hook(model, map_func, log_key, layers, pre_hook=pre_hook)
            if pre_hook:
                layer.register_forward_pre_hook(hook_func)

        else:
            if pre_hook:
                layer.register_forward_pre_hook(hook_func)
            else:
                layer.register_forward_hook(hook_func)

class inspector:
    def __init__(self, model) -> None:
        self._ins_item = []
        self.model = model

    def inspect(self, option=Literal[ "input, output" ], attr=Literal["mean, std, max, min, shape, dtype"]):
        model =self.model
        if attr in ['mean', 'std', 'max', 'min']: 
            map_func = lambda x: getattr(x, attr)()
        elif attr == "shape":
            map_func = lambda x: list(x.shape)
        map_func = (attr, map_func)
        if option == "output":
            register_ins_hook(model, map_func, log_key="output")
        elif option == "input":
            register_ins_hook(model, map_func, log_key="input", pre_hook=True)
    
    def inspect_weight(self):
        model = self.model
        summary = inspect_model(model, "*")
        return summary

    def get_summary(self):
        ins_log = _log.log()
        weight = self.inspect_weight(self.model)
        return ins_log, weight 
    
    def write(self, dirname, inspect_weight=True):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        log_file = dirname+"/ins_log.txt"
        _log.write(log_file)
        if inspect_weight:
            weight_file = dirname+"/weight_summary.txt"
            with open(weight_file, "w") as f:
                f.write(format_summary(self.inspect_weight()))



