from typing import Any, Dict, List

def align_str(s : str, align : int, left : bool) -> str:
    if left:
        return s + " " * (align - len(s))
    else:
        return " " * (align - len(s)) + s

def format_line(strs : List[str], length : List[int]):
    ret = ""
    for v, l in zip(strs, length):
        if len(v) + 1 > l:
            v = " " + v[:l - 1]
        else:
            v = " " + v
        ret += align_str(v, l, True)
    return ret

def item_formater(x) -> str:
    if isinstance(x, float):
        return "{:.4f}".format(x)
    else:
        return str(x)

def format_summary(summary : List[Dict[str, Any]]) -> str:
    """Format summary to string.

    Args:
        summary (List[Dict[str, Any]]): The summary to format.

    Returns:
        str: The formatted summary.

    """
    headers = set()
    ret = []

    for dic in summary:
        for k in dic.keys():
            headers.add(k)
    headers = list(headers)
    key_order = ["name", "shape"]
    for k in key_order[::-1]:
        if k in headers:
            headers.remove(k)
            headers = [k] + headers
    max_name_len = max([len("name")] + [len(item["name"]) for item in summary]) + 4
    key_lens = [max_name_len, 20] 
    headers_length = key_lens + [10 for i in range(len(headers)-2)]
    ret.append( format_line(headers, headers_length) )
    for item in summary:
        values = [ item_formater(item[name]) for name in headers ]
        ret.append( format_line(values, headers_length) )
    return "\n".join(ret)

        