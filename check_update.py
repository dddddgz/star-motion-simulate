try:
    import requests as r
    req = True
except ImportError:
    req = False

import os as o
import subprocess as s
import json as j
import rich.console as rc

def _check_internet():
    return not s.getstatusoutput("ping github.com -n 1")[0]

if req and o.path.isfile("version") and o.path.isdir(".git") and _check_internet():
    console = rc.Console()
    update = r.get("https://dddddgz.github.io/t1.json").text
    data = j.loads(update)
    with open("version") as _f:
        va, vb = map(int, _f.read().split())[:2]
    if data["va"] > va or (data["va"] == va and data["vb"] > vb):
        if s.getstatusoutput("git pull")[0] == 1:
            console.log("[blink white on purple b i u]It's time for Update! You did not installed Git LoL[/]")
        else:
            console.log("[white on purple]Updated Successfully[/]")
