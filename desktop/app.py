"""Load and save speetings for particular classes"""
import sys
import os
import json
from PySide6.QtWidgets import QApplication,QMainWindow,QFileDialog
import class_settings

class SettingsWindow(QMainWindow):
    """Class settings window handlers"""
    def __init__(self):
        """Setup local variables"""
        super().__init__()
        self.ui=class_settings.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.action_load.triggered.connect(self.load_file)
        self.ui.action_Save.triggered.connect(self.save_file)

    def load_file(self):
        """Load a file"""
        fd=QFileDialog.getOpenFileName(self,filter="*.bcs")
        print(fd[0])
        with open(fd[0], encoding='UTF-8') as settings_file:
            file_string=settings_file.read()
            file_data=json.loads(file_string)
            self.ui.TimeLimitMinute.setText(file_data.get('TimeLimitMinute','3'))
            self.ui.TimeLimitSecond.setText(file_data.get('TimeLimitSecond','0'))
            self.ui.PitOpenTimeMinute.setText(file_data.get('PitOpenTimeMinute','2'))
            self.ui.PitOpenTimeSecond.setText(file_data.get('PitOpenTimeSecond','0'))
            self.ui.CountdownDuration.setText(file_data.get('CountdownDuration','10'))
            self.ui.ActivePits.setChecked(file_data.get('ActivePits',True))
            self.ui.CompControls.setChecked(file_data.get('CompControls',True))
            self.ui.BlinkingLights.setChecked(file_data.get('BlinkingLight',True))

    def save_file(self):
        """Save a file"""
        fd=QFileDialog.getSaveFileName(self,filter="*.bcs",)
        fn=os.path.basename(fd[0])
        path=os.path.dirname(fd[0])
        file_data={
        'TimeLimitMinute':self.ui.TimeLimitMinute.text(),
        'TimeLimitSecond':self.ui.TimeLimitSecond.text(),
        'PitOpenTimeMinute':self.ui.PitOpenTimeMinute.text(),
        'PitOpenTimeSecond':self.ui.PitOpenTimeSecond.text(),
        'CountdownDuration':self.ui.CountdownDuration.text(),
        'ActivePits':self.ui.ActivePits.isChecked(),
        'CompControls':self.ui.CompControls.isChecked(),
        'BlinkingLights':self.ui.BlinkingLights.isChecked()
        }
        if not '.' in fn:
            fn=fn+".bcs"
        new_filespec=os.path.join(path,fn)
        print(new_filespec)
        with open(new_filespec,"w", encoding='UTF-8') as save_file:
            save_file.write(json.dumps(file_data))

app=QApplication()
settings_window=SettingsWindow()
settings_window.show()
sys.exit(app.exec())
