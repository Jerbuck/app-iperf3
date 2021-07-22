# app-iperf3
###  Catalyst 9000 Series Iperf3 Docker Build for Iperf

This Readme covers how to build a custom Iperf Docker app for use on Catalyst 9000 Series AppHosting Framework.

--

### Build

Navigate to the cloned repository directory and build the docker image:

```
docker build -t app-iperf3
```

### Verify

To verify the image has been successfully built:

```
jerbuck$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
app-iperf3       latest    3332c0686934   18 minutes ago   120MB

```

### Run 

```
docker run -it --rm -p 5201:5201 app-iperf3 --help
```

### Export

You can then export the docker image for installation onto Catalyst 9000 series using:

```
docker save -o app-iperf3.tar app-iperf3

jerbuck$ ls -ail
total 248728
54384971 drwxr-xr-x   6 jerbuck  staff        192 Jul 16 09:47 .
54386477 drwxr-xr-x   3 jerbuck  staff         96 Jul 16 09:20 ..
54384972 drwxr-xr-x  15 jerbuck  staff        480 Jul 16 09:20 .git
54386053 -rw-r--r--   1 jerbuck  staff        750 Jul 16 09:17 Dockerfile
54414249 -rw-r--r--@  1 jerbuck  staff       4361 Jul 16 09:44 README.md
54414692 -rw-------   1 jerbuck  staff  125520384 Jul 16 09:47 app-iperf3.tar
```

If you are unable to build and export this container, you can download the .tar file directly [here](https://cisco.box.com/s/804kbwz7vlupot53m77vvrs6h192i992).

### Installing app on Catalyst 9000 Series

```
! Copy the image onto the switch usbflash1 or SSD using SCP, FTP, TFTP, etc.
!
app-hosting install appid app-iperf3 package usbflash1:app-iperf3.tar
!
```

### Activating app on Catalyst 9000 Series

```
!
app-hosting activate appid app-iperf3
!
```

### Starting app on Catalyst 9000 Series

```
!
app-hosting start appid app-iperf3
!
```

### Stopping app on Catalyst 9000 Series

```
!
app-hosting stop appid app-iperf3
!
```

### Deactivating app on Catalyst 9000 Series

```
!
app-hosting deactivate appid app-iperf3
!
```

### Uninstalling app on Catalyst 9000 Series

```
!
app-hosting uninstall appid app-iperf3
!
```
<br>
--
<br>

### Usage

To test bandwidth between two containers, start a server (listener) and point a client container (initiator) at the server.

For reference the Iperf3 documentation can be found [here](https://iperf.fr/iperf-doc.php#3doc).

#### app-iperf3 Server

Start a listener service on port 5201 and name the container "app-iperf3-server":

```
docker run  -it --rm --name=app-iperf3-server -p 5201:5201 app-iperf3 -s
```

That returns an app-iperf3 process bound to a socket waiting for new connections:

```
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```

#### app-iperf3 Client Side

First, get the IP address of the new server container you just started:

```
docker inspect --format "{{ .NetworkSettings.IPAddress }}" app-iperf3-server
!
! (Returned) 172.17.0.163
```

Next, initiate a client connection from another container to measure the bandwidth between the two endpoints.

Run a client container pointing at the server service IP address. 

*Note* if you are new to Docker, the  `--rm` flag will destroy the container after the test runs. I also left out explicitly naming the container on the client side since I don't need its IP address. I typically explicitly name containers for organization and to maintain a consistent pattern.

```
docker run  -it --rm app-iperf3 -c 172.17.0.163
```

And the output is the following:

```
Connecting to host 172.17.0.163, port 5201
[  4] local 172.17.0.191 port 51148 connected to 172.17.0.163 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec  4.16 GBytes  35.7 Gbits/sec    0    468 KBytes
[  4]   1.00-2.00   sec  4.10 GBytes  35.2 Gbits/sec    0    632 KBytes
[  4]   2.00-3.00   sec  4.28 GBytes  36.8 Gbits/sec    0   1.02 MBytes
[  4]   3.00-4.00   sec  4.25 GBytes  36.5 Gbits/sec    0   1.28 MBytes
[  4]   4.00-5.00   sec  4.20 GBytes  36.0 Gbits/sec    0   1.37 MBytes
[  4]   5.00-6.00   sec  4.23 GBytes  36.3 Gbits/sec    0   1.40 MBytes
[  4]   6.00-7.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.40 MBytes
[  4]   7.00-8.00   sec  4.14 GBytes  35.6 Gbits/sec    0   1.40 MBytes
[  4]   8.00-9.00   sec  4.29 GBytes  36.8 Gbits/sec    0   1.64 MBytes
[  4]   9.00-10.00  sec  4.15 GBytes  35.7 Gbits/sec    0   1.68 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  42.0 GBytes  36.1 Gbits/sec    0             sender
[  4]   0.00-10.00  sec  42.0 GBytes  36.0 Gbits/sec                  receiver

iperf Done.
```

Or you can do something fancier in a one liner like so (docker ps -ql returns the CID e.g. container ID of the last container started which would be the server we want in this case)

```
docker run  -it --rm app-iperf3 -c $(docker inspect --format "{{ .NetworkSettings.IPAddress }}" $(docker ps -ql))
Connecting to host 172.17.0.193, port 5201
[  4] local 172.17.0.194 port 60922 connected to 172.17.0.193 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec  4.32 GBytes  37.1 Gbits/sec    0    877 KBytes
[  4]   1.00-2.00   sec  4.28 GBytes  36.7 Gbits/sec    0   1.01 MBytes
[  4]   2.00-3.00   sec  4.18 GBytes  35.9 Gbits/sec    0   1.01 MBytes
[  4]   3.00-4.00   sec  4.23 GBytes  36.3 Gbits/sec    0   1.13 MBytes
[  4]   4.00-5.00   sec  4.20 GBytes  36.1 Gbits/sec    0   1.27 MBytes
[  4]   5.00-6.00   sec  4.19 GBytes  36.0 Gbits/sec    0   1.29 MBytes
[  4]   6.00-7.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   7.00-8.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   8.00-9.00   sec  4.17 GBytes  35.8 Gbits/sec    0   1.29 MBytes
[  4]   9.00-10.00  sec  4.22 GBytes  36.3 Gbits/sec    0   1.29 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  42.1 GBytes  36.2 Gbits/sec    0             sender
[  4]   0.00-10.00  sec  42.1 GBytes  36.2 Gbits/sec                  receiver

iperf Done.
```

Thanks to ESNET for re-rolling iperf from the ground up. It is a killer piece of software.

Customized fork from nerdalert/app-iperf3.
