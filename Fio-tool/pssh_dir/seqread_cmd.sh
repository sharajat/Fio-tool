#!usr/bin/

fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=1 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=2 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=4 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=8 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=16 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=32 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=64 --size=512MB --numjobs=4 --group_reporting --readwrite=read
fio --ioengine=libaio --direct=1 --name=test --filename=test --bs=1m --iodepth=128 --size=512MB --numjobs=4 --group_reporting --readwrite=read

        
exit 0

