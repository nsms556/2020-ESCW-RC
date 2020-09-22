from time import sleep, time

import cwiid as WII

class Wiimote :
    def __init__(self) :
        print("Press Wiimote 1 + 2 Button to Connection")
        sleep(1)

        try :
            self.wii = WII.Wiimote()
        except RuntimeError :
            print("Wiimote Failed")
            quit()

        self.wii.rpt_mode = WII.RPT_BTN | WII.RPT_ACC
    
        print("Quit to Press Buttons + and -")
        sleep(1)

    def __del__(self) :
        print("Wiimote Power Off")

        self.wii.rumble = 1
        sleep(0.5)
        self.wii.rumble = 0
        sleep(0.5)

    def getButtonState(self) :
        return self.wii.state['buttons']
    
    def getAccState(self) :
        return self.wii.state['acc']

if __name__ == "__main__" :
    wii = Wiimote()

    while True :
        buttons = wii.getButtonState()
        acc = wii.getAccState()

        if buttons & WII.BTN_PLUS and buttons & WII.BTN_MINUS :
            del(wii)
            break

        print(buttons)
        print(acc)

        sleep(0.2)

