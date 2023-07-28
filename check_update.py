try:
    import requests as _r
    _req = True
except ImportError:
    _req = False

import os as _o
import subprocess as _s
import json as _j
import rich as _ri

def _check_internet():
    return not _s.getstatusoutput("ping github.com -n 1")[0]

if _req and _o.path.isfile("version") and _o.path.isdir(".git") and _check_internet():
    _update = _r.get("https://dddddgz.github.io/t1.json").text
    _data = _j.loads(_update)
    with open("version") as _f:
        _va, _vb = map(int, _f.read().split())
    if _data["va"] > _va or (_data["va"] == _va and _data["vb"] > _vb):
        _ri.print("[white on blue][i u b]time for update[/][/]")
