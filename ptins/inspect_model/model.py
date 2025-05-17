import torch
import fnmatch

@torch.no_grad()
def inspect_model(model : torch.nn.Module, param_name : str, prefix : str = ''):
    """Inspect the model and return the summary of the parameters.

    Args:
        model (torch.nn.Module): The model to be inspected.
        param_name (str): The name of the parameter to be inspected. The wildcard '*' can be used to match multiple parameters.
        prefix (str): The prefix of the parameter name.
        
    Returns:
        list: The summary of the parameters.
    
    Example:
        >>> result_linear = bmt.inspect.inspect_model(model, "*.linear*")
        >>> result_layernorm = bmt.inspect.inspect_model(model, "*.layernorm*")
        >>> text_summray = bmt.inspect.format_summary(result_linear + result_layernorm)
        >>> bmt.print_rank(text_summary)
        name   shape     max     min     std     mean    grad_std  grad_mean
        ...

    """
    ret = []
    for name, param in model._parameters.items():
        if fnmatch.fnmatch(prefix + name, param_name):
            p = param
            if p is None:
                continue
            stats = {
                'name': prefix + name,
                'shape': tuple(p.size()),
                "std": p.std().cpu().item(),
                "mean": p.mean().cpu().item(),
                "max": p.max().cpu().item(),
                "min": p.min().cpu().item(),
            }
            if param.grad is not None:
                g = param.grad
                stats["grad_std"] = g.std().cpu().item()
                stats["grad_mean"] = g.mean().cpu().item()
            else:
                stats["grad_std"] = 0.
                stats["grad_mean"] = 0.
            ret.append(stats)
    for name, module in model._modules.items():
        ret.extend(inspect_model(module, param_name, prefix + name + '.'))
    return ret
