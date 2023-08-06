import ctypes
import functools
import sys
import threading
from random import randrange
from time import time
from time import sleep as sleep_
from math import floor
from typing import Union, Any
import kthread
import psutil
from copy_functions_and_more import copy_func

copiedfu = copy_func(sys.settrace)
def sleep(secs):
    maxrange = 20 * secs
    if isinstance(maxrange, float):
        sleeplittle = floor(maxrange)
        sleep_((maxrange - sleeplittle) / 20)
        maxrange = int(sleeplittle)

    if maxrange > 0:
        for _ in range(maxrange):
            sleep_(0.05)


def killthread(_thread):
    # from https://pypi.org/project/kthread/
    exctype = SystemExit
    for tid, tobj in threading._active.items():
        if tobj is _thread:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(tid), ctypes.py_object(exctype)
            )
            if res == 0:
                raise ValueError("Invalid thread ID")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
                raise SystemError("PyThreadState_SetAsyncExc failed")


def sleep_with_statusbar(maxrange):
    if isinstance(maxrange, float):
        sleeplittle = floor(maxrange)
        sleep(maxrange - sleeplittle)
        maxrange = int(sleeplittle)
    if maxrange > 0:
        for i in range(maxrange + 1):
            sys.stdout.write("\r")
            sys.stdout.write(f"[{'=' * i}] {i} / {maxrange}")
            sys.stdout.flush()
            sleep(1)
    sys.stdout.write("\r")
    sys.stdout.write(f"                   ")
    sys.stdout.flush()


class timeout_context:
    def __init__(
        self, name, timeout, print_debug, show_remaining_time, timeout_message
    ):
        self.show_remaining_time = show_remaining_time

        self.print_debug = print_debug
        self.name = name
        self.kill_process = False
        self.timeout = timeout
        self.subprocesses = {}
        self.locks = {}
        self.threads = {}
        self.multiprocesses = {}

        self.timeout_message = timeout_message

        self.t = kthread.KThread(
            target=self.check_timer, name=f"{time() + randrange(1,3333333333)}"
        )
        self.t.daemon = True
        self.t.start()

    def check_timer(self):
        if not self.show_remaining_time:
            sleep(self.timeout)
        else:
            sleep_with_statusbar(maxrange=self.timeout)
        self.kill_process = True
        if self.timeout_message is not None:
            print(self.timeout_message)
        # self.stop_asyncio()
        self.__exit__()

    def release_lock(self):
        if self.locks:
            for key, item in self.locks.items():
                try:
                    item.release()
                except Exception as vdw:
                    continue

    def __enter__(self):
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        self.release_lock()

        if self.subprocesses:
            for key, item in self.subprocesses.items():
                try:
                    if psutil.pid_exists(item.pid):
                        self.release_lock()
                        p = psutil.Process(item.pid)
                        p.kill()
                except Exception as da:
                    if self.print_debug:
                        print(da)
                    continue
        if self.threads:
            for key, item in self.threads.items():
                try:
                    self.release_lock()
                    killthread(item)
                except Exception as da:
                    if self.print_debug:
                        print(da)
                    continue
        if self.multiprocesses:
            for key, item in self.multiprocesses.items():
                try:
                    if psutil.pid_exists(item.pid):
                        self.release_lock()
                        p = psutil.Process(item.pid)
                        p.kill()
                except Exception as da:
                    if self.print_debug:
                        print(da)
                    continue
        try:
            if self.t.is_alive():
                self.t.kill()
        except Exception as fe:
            if self.print_debug:
                print(fe)
        if self.kill_process:
            raise TimeoutError
        sys.settrace = copy_func(copiedfu)

    def trace_calls(self, frame, event, arg):
        if event != "call":
            return
        elif frame.f_code.co_name != self.name:
            return
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        if self.kill_process:
            self.__exit__()
        for key, item in frame.f_locals.items():
            itemtype = str(type(item))

            if "'subprocess." in itemtype:
                self.subprocesses[key] = item
            elif ".lock'" in itemtype or ".Lock'" in itemtype:
                self.locks[key] = item
            elif ".Thread'" in itemtype:
                self.threads[key] = item
            elif "multiprocessing." in itemtype:
                self.multiprocesses[key] = item


def ofen_aus(
    func=None,
    timeout: Union[int, float] = 5,
    timeout_value: Any = None,
    print_debug: bool = False,
    show_remaining_time: bool = False,
    print_exceptions: bool = True,
    timeout_message: str = "Time is over!",
):
    def decorated_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with timeout_context(
                    func.__name__,
                    timeout=timeout,
                    print_debug=print_debug,
                    show_remaining_time=show_remaining_time,
                    timeout_message=timeout_message,
                ):

                    return_value = func(*args, **kwargs)
                return return_value
            except Exception as fe:
                if print_exceptions:
                    print(fe)
                return timeout_value

        return wrapper

    return decorated_func(func) if callable(func) else decorated_func
