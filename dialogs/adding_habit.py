from PySide6 import QtWidgets

from functions import load_ui, save_habits


class AddingHabit(QtWidgets.QDialog):
    def __init__(self, parent=None, habit_class=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить привычку")
        self.ui = load_ui("ui/adding_habit.ui", self)
        self.setLayout(self.ui.layout())
        self.ui.buttonBox.accepted.connect(self.add_habit)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.habit_class = habit_class

    def add_habit(self):
        habit_name = self.ui.name_habit_lineEdit.text()
        habit_points = self.ui.points_habit_spinBox.value()
        save_habits(habit_name, self.habit_class, habit_points)
        self.accept()
