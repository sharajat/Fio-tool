import subprocess
import re

no_of_instances = 160


def get_read_data(line):
    """
    Helper function to get read data from output.
    :param line: Output line for read iops
    :return: tuple of iops_data and bandwidth_data
    """
    result = line.split(" ")
    val = result[4].strip(",")
    iops = re.findall(r'\d*\.\d+|\d+', val)
    if "k" not in val:
        iops_data = (float(iops[0]))
    else:
        final = float(iops[0])
        iops_data = (final * 1000)
    bandwidth = re.findall(r'\d*\.\d+|\d+', result[5])
    if "G" in bandwidth:
        final = float(bandwidth[0])
        bw_data = (final * 1024)
    else:
        bw_data = (float(bandwidth[0]))

    return iops_data, bw_data


def get_write_data(line):
    """
    Helper function to get write data from output.
    :param line: Output line for write iops
    :return: tuple of iops_data and bandwidth_data
    """
    result = line.split(" ")
    val = result[3].strip(",")
    iops = re.findall(r'\d*\.\d+|\d+', val)
    if "k" not in val:
        iops_data = float(iops[0])
    else:
        final = float(iops[0])
        iops_data = (final * 1000)
    bw = re.findall(r'\d*\.\d+|\d+', result[4])
    if "G" in bw:
        final = float(bw[0])
        bw_data = (final * 1024)
    else:
        bw_data = (float(bw[0]))

    return iops_data, bw_data


def get_latency_data(line):
    """
    Helper function to get latency data from output.
    :param line: Output line for latency
    :return: tuple of latency
    """
    result = line.split(" ")
    val = result[9].strip(",")
    lat = re.findall(r'\d*\.\d+|\d+', val)
    if "usec" in line:
        final = float(lat[0])
        latency_data = (final / 1000)
    else:
        latency_data = (float(lat[0]))

    return latency_data


def get_cpu_data(line):
    """
    Helper function to get % of CPU utilization data from output.
    :param line: Output line for CPU utilization
    :return: tuple of % of CPU utilization
    """
    result = line.split(" ")
    val = result[14].strip(",")
    cpu = re.findall(r'\d*\.\d+|\d+', val)
    cpu_util_data = (float(cpu[0]))
    return cpu_util_data


def get_average(final_list, inst):
    """
    Helper function to calculate average of data of insatnces and rounding it 
    off to two decimal places.
    :param final_list:
    :param inst:
    :return:
    """
    for index in range(len(final_list)):
        final_list[index] = round((final_list[index] / inst), 2)
    return final_list


def random_read():
    """
    This function executes 4K Random Reads for iodepth (1,2,4,8,16,32,64,128)
    and gets read-iops, read_latency, read_bandwidth and cpu utilization for
    the respective no_of_instances..

    """
    command = 'sudo pssh -h pssh_host -t ' \
              '1000000000 -x "-o StrictHostKeyChecking=no ' \
              '-i /home/centos/centos.pem" ' \
              '-o /home/centos/FIO_test/fio-out -I<./randread_cmd.sh'
    subprocess.call(command, shell=True)
    instance_names = []
    with open("/home/centos/FIO_test/pssh_dir/pssh_host") as f:
        lines = f.readlines()
        for line in range(len(lines)):
            instance_names.append(lines[line].strip("\n"))
    final_r_iops = []
    final_r_lat = []
    final_r_cpu = []
    final_r_bw = []
    for instance in instance_names[0:no_of_instances]:
        read_iops = []
        latency = []
        cpu_util = []
        read_bw = []
        path = "/home/centos/FIO_test/fio-out/" + instance
        with open(path) as f:
            file_data = f.readlines()
            for line in file_data:
                if "read" in line and "IOPS" in line:
                    iops_data, bw_data = get_read_data(line)
                    read_iops.append(iops_data)
                    read_bw.append(bw_data)

                if " lat" in line and "avg" in line:
                    latency_data = get_latency_data(line)
                    latency.append(latency_data)

                if "cpu" in line:
                    cpu_util_data = get_cpu_data(line)
                    cpu_util.append(cpu_util_data)

        if not final_r_iops and not final_r_lat:
            final_r_iops = read_iops
            final_r_lat = latency
            final_r_cpu = cpu_util
            final_r_bw = read_bw
        else:
            final_r_iops = [sum(x) for x in zip(final_r_iops, read_iops)]
            final_r_lat = [sum(x) for x in zip(final_r_lat, latency)]
            final_r_cpu = [sum(x) for x in zip(final_r_cpu, cpu_util)]
            final_r_bw = [sum(x) for x in zip(final_r_bw, read_bw)]

    final_r_iops = get_average(final_r_iops, no_of_instances)
    final_r_lat = get_average(final_r_lat, no_of_instances)
    final_r_cpu = get_average(final_r_cpu, no_of_instances)
    final_r_bw = get_average(final_r_bw, no_of_instances)

    # Printing the final outputs...

    print("Random-read Output of " + str(no_of_instances) + " Instances ")
    print("read_iops = ", final_r_iops)
    print("read_latency (msec)= ", final_r_lat)
    print("read_cpu = ", final_r_cpu)
    print("read_bw (MB/s) = ", final_r_bw)


