# HandCar
# (By) Xoán Carlos Cosmed Peralejo

# This is the software that is executed in the computer which has the Leap Motion controller attached and the Arduino connected via serial port.

#enconding: utf-8

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import serial

import sys, os, thread, time, math

def SerialInit():
    return serial.Serial(
        #port='/dev/tty.usbmodemFD121',
        port='/dev/cu.usbmodemFD121',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

def SerialSend(ser, dato1, dato2, dato3, dato4):
    if ser is None:
        ser = SerialInit()
    mes = str(dato1) + '_' + str(dato4) + ':::' + str(dato2) + '_' + str(dato3) + '*'
    ser.write(mes)

def SendData(dato1, dato2, dato3, dato4):
    os.system('clear')

    print "\n\n\n"
    print "\t\t\t\t\t" + str(dato1) + "\t\t\t\t\t"
    print "\n\n\n\n\n"
    print "\t\t\t" + str(dato2) + "\t\t\t\t" + str(dato3) + "\t\t\t"
    print "\n\n\n\n\n"
    print "\t\t\t\t\t" + str(dato4) + "\t\t\t\t\t"
    print "\n\n\n"

class LeapMotionListener(Leap.Listener):

    # finger_names = ['Pulgar', 'Indice', 'Corazon', 'Anular', 'Meñique']
    # bone_names = ['Metacarpo', 'Proximal', 'Intermedio', 'Distal']
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarp', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    cont = int(0);

    def on_init(self, controller):
        print "Initializing"
        self.ser = SerialInit()

    def on_connect(self, controller):
        print "Sensor connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Sensor disconnected"

    def on_exit(self, controller):
        print "Exiting"
        self.ser.close()

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.hands) == 0:
            SendData(0, 0, 0, 0)
        #    SerialSend(self.ser, 0, 0, 0, 0) # Experiment! Uncomment?

        for hand in frame.hands:

            if hand.is_right:
                normal = hand.palm_normal
                direction = hand.direction

                dato1 = int(0)
                dato2 = int(0)
                dato3 = int(0)
                dato4 = int(0)

                if direction.pitch < -0.15:
                    dato1 = int(10*abs(direction.pitch))
                    if dato1 > 9:
                        dato1 = 9

                if direction.pitch > 0.15:
                    dato4 = int(10*abs(direction.pitch))
                    if dato4 > 9:
                        dato4 = 9

                if normal.roll < -0.15:
                    dato3 = int(10*abs(normal.roll))
                    if dato3 > 9:
                        dato3 = 9

                if normal.roll > 0.15:
                    dato2 = int(10*abs(normal.roll))
                    if dato2 > 9:
                        dato2 = 9

                SendData(dato1, dato2, dato3, dato4)
                fps = int(frame.current_frames_per_second)  # Trial
                print str(fps)  # Trial

                if self.cont > 100: # Attention
                    SerialSend(self.ser, dato1, dato2, dato3, dato4)
                    self.cont = 0
                else:
                    self.cont = self.cont + 1


def main():
    SendData(0,0,0,0)

    self.ser = SerialInit()

    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press ENTER to exit"

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()


# (By) Xoan Carlos Cosmed Peralejo
