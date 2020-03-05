#!usr/bin/

fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=1 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=2 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=4 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=8 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=16 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=32 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=64 --size=512MB --numjobs=4 --group_reporting --readwrite=randread
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=4k --iodepth=128 --size=512MB --numjobs=4 --group_reporting --readwrite=randread

exit 0
