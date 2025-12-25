from PySide6 import QtWidgets

from functions import load_ui


class EntryView(QtWidgets.QDialog):
    def __init__(self, parent=None, text=None, name=None, date=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр записи")
        self.ui = load_ui("ui/entry_view.ui", self)
        self.setLayout(self.ui.layout())
        self.ui.date.setText(date)
        self.ui.name.setText(name)
        self.ui.text.setPlainText(text)
