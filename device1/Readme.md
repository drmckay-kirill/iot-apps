# Device emulator
### python3
### CoAP on application level
##### docker build -t iot/device1 .
##### docker run -it -d -v /c/Users/sienc/iot_apps/device1:/mnt/code -p 5684:5684 iot/device1