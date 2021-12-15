#!/bin/bash

DATA=data.txt
CEPH=/ceph/build.latest/bin/ceph # built with docker

$CEPH mgr module enable cli_api
rm $DATA 2>/dev/null
TTL=10
SLEEP=0
THREADS=10

osdmap_test() {
	$CEPH config set mgr mgr_inject true
	for op in no_ttl;
	do
		if [ $op = "no_ttl" ]; then
			$CEPH config set mgr mgr_ttl_cache_expire_seconds 0

		else
			$CEPH config set mgr mgr_ttl_cache_expire_seconds $TTL
		fi
		echo $op >> $DATA
		#for num_osds in 3000;
		#for num_osds in 10 20 30 40 50 75;
		for num_osds in 10 20 30 40 50 75 100 250 500 600 750 900 1000 2000 3000;
		do
			echo $num_osds
			$CEPH config set mgr mgr_inject_num_osds $num_osds
			set_osds="setosds${num_osds}"
			$CEPH mgr api get $set_osds
			#sleep 20
			stats=$($CEPH mgr api benchmark get osd_map 1000 $THREADS)
			echo "$num_osds;$stats" >> $DATA
		done
	done
	$CEPH config set mgr mgr_inject false
}

pgmap_test() {
	$CEPH osd pool create pooltest 1
	$CEPH osd pool set pooltest pg_autoscale_mode off
	for op in no_ttl ttl;
	do
		if [ $op = "no_ttl" ]; then
			$CEPH config set mgr mgr_ttl_cache_expire_seconds 0
			SLEEP=60

		else
			SLEEP=60
			$CEPH config set mgr mgr_ttl_cache_expire_seconds $TTL
		fi
		echo $op >> $DATA
		#for num_pgs in 10000 20000 30000 50000 100000;
		#for num_pgs in 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192;
		for num_pgs in 16384 32768;
		do
			echo $num_pgs
			$CEPH osd pool set pooltest pg_num $num_pgs
			sleep $SLEEP
			stats=$($CEPH mgr api benchmark get pg_stats 1000 $THREADS)
			echo "$num_pgs;$stats" >> $DATA
		done
	done
}
syn_test() {
	$CEPH config set mgr mgr_inject true
	for op in no_ttl;
	do
		if [ $op = "no_ttl" ]; then
			$CEPH config set mgr mgr_ttl_cache_expire_seconds 0

		else
			$CEPH config set mgr mgr_ttl_cache_expire_seconds $TTL
		fi
		echo $op >> $DATA
		#for num_osds in 3000;
		#for num_osds in 10 20 30 40 50 75;
		for formatter in p j;
		do
			echo $formatter
			for num_osds in 10 20 30 40 50 75 100 250 500 600 750 900 1000 2000 3000;
			#for num_osds in 3000;
			do
				to_get="test${formatter}${num_osds}"
				echo $to_get
				$CEPH mgr api get $to_get
			done
		done
	done
	$CEPH config set mgr mgr_inject false
}

osdmap_test2() {
	$CEPH config set mgr mgr_inject true
	for op in no_ttl ttl;
	do
		if [ $op = "no_ttl" ]; then
			$CEPH config set mgr mgr_ttl_cache_expire_seconds 0

		else
			$CEPH config set mgr mgr_ttl_cache_expire_seconds $TTL
		fi
		echo $op >> $DATA
		#for num_osds in 3000;
		#for num_osds in 10 20 30 40 50 75;
		set -x
		for formatter in j p;
		# for formatter in p;
		do
			echo $formatter >> $DATA
			# for num_osds in 1000;
			# for num_osds in 10 20 30 40 50;
			for num_osds in 10 20 30 40 50 75 100 250 500 600 750 900 1000 2000 3000;
			do
				echo $num_osds
				$CEPH config set mgr mgr_inject_num_osds $num_osds

				# this also updates the osd_num and osdmap
				$CEPH mgr cli get $formatter

				# clear
				if [ $op = "ttl" ]; then
					sleep 20

				fi
				stats=$($CEPH mgr cli_benchmark 5000 $THREADS get osd_map)
				# stats=$($CEPH mgr api benchmark get $to_get 1000 1
				echo "$num_osds"$'\n'"$stats" >> $DATA
			done
		done
	done
	$CEPH config set mgr mgr_inject false
}

# build.latest/bin/ceph mgr module enable cli_api
# build.latest/bin/ceph mgr cli get j
# build.latest/bin/ceph mgr cli get osd_map
# build.latest/bin/ceph config set mgr mgr_inject true
# build.latest/bin/ceph config set mgr mgr_inject_num_osds 40
# build.latest/bin/ceph mgr cli get osd_map

osdmap_test2
