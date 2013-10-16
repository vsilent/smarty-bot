#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Control robot's neck stepper motor 1
    default port 888 (378h)
    One motor turnover takes 200 steps
"""
import parallel
import time

#SELECT_IN_PORT  = 890   #890
TURNOVER = 200          # turnover steps
CLOCKWISE = 1          # rotate clockwise
ANTICLOCKWISE  = -1     # rotate counterclockwise
#DELAY = 0.005            # delay between steps
#DELAY = 0.001            # delay between steps
DELAY = 0.01            # delay between steps for test
RESET_DELAY = 0.0005
#RESET_DELAY = 0.005


class StepperMotor():

    def __init__( self ):
        """docstring for __init__"""
        self.port = parallel.Parallel()
        self.reset_port()

    def reset_port( self ):
        #self.port.setData(0xff)
        #self.port.setData(0x00)
        pass

    def step( self, direction, delay ):
        """docstring for step_clockwise"""
        if direction == 1:
            for i in range (4):
                byte = 1 << i
                print('Send %s' % byte)
                self.port.setData(byte)
                self.port.setInitOut(0)
                time.sleep(RESET_DELAY)
                self.port.setInitOut(1)
                time.sleep(delay)
        elif direction == -1:
            for i in range (4):
                byte = 8 >> i
                print('Send %s' % byte)
                self.port.setData(byte)
                time.sleep(RESET_DELAY)
                self.port.setInitOut(0)
                time.sleep(RESET_DELAY)
                self.port.setInitOut(1)
                time.sleep(delay)

    def rotate( self, direction, steps ):
        """docstring for rotate_clockwise"""
        for step in range(steps):
            self.step( direction, DELAY )


class StepperMotor1():

    def __init__( self ):
        """docstring for __init__"""
        self.port = parallel.Parallel()

    def reset_port( self ):
        self.port.setData(0xf0)
        self.port.setInitOut(0)
        time.sleep(RESET_DELAY)
        self.port.setInitOut(1)

    def step( self, direction, delay ):
        """docstring for step_clockwise"""
        if direction == 1:
            #add
            self.port.setData(0x01)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x03)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x06)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x0c)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x09)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #self.port.setData(0x0c)
            #self.port.setInitOut(0)
            #time.sleep(RESET_DELAY)
            #self.port.setInitOut(1)
            #time.sleep(delay)

            ##add
            #self.port.setData(0x08)
            #self.port.setInitOut(0)
            #time.sleep(RESET_DELAY)
            #self.port.setInitOut(1)
            #time.sleep(delay)

            self.port.setData(0x09)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)


        elif direction == -1:
            #for i in range (4):
                #byte = 80 >> i
                #print('Send %s' % byte)
                #self.port.setData(byte)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(0)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(1)
                #time.sleep(delay)

            self.port.setData(0x09)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x0c)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x06)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x03)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x01)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            ##add
            #self.port.setData(0x02)
            #self.port.setInitOut(0)
            #time.sleep(RESET_DELAY)
            #self.port.setInitOut(1)
            #time.sleep(delay)

            #self.port.setData(0x03)
            #self.port.setInitOut(0)
            #time.sleep(RESET_DELAY)
            #self.port.setInitOut(1)
            #time.sleep(delay)

            #self.port.setData(0x01)
            #self.port.setInitOut(0)
            #time.sleep(RESET_DELAY)
            #self.port.setInitOut(1)
            #time.sleep(delay)

    def rotate( self, direction, steps ):
        """docstring for rotate_clockwise"""
        for step in range(steps):
            self.step( direction, DELAY )

class StepperMotor2():

    def __init__( self ):
        """docstring for __init__"""
        self.port = parallel.Parallel()

    def reset_port( self ):
        self.port.setData(0x00)
        self.port.setInitOut(0)
        time.sleep(RESET_DELAY)
        self.port.setInitOut(1)

    def step( self, direction, delay ):
        """docstring for step_clockwise"""
        if direction == 1:
            #for i in range (4):
                #byte = 10 << i
                #print('Send %s' % byte)
                #self.port.setData(byte)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(0)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(1)
                #time.sleep(delay)

            #add
            self.port.setData(0x10)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x30)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x20)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x60)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x40)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0xc0)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x80)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x90)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)


        elif direction == -1:
            #for i in range (4):
                #byte = 80 >> i
                #print('Send %s' % byte)
                #self.port.setData(byte)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(0)
                #time.sleep(RESET_DELAY)
                #self.port.setInitOut(1)
                #time.sleep(delay)

            self.port.setData(0x90)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x80)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0xc0)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x40)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x60)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            #add
            self.port.setData(0x20)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x30)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

            self.port.setData(0x10)
            self.port.setInitOut(0)
            time.sleep(RESET_DELAY)
            self.port.setInitOut(1)
            time.sleep(delay)

    def rotate( self, direction, steps ):
        """docstring for rotate_clockwise"""
        for step in range(steps):
            self.step( direction, DELAY )

#if __name__ == '__main__':

    #motor2 = StepperMotor2()
    #motor2.rotate(CLOCKWISE, 15)
    #time.sleep(DELAY)
    #motor2.rotate(ANTICLOCKWISE, 15)
    #motor2.reset_port()