def random_write():
    """
    This function executes 4K Random write for iodepth (1,2,4,8,16,32,64,128)
    and gets write-iops, write_latency, write_bandwidth and cpu utilization
    for the respective no_of_instances..

    """
    command = 'sudo pssh -h pssh_host ' \
              '-t 1000000000 -x "-o StrictHostKeyChecking=no ' \
              '-i /home/centos/centos.pem" ' \
              '-o /home/centos/FIO_test/fio-out -I<./randwrite_cmd.sh'
    subprocess.call(command, shell=True)
    instance_names = []
    with open("/home/centos/FIO_test/pssh_dir/pssh_host") as f:
        lines = f.readlines()
        for line in range(len(lines)):
            instance_names.append(lines[line].strip("\n"))
    final_w_iops = []
    final_w_lat = []
    final_w_cpu = []
    final_w_bw = []
    for instance in instance_names[0:no_of_instances]:
        write_iops = []
        latency = []
        cpu_util = []
        write_bw = []
        path = "/home/centos/FIO_test/fio-out/" + instance
        with open(path) as f:
            file_data = f.readlines()
            for line in file_data:
                if "write" in line and "IOPS" in line:
                    iops_data, bw_data = get_write_data(line)
                    write_iops.append(iops_data)
                    write_bw.append(bw_data)

                if " lat" in line and "avg" in line:
                    latency_data = get_latency_data(line)
                    latency.append(latency_data)

                if "cpu" in line:
                    cpu_util_data = get_cpu_data(line)
                    cpu_util.append(cpu_util_data)

        if not final_w_iops and not final_w_lat:
            final_w_iops = write_iops
            final_w_lat = latency
            final_w_cpu = cpu_util
            final_w_bw = write_bw
        else:
            final_w_iops = [sum(x) for x in zip(final_w_iops, write_iops)]
            final_w_lat = [sum(x) for x in zip(final_w_lat, latency)]
            final_w_cpu = [sum(x) for x in zip(final_w_cpu, cpu_util)]
            final_w_bw = [sum(x) for x in zip(final_w_bw, write_bw)]

    final_w_iops = get_average(final_w_iops, no_of_instances)
    final_w_lat = get_average(final_w_lat, no_of_instances)
    final_w_cpu = get_average(final_w_cpu, no_of_instances)
    final_w_bw = get_average(final_w_bw, no_of_instances)

    # Printing the final output....

    print("Random-write Output of " + str(no_of_instances) + " Instances ")
    print("write_iops = ", final_w_iops)
    print("write_latency (msec)= ", final_w_lat)
    print("write_cpu = ", final_w_cpu)
    print("write_bw (MB/s) = ", final_w_bw)


def sequential_read():
    """
    This function executes 1M sequential Reads for iodepth
    (1,2,4,8,16,32,64,128) and gets read-iops, read_latency,
    read_bandwidth and cpu utilization for the respective no_of_instances..

    """
    command = 'sudo pssh -h pssh_host ' \
              '-t 1000000000 -x "-o StrictHostKeyChecking=no ' \
              '-i /home/centos/centos.pem" ' \
              '-o /home/centos/FIO_test/fio-out -I<./seqread_cmd.sh'
    subprocess.call(command, shell=True)
    instance_names = []
    with open("/home/centos/FIO_test/pssh_dir/pssh_host") as f:
        lines = f.readlines()
        for line in range(len(lines)):
            instance_names.append(lines[line].strip("\n"))
    final_r_iops = []
    final_r_lat = []
    final_r_cpu = []
    final_r_bw = []
    for instance in instance_names[0:no_of_instances]:
        read_iops = []
        latency = []
        cpu_util = []
        read_bw = []
        path = "/home/centos/FIO_test/fio-out/" + instance
        with open(path) as f:
            file_data = f.readlines()
            for line in file_data:
                if "read" in line and "IOPS" in line:
                    iops_data, bw_data = get_read_data(line)
                    read_iops.append(iops_data)
                    read_bw.append(bw_data)
                if " lat" in line and "avg" in line:
                    latency_data = get_latency_data(line)
                    latency.append(latency_data)
                if "cpu" in line:
                    cpu_util_data = get_cpu_data(line)
                    cpu_util.append(cpu_util_data)

        if not final_r_iops and not final_r_lat:
            final_r_iops = read_iops
            final_r_lat = latency
            final_r_cpu = cpu_util
            final_r_bw = read_bw
        else:
            final_r_iops = [sum(x) for x in zip(final_r_iops, read_iops)]
            final_r_lat = [sum(x) for x in zip(final_r_lat, latency)]
            final_r_cpu = [sum(x) for x in zip(final_r_cpu, cpu_util)]
            final_r_bw = [sum(x) for x in zip(final_r_bw, read_bw)]

    final_r_iops = get_average(final_r_iops, no_of_instances)
    final_r_lat = get_average(final_r_lat, no_of_instances)
    final_r_cpu = get_average(final_r_cpu, no_of_instances)
    final_r_bw = get_average(final_r_bw, no_of_instances)

    # Printing final outputs...

    print("Seq-read Output of " + str(no_of_instances) + " Instances ")
    print("read_iops = ", final_r_iops)
    print("read_latency (msec)= ", final_r_lat)
    print("read_cpu = ", final_r_cpu)
    print("read_bw (MB/s) = ", final_r_bw)


