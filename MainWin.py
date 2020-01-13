import sys
import subprocess
import re
import os
from optparse import OptionParser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from Ui_MainWin import Ui_MainWindow

statusFlag = {'--enable': 'Enabled', '--disable': 'Disabled'}

# Gets the touch device ID
def getDeviceId():
    try:
        data = subprocess.check_output(['xinput', '--list'])
    except Exception:
        print("xinput not found!")
        sys.exit();

    deviceId = 'none'

    for line in data.splitlines():
        line = line.lower()
        line = str(line)
        if "touchpad" in line and "pointer" in line:
            line = line.strip()
            match = re.search('id=([0-9]+)', line)
            deviceId = str(match.group(1))
            # print(deviceId)
            # print(line)

    if deviceId == 'none':
        print('Touch Device not found')
        sys.exit();

    return deviceId


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # Connect signals to slot
        # When program starts  disable touchpad
        command = "xinput --disable " + getDeviceId()
        os.system(command)
        self.ui.checkBox.clicked.connect(lambda: self.checkBoxChangedAction())


    def show(self):
        self.main_win.show()

    def checked(self):
        self.ui.checkBox.setText('Checked')

    def uncheck(self):
        self.ui.checkBox.setText('Uncheck')

    def checkBoxChangedAction(self):
        if (self.ui.checkBox.isChecked() == True):
            command = "xinput --enable " + getDeviceId()
            os.system(command)
        else:
            command = "xinput --disable " + getDeviceId()
            os.system(command)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())