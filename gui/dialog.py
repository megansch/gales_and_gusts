import os
from PyQt5 import QtCore, QtWidgets

from train_tracks import train_tracks


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None, options=None):
        super(Dialog, self).__init__(parent)
        self.setMinimumSize(500, 500)

        self.options = options

        self.setWindowTitle("Gales and Gusts")
        self.dialog_layout = QtWidgets.QVBoxLayout(self)

        self.form_layout = QtWidgets.QFormLayout()
        self.add_browse_to_train_dir()
        #self.add_browse_to_out_dir()
        self.dialog_layout.addLayout(self.form_layout)

        self.add_train_button()
        self.add_progress_bar()

    def open_folder(self):
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)
        if dir_name:
            dir_name = os.path.normpath(dir_name)

        self.train_dir.setText(dir_name)

    def add_train_button(self):
        train_layout = QtWidgets.QHBoxLayout()
        self.train_button = QtWidgets.QPushButton('Train')
        self.train_button.setEnabled(False)
        self.train_button.clicked.connect(self.train_tracks)
        train_layout.addWidget(self.train_button)
        self.dialog_layout.addLayout(train_layout)

    def train_tracks(self):

        if not self.valid_inputs():
            return

        num_files = 10
        self.progress_widget.setMaximum(num_files)
        self.progress_widget.setValue(0)
        try:
            train_tracks(self.train_dir.text(), self.options.all)
        except Exception as err:
            QtWidgets.QMessageBox.Critical(self,
                                           'Runtime Error',
                                           str(err))
        self.progress_widget.setValue(5)
        self.progress_widget.setValue(10)

    def add_browse_to_train_dir(self):
        browse_layout = QtWidgets.QHBoxLayout()

        self.train_dir = QtWidgets.QLineEdit()
        self.train_dir.setReadOnly(True)
        browse_layout.addWidget(self.train_dir)

        browse_button = QtWidgets.QPushButton("Browse...")
        browse_button.clicked.connect(self.open_folder)
        browse_button.clicked.connect(self.enable_train_button)
        browse_layout.addWidget(browse_button)

        self.form_layout.addRow('Train Dir:', browse_layout)

    def add_progress_bar(self):
        progress_layout = QtWidgets.QHBoxLayout()
        self.progress_widget = QtWidgets.QProgressBar()
        self.progress_widget.setAlignment(QtCore.Qt.AlignCenter)
        progress_layout.addWidget(self.progress_widget)
        self.dialog_layout.addLayout(progress_layout)

    def valid_inputs(self):
        print(self.train_dir.text())
        if self.train_dir.text() == '':
            return False

        if os.path.isdir(self.train_dir.text()):
            return True

    def enable_train_button(self):
        self.train_button.setEnabled(self.valid_inputs())
