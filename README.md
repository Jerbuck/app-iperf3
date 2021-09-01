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
  app-vnic AppGigEthernet trunk
   vlan 100 guest-interface 0 
   guest-ipaddress 172.17.0.2 netmask 255.255.255.0
  app-default-gateway 172.17.0.1 guest-intereface 0
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
<br>
--
<br>

### Docker Usage

**Add this**

### Catalyst 9000 Usage

**Add this**


Customized fork from nerdalert/app-iperf3.
