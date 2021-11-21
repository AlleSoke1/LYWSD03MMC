# LYWSD03MMC
Reading data from LYWSD03MMC BLE Broadcast with ATC Custom firmware


Xiaomi Temperature/Humidity sensor sends regular bluetooth low energy beacon packets/broadcast packets with its current temperature/huimidity/battery level.
For that to work, it has to be flashed with [ATC costum firmware](https://github.com/atc1441/ATC_MiThermometer) in order to disable packet encryption (can be done with official firmware but the packet structure is different and and you'll also need a bindingkey)