def sequential_write():
    """
    This function executes 1M Sequential Writes for
    iodepth (1,2,4,8,16,32,64,128) and gets read-iops, read_latency,
    read_bandwidth and cpu utilization for the respective no_of_instances..

    """
    command = 'sudo pssh -h pssh_host ' \
              '-t 1000000000 -x "-o StrictHostKeyChecking=no ' \
              '-i /home/centos/centos.pem" ' \
              '-o /home/centos/FIO_test/fio-out -I<./seqwrite_cmd.sh'
    subprocess.call(command, shell=True)
    instance_names = []
    with open("/home/centos/FIO_test/pssh_dir/pssh_host") as f:
        lines = f.readlines()
        for line in range(len(lines)):
            instance_names.append(lines[line].strip("\n"))
    final_w_iops = []
    final_w_lat = []
    final_w_cpu = []
    final_w_bw = []
    for instance in instance_names[0:no_of_instances]:
        write_iops = []
        latency = []
        cpu_util = []
        write_bw = []
        path = "/home/centos/FIO_test/fio-out/" + instance
        with open(path) as f:
            file_data = f.readlines()
            for line in file_data:
                if "write" in line and "IOPS" in line:
                    iops_data, bw_data = get_write_data(line)
                    write_iops.append(iops_data)
                    write_bw.append(bw_data)
                if " lat" in line and "avg" in line:
                    latency_data = get_latency_data(line)
                    latency.append(latency_data)
                if "cpu" in line:
                    cpu_util_data = get_cpu_data(line)
                    cpu_util.append(cpu_util_data)

        if not final_w_iops and not final_w_lat:
            final_w_iops = write_iops
            final_w_lat = latency
            final_w_cpu = cpu_util
            final_w_bw = write_bw
        else:
            final_w_iops = [sum(x) for x in zip(final_w_iops, write_iops)]
            final_w_lat = [sum(x) for x in zip(final_w_lat, latency)]
            final_w_cpu = [sum(x) for x in zip(final_w_cpu, cpu_util)]
            final_w_bw = [sum(x) for x in zip(final_w_bw, write_bw)]

    final_w_iops = get_average(final_w_iops, no_of_instances)
    final_w_lat = get_average(final_w_lat, no_of_instances)
    final_w_cpu = get_average(final_w_cpu, no_of_instances)
    final_w_bw = get_average(final_w_bw, no_of_instances)

    # Printing final outputs...

    print("Seq-write Output of " + str(no_of_instances) + " Instances ")
    print("write_iops = ", final_w_iops)
    print("write_latency (msec)= ", final_w_lat)
    print("write_cpu = ", final_w_cpu)
    print("write_BW (MB/s) = ", final_w_bw)


def main():
    random_write()
    subprocess.call('sudo pssh -h pssh_host -x "-o StrictHostKeyChecking=no '
                    '-i /home/centos/centos.pem" "rm -rf test"', shell=True)
    random_read()
    subprocess.call('sudo pssh -h pssh_host -x "-o StrictHostKeyChecking=no '
                    '-i /home/centos/centos.pem" "rm -rf test"', shell=True)
    sequential_write()
    subprocess.call('sudo pssh -h pssh_host -x "-o StrictHostKeyChecking=no '
                    '-i /home/centos/centos.pem" "rm -rf test"', shell=True)
    sequential_read()
    subprocess.call('sudo pssh -h pssh_host -x "-o StrictHostKeyChecking=no '
                    '-i /home/centos/centos.pem" "rm -rf test"', shell=True)


if __name__ == "__main__":
    main()
