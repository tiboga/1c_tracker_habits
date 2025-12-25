from PySide6 import QtWidgets

from functions import load_ui, add_diary_entry


class AddingEntry(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись в дневник")
        self.ui = load_ui("ui/adding_diary_entry.ui", self)
        self.setLayout(self.ui.layout())
        self.ui.name.textChanged.connect(self.text_changed)
        self.ui.text.textChanged.connect(self.text_changed)
        self.ui.buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.ui.buttonBox.accepted.connect(self.add_entry)
        self.ui.buttonBox.rejected.connect(self.reject)

    def add_entry(self):
        add_diary_entry(self.ui.name.text(), self.ui.text.toPlainText())
        self.accept()

    def text_changed(self):
        if self.ui.name.text() == "" or self.ui.text.toPlainText() == "":
            self.ui.buttonBox.button(
                QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.ui.buttonBox.button(
                QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
