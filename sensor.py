from bluepy.btle import Scanner, DefaultDelegate
import requests

valid_sensors = {
    "a4:c1:38:ff:ff:f1" : "kitchen",
    "a4:c1:38:ff:ff:f2" : "bathroom",
    "a4:c1:38:ff:ff:f3" : "bedroom",
    "a4:c1:38:ff:ff:f4" : "living",
    "a4:c1:38:ff:ff:f5" : "living2",
    "a4:c1:38:ff:ff:f6" : "outdoor"
}

influxdb = 'http://10.2.4.4:8086/write?db=home'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def shipToInfluxDb(self, sensor_mac, temp, humidity, battery):
        x1 = requests.post(influxdb, "temperature,mac=%s value=%s"%(sensor_mac,temp))
        x2 = requests.post(influxdb, "humidity,mac=%s value=%s"%(sensor_mac,humidity))
        x3 = requests.post(influxdb, "battery,mac=%s value=%s"%(sensor_mac,battery))
        #print(x1.status_code)
        #print(x2.status_code)
        #print(x3.status_code)

    def handleSensorPacket(self, sensor_mac, data):
        data = bytes.fromhex(data)  
        name = valid_sensors[sensor_mac]
        temperature = int.from_bytes(data[8:10],byteorder='big',signed=True)
        temperature = str(temperature / 10)
        humidity = int.from_bytes(data[10:11],byteorder='big',signed=True)
        humidity = str(humidity)
        battery = int.from_bytes(data[11:12],byteorder='big',signed=True)
        #print("%s = %s , %s , %s"%(name,temperature,humidity, str(battery)))
        with open("/tmp/sensor_"+name, 'w') as f:
            f.write(temperature)
        
        self.shipToInfluxDb(sensor_mac, temperature, humidity, battery)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if(dev.addr in valid_sensors):
            for (adtype, desc, value) in dev.getScanData():
                if("Service" in desc):
                    self.handleSensorPacket(dev.addr, value)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(20.0)
