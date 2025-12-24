from PySide6 import QtCore, QtWidgets, QtGui

from functions import delete_habits, update_stat


class HabitsHorizontalLayout(QtWidgets.QHBoxLayout):
    def __init__(self, h_id, parent=None, name="None", points=0,
                 habit_class=None, main_parent=None, ended=False):
        super().__init__(parent)
        self.ended = ended
        self.parent = parent
        self.id = h_id
        self.habit_class = habit_class
        self.main_parent = main_parent
        self.setSpacing(20)
        self.setContentsMargins(10, 10, 20, 10)
        self.name_label = QtWidgets.QLabel(name)
        self.points_label = QtWidgets.QLabel(str(points))
        self.points_label.setMaximumWidth(40)
        self.generate_buttons()
        self.addWidget(self.ok_button)
        self.addWidget(self.name_label)
        self.addWidget(self.points_label)
        self.addWidget(self.delete_button)
        self.update_stylesheet_of_container()

    def generate_buttons(self):
        self.delete_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon("imgs/delete_icon.png")
        self.delete_button.setIcon(icon)
        self.delete_button.setIconSize(QtCore.QSize(24, 24))
        self.delete_button.setStyleSheet("background-color: #802203;")
        self.delete_button.setMaximumWidth(40)
        self.delete_button.clicked.connect(self.delete_habit)
        self.ok_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon("imgs/ok.png")
        self.ok_button.setIcon(icon)
        self.ok_button.setIconSize(QtCore.QSize(24, 24))
        self.ok_button.setStyleSheet("background-color: #3f8f3d;")
        self.ok_button.setMaximumWidth(40)
        self.ok_button.clicked.connect(self.update_stat)

    def delete_habit(self):
        delete_habits(self.id, self.habit_class)
        self.main_parent.update_tab()

    def update_stat(self):
        self.ended = True
        update_stat(self.id, self.habit_class)
        self.main_parent.update_tab()
        self.update_stylesheet_of_container()

    def update_stylesheet_of_container(self):
        if self.habit_class == "good_habits":
            style = "border: 2px " + (
                    "rgba(156, 158, 155, 0.7);"
                    if not self.ended else "rgba(63, 143, 61, 0.9);") + "" \
                "border-style: solid;" \
                "border-radius: 5px; padding: 5px;" \
                "background: " + (
                    "rgba(156, 158, 155, 0.56);"
                    if not self.ended else "rgba(63, 143, 61, 0.72)")
        else:
            style = "border: 2px " + (
                    "rgba(156, 158, 155, 0.5);"
                    if not self.ended else "rgba(187, 58, 58, 0.7);") + "" \
                "border-style: solid;" \
                "border-radius: 5px; padding: 5px;" \
                "background: " + (
                    "rgba(156, 158, 155, 0.56);"
                    if not self.ended else "rgba(187, 58, 58, 0.25)")

        self.parent.setStyleSheet(
            str(style)
        )
        self.parent.setFixedHeight(60)


class CircularProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None, radius=50, value=50,
                 color=QtGui.QColor("#3f8f3d")):
        super().__init__(parent)
        self.setObjectName("stat_circular_progress_bar")
        self.value = 0
        self.minimum = 0
        self.maximum = 100
        self.setFixedSize(radius * 2, radius * 2)
        self.setValue(value)
        self.color = color

    def setValue(self, value):
        self.value = max(self.minimum, min(value, self.maximum))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        size = min(self.width(), self.height())
        pen_width = 10
        margin = pen_width / 2 + 1
        rect = QtCore.QRectF(0, 0, size - 2 * margin, size - 2 * margin)
        rect.moveCenter(QtCore.QPointF(self.rect().center()))

        bg_pen = QtGui.QPen(QtGui.QColor(200, 200, 200), pen_width)
        painter.setPen(bg_pen)
        painter.drawArc(rect, 90 * 16, -360 * 16)

        progress_angle = int((self.value - self.minimum) /
                             (self.maximum - self.minimum) * 360 * 16)
        prog_pen = QtGui.QPen(self.color, pen_width)
        prog_pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(prog_pen)
        painter.drawArc(rect, 90 * 16, -progress_angle)

        painter.setPen(self.palette().color(
            QtGui.QPalette.ColorRole.WindowText))
        font = painter.font()
        font.setPointSize(max(8, int(size / 8)))
        painter.setFont(font)
        painter.drawText(rect, QtCore.Qt.AlignCenter, f"{self.value}%")
