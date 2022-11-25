#!/bin/bash

for i in {1..10};
do
	ceph osd pool create rbd_$i;
	ceph osd pool application enable rbd_$i rbd
	for j in {1..10};
	do
		rbd namespace create --pool rbd_$i --namespace ns_$j;
		for k in {1..100};
		do
			echo "pool=rbd_$i, namespace=ns_$j, img=rbd_$k";
			rbd create --pool rbd_$i --namespace ns_$j --size 1G rbd_$k;
      for z in {1..100};
      do
        rbd image-meta set "rbd_$i/ns_$j/rbd_$k" foo_$z $z
      done;
		done;
	done;
done

# i=2
# ceph osd pool create rbd_$i;
# ceph osd pool application enable rbd_$i rbd
# a=1
# for j in {1..10};
# do
# 	rbd namespace create --pool rbd_$i --namespace ns_$j;
# 	for k in {1..10};
# 	do
# 		echo "pool=rbd_$i, namespace=ns_$j, img=rbd_$k";
# 		rbd create --pool rbd_$i --namespace ns_$j --size 1G $a;
# 		((a=a+1))
# 	done;
# done;
