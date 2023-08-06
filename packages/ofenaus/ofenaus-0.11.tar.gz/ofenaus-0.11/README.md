# Timeout decorator for functions! Works on Windows with multiprocessing, threading, subprocess!
### Kill a function after a certain time.
#### Tested on Windows 10 / Python 3.9.13 

```python
pip install ofenaus
```

### Here are some examples 
##### There might be situations where killing the function doesn't work (asyncio, for example) 

```python
import subprocess
import threading
from multiprocessing import Process, Lock
import os

from ofenaus import ofen_aus, sleep # use sleep from this module instead time.sleep() 


@ofen_aus(timeout=3, print_debug=True, print_exceptions=False)
def subprocess_ping():
    pp = subprocess.Popen("ping -t 8.8.8.8") # Only subprocess.Popen can be killed! subprocess.run, subprocess.call etc. can't be killed.
	
    while True:
        sleep(1)


@ofen_aus(timeout=3, print_debug=True, print_exceptions=False)
def thread_lock_aquire():
    my_lock = threading.Lock()
    my_lock.acquire()
    my_lock.acquire()
    while True:
        print("test aquire")
        sleep(1)


@ofen_aus(timeout=3, print_debug=True, print_exceptions=False)
def deamon_thread():
    def f_check(x: int) -> None:
        for _ in range(x):
            print(_)
            sleep(1)

    f_check(0)
    test_1 = threading.Thread(target=f_check, args=(20,))
    test_1.name = "xx"
    test_1.daemon = True
    test_1.start()
    test_1.join()


@ofen_aus(
    timeout=2,
    timeout_value=2000, # the function will return this value if any kind (!) of Exception is raised, not only TimeoutError.
    print_debug=False,
    show_remaining_time=False,
    print_exceptions=False,
    timeout_message="Time is over!",
)
def testing2():
    sleep(1)
    a = 10
    os.chdir("c:\\")
    pp = subprocess.Popen("ping 8.8.8.8")
    print(pp)
    sleep(1)

    b = 20
    sleep(1)

    c = a + b
    sleep(1)


@ofen_aus(timeout=1, timeout_value="not good", show_remaining_time=False)
def testa(i45):
    for k in range(2):
        print(k + i45)
        sleep(1)
    return i45


@ofen_aus(timeout=4)
def fx(name):
    while True:

        print("hello", name)
        sleep(1)


@ofen_aus(timeout=4)
def faax(l, i):
    l.acquire()
    try:
        print("hello world", i)
        sleep(5)
    finally:
        l.release()


if __name__ == "__main__":
    p = Process(target=fx, args=("bob",))
    p.start()
    p.join()
    do = subprocess_ping()
    print(do)
    thread_lock_aquire()
    deamon_thread()
    lock = Lock()
    for num in range(5):
        Process(target=faax, args=(lock, num)).start()
    testa_value = testa(555)
    print(testa_value)
	
	
	
hello bob
hello bob
hello bob
hello bob
hello bob
Time is over!
Pinging 8.8.8.8 with 32 bytes of data:
Reply from 8.8.8.8: bytes=32 time=9ms TTL=119
Reply from 8.8.8.8: bytes=32 time=12ms TTL=119
Reply from 8.8.8.8: bytes=32 time=9ms TTL=119
Reply from 8.8.8.8: bytes=32 time=10ms TTL=119
Time is over!
None
Time is over!
0
1
2
Time is over!
555
hello world 0
556
Time is over!
not good
Time is over!
hello worldhello world 2 
1
Time is over!
Time is over!
hello world 4
Time is over!
Time is over!	


```
