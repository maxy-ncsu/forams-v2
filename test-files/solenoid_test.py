import serial
import time

# opening arduino comms
arduino = serial.Serial(port='/dev/tty.usbmodem1101', baudrate=9600, timeout=.1)
time.sleep(2)

for i in range(1, 6):
    arduino.write(str.encode(str(i)))
    time.sleep(10)


#arduino.write(str.encode('3'))
#print('measure me')
#time.sleep(60)


arduino.write(str.encode('0'))
time.sleep(2)
arduino.close()