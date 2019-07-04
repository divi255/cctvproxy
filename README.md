# CCTV camera image proxy

## What's that

You have CCTV camera which gives you image snapshot and want to add it
somewhere e.g. to your internal web page, refreshing periodically.

Problem: camera is password protected and you don't want to be continuously
prompted for the credentials

Problem 2: sometimes your camera may die and you want to display some pretty
error image.

Solution:

```bash
pip3 install cctvproxy
# put this string somewhere to your system startup
cctv-proxy.sh start
```

## Usage

*http://cctv-proxy-ip:port/ci?_id=CAM_ID&.....*

Params:

* **_id** camera id
* **_return** if "raw" - return raw response from camera, if "test" - test
  camera and return OK (or FAILED)

All other params are passed to CCTV camera as-is.

CCTV Proxy was made for AXIS cameras but you can configure it for almost any.

## Config file

Default config file should be located at */usr/local/etc/cctv-proxy.yml*

You can specify alternative location with *-f* option.

```yaml
#bind-host: 127.0.0.1
#bind-port: 8781
#pool: 30
login: axisusername
password: axispassword
# change for non-AXIS cameras
#uri: /axis-cgi/jpg/image.cgi
cams:
  cam1: 192.168.55.1
  cam2: 192.168.55.1
  cam3: 192.168.55.1
timeout: 5
#user: nobody
#group: nogroup
# change for each instance
#pid: /tmp/cctv-proxy.pid
# if no image available
#no-image: /data/nocam.jpg
```

## Debug

```bash
python3 -m cctvproxy.proxy [-f config_file] -D
```

## TODO

Image processing. Sometime later. I don't need it - [EVA
ICS](https://www.eva-ics.com/) has built-in.
