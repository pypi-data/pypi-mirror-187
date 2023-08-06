# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413,W0212,R0903,W0201,E0402,E0401,W0613
# pylint: disable=R0902


"runtime"


import time
import traceback


from .handler import Command, Handler
from .message import Event, Parsed
from .objects import Class, Default, update


def __dir__():
    return (
            "Cfg",
            "boot",
            "command",
            "date",
            "parse",
            "starttime",
            "wait",
            "waiter",
            "wrap"
           )


class Config(Default):

    pass


Class.add(Config)


Cfg = Config()
Cfg.mod = "cmd,irc,rss"
Cfg.name = "bot"
Cfg.prs = Parsed()


starttime = time.time()
date = time.ctime(starttime).replace("  ", " ")


def boot(txt):
    prs = parse(txt)
    if "c" in prs.opts:
        Cfg.console = True
    if "d" in prs.opts:
        Cfg.daemon= True
    if "v" in prs.opts:
        Cfg.verbose = True
    if "w" in prs.opts:
        Cfg.wait = True
    if "x" in prs.opts:
        Cfg.exec = True
    update(Cfg.prs, prs)
    update(Cfg, prs.sets)


def command(txt, cli=None, event=None):
    cli = cli or Handler()
    evt = (event() if event else Event())
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    evt.wait()
    return evt


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    update(Cfg.prs, prs)
    return prs


def wait(func=None):
    while 1:
        time.sleep(1.0)
        if func:
            func()


def waiter():
    for ex in Command.errors:
        traceback.print_exception(type(ex), ex, ex.__traceback__)


def wrap(func):
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        waiter()
