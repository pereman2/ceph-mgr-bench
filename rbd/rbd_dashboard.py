"""
This should be run inside selftest module.
example:
```
cd src/pybind/
./ceph_mgr_repl.py --timeout 10000 rbd_dashboard.py # this doesn't work rn
```
if it fails loading the file then copy and paste the code inside the repl:
```
ceph mgr module enable selftest
cd src/pybind/
./ceph_mgr_repl.py --timeout 10000

<paste>


# create images:
for i in {1..2000}; do  rbd create "image${i}" --size 10M; done
# if you want mirrored things :P
for i in {1..5}; do  rbd mirror image enable rbd/"image${i}" journal; done
for i in {6..10}; do  rbd mirror image enable rbd/"image${i}" snapshot; done
```

# FUNCTIONS MUSTN'T HAVE LINE BREAK IN BETWEEN because of selftest
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

def remove_images(start=0, size=10, pool_name='rbd'):
    ioctx = mgr.rados.open_ioctx(pool_name)
    for i in range(start, start+size):
        try:
            rbd.RBD().remove(ioctx, f'image{i}', force=True)
        except:
            pass


def create_images(start=0, size=10, pool_name='rbd'):
    ioctx = mgr.rados.open_ioctx(pool_name)
    for i in range(start, start+size):
        try:
            rbd.RBD().create(ioctx, f'image{i}', 1024)
        except:
            pass
        

def prof_rbd(total=1, size=-1):
    if size != -1:
        create_images(size=size)
    pr = cProfile.Profile()
    pr.enable()
    t1 = time.time()
    for i in range(total):
        res = RbdService.rbd_pool_list(['rbd'], offset=1000, limit=10)
    t2 = time.time()
    pr.disable()
    ps = pstats.Stats(pr).sort_stats('cumulative')
    ps.print_stats()
    ps.dump_stats('/ceph/rbd.stats')
    print(f'time avg taken {(t2-t1)/total}')
    if size != -1:
        remove_images(size=size)

def bench(total=10, size_limit=512, limit=10):
    # NOTE: 1024 will take forever in my computer, I recommend limitting to
    # 512. You can check the flamegraph where you can see that most of the time
    # the mgr does nothing.
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
    times = []
    import datetime
    date = datetime.datetime.now()
    #for test in ['default', 'ttl pool', 'ttl image' 'ttl both']:
    with open('/ceph/bench.res', 'a+') as f:
        f.write(f'size;avg time')
        f.write('\n')
    for s in sizes:
        if s > size_limit:
            break
        create_images(size=s)
        t1 = time.time()
        for i in range(total):
            RbdService.rbd_pool_list(['rbd'], offset=0, limit=limit)
        t2 = time.time()
        times.append(t2-t1)
        remove_images(size=s)
        with open('/ceph/bench.res', 'a+') as f:
            f.write(f'{s};{(t2-t1)/total}')
            f.write('\n')
    return times


def test(pool_name=None):
    pools = ['rbd']
    if pool_name:
        pools = [pool_name]
    else:
        for pool in range(1, 10):
            pools.append('rbd_' + str(pool))
        
    print(pools)
    import rbd
    inst = rbd.RBD()
    for pool in pools:
        with mgr.rados.open_ioctx(pool) as ioctx:
            print(inst.mirror_image_status_summary(ioctx))
            if pool_name:
                for i in inst.mirror_image_status_list(ioctx):
                    print(i)

    
