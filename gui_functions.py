# libraries
import sys
import glob
import serial
from hamamatsu.dcam import copy_frame, dcam, Stream
import logging

# Class that stores and prints the states of the solenoids
# 0 is closed, 1 is open
class Solenoids:
    # Solenoid valves all closed initially
    def __init__(self):
        print("camera and solenoids initialized")
        self.state = [0, 0, 0, 0, 0]

    # Updates state of solenoid, each index corresponding to solenoid 1,2,3,4,5
    # Prints if solenoid now closed or opened
    def changeSolenoid(self, sol):
        status = "opened"
        if self.state[sol]: status = "closed"
        self.state[sol] = ~self.state[sol]

        print("solenoid " + str(sol) + " " + status)

# Returns list of available serial ports
def serial_ports():
    # Based on OS
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    # Searches through list of ports to find available one
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    # No ports detected
    if (len(result) < 1):
        raise RuntimeError('No ports detected')

    return result

# Code used for Hamamatsu camera image acquisition in other project, ignore
def gen_acquire(device, exposure_time=1, nb_frames=1):
    """Simple acquisition example"""
    device["exposure_time"] = exposure_time
    with Stream(device, nb_frames) as stream:
        logging.info("start acquisition")
        device.start()
        for frame in stream:
            yield copy_frame(frame)
        logging.info("finished acquisition")

# Code used for Hamamatsu camera image acquisition in other project, ignore
def get_image(exposure_time=0.1, nb_frames=1):
    with dcam:
        with dcam[0] as camera:
            for i, frame in enumerate(
                gen_acquire(camera, exposure_time, nb_frames)
            ):
                logging.info(
                    f"Frame #{i+1}/{nb_frames} {frame.shape} {frame.dtype}"
                )
                return frame