"""
selftest benchmarks to run on a mgr

**copy paste on the repl loop**
"""

import time
import threading

def osd_map(times=1000):
    for i in range(times):
        osdmap = mgr.get("osd_map")
        print(osdmap)

def test_osd_map(times=10000, nthreads=1):
    thread_times = int(times / nthreads)
    threads = []
    for i in range(nthreads):
        t = threading.Thread(target=osd_map, args=(thread_times,))
        threads.append(t)
    for t in threads:
        t.start()
    t1 = time.time()
    for t in threads:
        t.join()
    print(f'total time {time.time() - t1} times={times}')

