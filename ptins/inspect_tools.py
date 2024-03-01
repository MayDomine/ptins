from contextlib import contextmanager
import sys
from typing import Optional, Union, List, Tuple, Enum
from ins_logger import InsLogger
from inspect import inspect_model, format_summary

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
    def _post_hook(layer, _, output):
        try:
            _log(layer.__name__+f" {key}", map_func(output))
        except:
            _log(layer.__name__+f" {key}", map_func(output[0]))

    def _pre_hook(layer, inp):
        try:
            _log(layer.__name__+f" {key}", map_func(inp))
        except:
            _log(layer.__name__+f" {key}", map_func(inp[0]))
    
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
    def __init__(self) -> None:
        self._ins_item = []

    def inspect(self, model, option=Enum("input, output"), attr=Enum("mean, std, max, min, shape")):
        if attr in ['mean', 'std', 'max', 'min']: 
            map_func = lambda x: getattr(x, attr)()
        elif attr == "shape":
            map_func = lambda x: x.shape
        if option == "output":
            register_ins_hook(model, map_func, log_key="output")
        elif option == "input":
            register_ins_hook(model, map_func, log_key="input", pre_hook=True)
    
    def inspect_weight(self, model):
        summary = inspect_model(model, "*")
        return format_summary(summary)


