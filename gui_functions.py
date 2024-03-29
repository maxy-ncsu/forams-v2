import sys
import glob
import serial

class Solenoids:
    def __init__(self):
        print("solenoids initialized")
        self.state = [0, 0, 0, 0, 0]

    def changeSolenoid(self, sol):
        status = "opened"
        if self.state[sol]: status = "closed"
        self.state[sol] = ~self.state[sol]

        print("solenoid " + str(sol) + " " + status)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :raises RuntimeError:
            No ports found
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    if (len(result) < 1):
        raise RuntimeError('No ports detected')

    return result