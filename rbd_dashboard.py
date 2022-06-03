"""
This should be run inside selftest module.
example:
```
cd src/pybind/
./ceph_mgr_repl.py --timeout 10000 rbd_dashboard.py
```
if it fails loading the file then copy and paste the code inside the repl:
```
ceph mgr module enable selftest
cd src/pybind/
./ceph_mgr_repl.py --timeout 10000
<paste>


# create images:
for i in {1..10}; do  rbd create "${i}m" --size 10M; done
```

"""

# import as mgrd because self store the mgr module inside 'mgr' variable
import mgr.dashboard as mgrd
# init dashboard config proxy
mgrd.mgr.init(mgr)
from mgr.dashboard.services.rbd import RbdService
import sys
import cProfile
import pstats
import rbd
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

"""
FUNCTIONS MUSTN'T HAVE LINE BREAK IN BETWEEN because of selftest
"""


def remove_images(start=0, size=10, pool_name='rbd'):
    ioctx = mgr.rados.open_ioctx(pool_name)
    for i in range(start, start+size):
        rbd.RBD().remove(ioctx, f'image{i}')


def create_images(start=0, size=10, pool_name='rbd'):
    ioctx = mgr.rados.open_ioctx(pool_name)
    for i in range(start, start+size):
        rbd.RBD().create(ioctx, f'image{i}', 1024)
        

def prof_rbd(total):
    pr = cProfile.Profile()
    pr.enable()
    for i in range(total):
        res = RbdService.rbd_pool_list('rbd')
    pr.disable()
    ps = pstats.Stats(pr).sort_stats('cumulative')
    ps.print_stats()
    ps.dump_stats('/ceph/rbd.stats')

def bench(total=10):
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
    times = []
    for s in sizes[:8]:
        create_images(size=s)
        t1 = time.time()
        for i in range(total):
            RbdService.rbd_pool_list('rbd')
        t2 = time.time()
        times.append(t2-t1)
        remove_images(size=s)
    return times


def plot(x, ys):
    for y in ys:
        plt.plot(x, y)
    plt.savefig('/ceph/fig.png')

# wefwe
