# app-iperf3
###  Catalyst 9000 Series Docker Build for Iperf

This Readme covers how to build a custom Iperf Docker app for use on Catalyst 9000 Series AppHosting Framework.

--

### Docker Build

Navigate to the cloned repository directory and build the docker image:

```
docker build -t app-iperf3 .
```

### Docker Verify

To verify the image has been successfully built:

```
jerbuck$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
app-iperf3       latest    3332c0686934   18 minutes ago   120MB

```

### Docker Run 

```
docker run -it --rm -p 5201:5201 app-iperf3
```

### Docker Export

You can then export the docker image for installation onto Catalyst 9000 series using:

```
docker save app-iperf3 -o app-iperf3.tar

jerbuck$ ls -ail
total 248728
54384971 drwxr-xr-x   6 jerbuck  staff        192 Jul 16 09:47 .
54386477 drwxr-xr-x   3 jerbuck  staff         96 Jul 16 09:20 ..
54384972 drwxr-xr-x  15 jerbuck  staff        480 Jul 16 09:20 .git
54386053 -rw-r--r--   1 jerbuck  staff        750 Jul 16 09:17 Dockerfile
54414249 -rw-r--r--@  1 jerbuck  staff       4361 Jul 16 09:44 README.md
54414692 -rw-------   1 jerbuck  staff  125520384 Jul 16 09:47 app-iperf3.tar
```

### Licensing

Ensure that the switch is licensed for DNA-Advantage

```
license boot level network-advantage addon dna-advantage
```


### Connecting app to Catalyst 9000 Series
```
! Configured on switch
!
app-hosting appid iperf
 app-vnic AppGigabitEthernet trunk
  vlan 100 guest-interface 0
   guest-ipaddress 192.168.10.2 netmask 255.255.255.0
 app-default-gateway 192.168.10.1 guest-interface 0
 app-resource docker
  run-opts 1 "--restart=unless-stopped -p 5201:5201/tcp -p 5201:5201/udp"
!
!
int AppGigEthernet 1/0/1
  switchport mode trunk
  switchport trunk allowed vlan 100 
!
```

### Enable Cisco IOX

```
#configure terminal
(config)#iox
(config)#exit

```

### Installing app on Catalyst 9000 Series

```
! Copy the image onto the switch usbflash1 or SSD using SCP, FTP, TFTP, etc.
!
switch# app-hosting install appid iperf package usbflash1:app-iperf3.tar
!
```

### Activating app on Catalyst 9000 Series

```
!
switch# app-hosting activate appid iperf
!
```

### Starting app on Catalyst 9000 Series

```
!
switch# app-hosting start appid iperf
!
```

### Stopping app on Catalyst 9000 Series

```
!
switch# app-hosting stop appid iperf
!
```

### Deactivating app on Catalyst 9000 Series

```
!
switch# app-hosting deactivate appid iperf
!
```

### Uninstalling app on Catalyst 9000 Series

```
!
switch# app-hosting uninstall appid iperf
!
```

### Catalyst 9000 Usage

When you start a container it will launch a server by default. You can test this by connecting to it over the loopback.
```
switch# app-hostings connect appid iperf session
iperf3 -c 127.0.0.1
```

Once you have deployed the container on multiple switches, verify you have ip reachability. Once you've verified reachability you can run bandwidth tests as follows:

```
/ # iperf3 -c 192.168.10.2
Connecting to host 192.168.10.2, port 5201
[  5] local 192.168.20.2 port 52286 connected to 192.168.10.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec   115 MBytes   961 Mbits/sec    0   1.60 MBytes       
[  5]   1.00-2.00   sec   112 MBytes   944 Mbits/sec    0   1.60 MBytes       
[  5]   2.00-3.00   sec   111 MBytes   933 Mbits/sec   30   1.60 MBytes       
[  5]   3.00-4.00   sec   112 MBytes   944 Mbits/sec   11   1.60 MBytes       
[  5]   4.00-5.00   sec   111 MBytes   933 Mbits/sec  841   1.60 MBytes       
[  5]   5.00-6.00   sec   111 MBytes   933 Mbits/sec    0   1.60 MBytes       
[  5]   6.00-7.00   sec   112 MBytes   944 Mbits/sec   22   1.60 MBytes       
[  5]   7.00-8.00   sec   111 MBytes   933 Mbits/sec  296   1.60 MBytes       
[  5]   8.00-9.00   sec   111 MBytes   933 Mbits/sec    7   1.60 MBytes       
[  5]   9.00-10.00  sec   112 MBytes   944 Mbits/sec  179   1.60 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  1.09 GBytes   940 Mbits/sec  1386             sender
[  5]   0.00-10.05  sec  1.09 GBytes   934 Mbits/sec                  receiver

iperf Done.
/ # 

```

This cannot be used to test multicast as Docker does not support multicast natively without additional complexities.

Iperf is very capable, there are many options in how you run tests, these can be found [here](https://iperf.fr/iperf-doc.php#3doc).


Customized fork from nerdalert/app-iperf3 and michellabbe/docker-iperf3.
