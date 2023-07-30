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
    with open("version") as f:
        x = f.read().split()
        va, vb = int(x[0]), int(x[1])
    if data["va"] > va or (data["va"] == va and data["vb"] > vb):
        if len(x) > 2:
            s.getstatusoutput("git pull")
        console.log("[blink white on purple b i u]It's time for Update![/]")
