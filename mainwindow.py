import sys
from PySide6.QtCharts import (QChart, QChartView, QBarSeries,
                              QBarSet, QBarCategoryAxis)
from PySide6 import QtCore, QtWidgets, QtGui

from classes import CircularProgressBar, HabitsHorizontalLayout
from functions import (load_day_stat, load_global_stat, load_stat_percents,
                       load_ui, load_habits,
                       update_global_stat)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трекер привычек")
        self.ui = load_ui("ui/main.ui", self)

        self.tab_widget = self.ui.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.tab_widget.currentChanged.connect(self.update_tab)
        self.tab_stat_widget = self.ui.findChild(QtWidgets.QTabWidget,
                                                 "statistics_tabWidget")
        self.tab_stat_widget.currentChanged.connect(self.update_tab)
        self.year_tab = self.ui.findChild(QtWidgets.QWidget, "year_tab")
        year_layout = QtWidgets.QVBoxLayout(self.year_tab)
        self.circular_progress = CircularProgressBar()
        self.circular_progress.setValue(75)
        year_layout.addWidget(self.circular_progress)
        self.month_tab = self.ui.findChild(QtWidgets.QWidget, "month_tab")
        QtWidgets.QVBoxLayout(self.month_tab)

        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumWidth(1000)
        self.notify = self.ui.findChild(QtWidgets.QPushButton, "pushButton")
        self.notify.clicked.connect(self.show_system_notification)
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.create_tray_icon()
        self.update_tab()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            w = item.widget()
            sub = item.layout()
            if w:
                w.deleteLater()
            elif sub:
                self.clear_layout(sub)
                try:
                    sub.deleteLater()
                except Exception:
                    pass
            else:
                pass

    def generate_chart(self, current_tab: QtWidgets.QWidget):
        time = current_tab.objectName().replace("_tab", "")
        data = load_global_stat(time=time)
        if time != "day":
            self.clear_layout(current_tab.layout())
            good_habits = QBarSet("хорошие привычки", color=QtGui.QColor("#3f8f3d"))
            bad_habits = QBarSet("плохие привычки", color=QtGui.QColor("#B10F0F"))
            for i in range(len(data[0])):
                good_habits << data[0][i]
                bad_habits << data[1][i]
            series = QBarSeries()
            series.append(good_habits)
            series.append(bad_habits)
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Статистика по выполненным целям")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            categories = data[2]
            axis = QBarCategoryAxis()
            axis.append(categories)
            chart.createDefaultAxes()
            chart.setAxisX(axis, series)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(QtCore.Qt.AlignBottom)
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
            current_tab.layout().addWidget(chart_view)
        else:
            current_tab.setLayout(QtWidgets.QHBoxLayout())
            self.clear_layout(current_tab.layout())
            circ_prog_bar_good = CircularProgressBar(current_tab, 200, data[0],
                                                     QtGui.QColor("#3f8f3d"))
            circ_prog_bar_bad = CircularProgressBar(current_tab, 200, data[1],
                                                    QtGui.QColor("#b33a3a"))
            current_tab.layout().addWidget(circ_prog_bar_good)
            current_tab.layout().addWidget(circ_prog_bar_bad)
    def generate_dnevnik_tab(self, current_tab):
        scroll_area = current_tab.findChild(QtWidgets.QScrollArea,
                                            "dnevnik_list_scrollarea")
        if scroll_area is None:
            container = current_tab.findChild(QtWidgets.QWidget,
                                              "list_entry")
            container_layout = container.layout()
            if container_layout is None:
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setObjectName("list_entry_layout")
                container_layout.setSpacing(20)
            container_layout.setAlignment(QtCore.Qt.AlignTop)
            scroll_area = QtWidgets.QScrollArea(current_tab)
            scroll_area.setObjectName("habits_list_scrollarea")
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
            scroll_area.setWidget(container)
            if current_tab.layout() is None:
                current_tab.setLayout(QtWidgets.QVBoxLayout())
            current_tab.layout().addWidget(scroll_area)
        else:
            container = scroll_area.widget()
            container.setMinimumWidth(400)
            container_layout = container.layout()
            if container_layout is None:
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setObjectName("list_entry_layout")
                container_layout.setSpacing(20)

    def generate_habit_tab(self, current_tab, type_habit="good_habits"):
        self.add_good_habit_button = QtWidgets.QPushButton(
                "Добавить привычку")
        self.add_good_habit_button.setObjectName("add_habit_button")
        self.add_good_habit_button.clicked.connect(
            lambda: self.open_adding_habit_dialog(type_habit))
        self.add_good_habit_button.setFixedHeight(40)
        dict_habits = load_habits(type_habit)

        scroll_area = current_tab.findChild(QtWidgets.QScrollArea,
                                            "habits_list_scrollarea")
        if scroll_area is None:
            container = current_tab.findChild(QtWidgets.QWidget,
                                              "habits_list_container")
            if container is None:
                container = QtWidgets.QWidget()
                container.setObjectName("habits_list_container")
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setObjectName("habits_list")
                container_layout.setSpacing(20)
            else:
                container_layout = container.layout()
                if container_layout is None:
                    container_layout = QtWidgets.QVBoxLayout(container)
                    container_layout.setObjectName("habits_list")
                    container_layout.setSpacing(20)
            container_layout.setAlignment(QtCore.Qt.AlignTop)
            scroll_area = QtWidgets.QScrollArea(current_tab)
            scroll_area.setObjectName("habits_list_scrollarea")
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
            scroll_area.setWidget(container)
            if current_tab.layout() is None:
                current_tab.setLayout(QtWidgets.QVBoxLayout())
            current_tab.layout().addWidget(scroll_area)
        else:
            container = scroll_area.widget()
            container.setMinimumWidth(400)
            container_layout = container.layout()
            if container_layout is None:
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setObjectName("habits_list")
                container_layout.setSpacing(20)
        layout_habits_list = container_layout
        self.clear_layout(layout_habits_list)
        layout_habits_list.addWidget(self.add_good_habit_button)
        if type_habit == "bad_habits":
            self.add_good_habit_button.setText("Добавить вредную привычку")
            self.add_good_habit_button.setStyleSheet(
                "background-color: rgba(187, 58, 58, 0.83); border-radius: 5px;padding: 5px;")
        else:
            self.add_good_habit_button.setText("Добавить полезную привычку")
            self.add_good_habit_button.setStyleSheet(
                "background-color: #3f8f3d;border-radius: 5px; padding: 5px;")
        if len(dict_habits) == 0:
            label = QtWidgets.QLabel(
                "Привычек нет. Добавьте новую привычку.")
            layout_habits_list.addWidget(label)
        else:
            for habit in dict_habits.items():
                container = QtWidgets.QWidget()
                HabitsHorizontalLayout(
                    habit[0],
                    container,
                    name=habit[1]["name"],
                    points=habit[1]["points"],
                    habit_class=type_habit,
                    main_parent=self,
                    ended=load_day_stat(type_habit)[habit[0]]["ended"]
                    )
                layout_habits_list.addWidget(
                    container
                )

        layout_for_stat = current_tab.findChild(QtWidgets.QVBoxLayout,
                                                "for_stat_layout")
        layout_for_stat.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)
        if not current_tab.findChild(CircularProgressBar,
                                     "stat_circular_progress_bar"):
            current_tab.layout().addItem(
                QtWidgets.QSpacerItem(100,
                                      1,
                                      QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Minimum))

            current_tab.layout().addWidget(CircularProgressBar(
                current_tab,
                radius=100,
                value=load_stat_percents(type_habit),
                color=QtGui.QColor("#3f8f3d") if type_habit == "good_habits"
                else QtGui.QColor("#b33a3a")),

            )
            current_tab.layout().addItem(
                QtWidgets.QSpacerItem(100,
                                      1,
                                      QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Minimum))

        else:
            current_tab.findChild(
                CircularProgressBar,
                "stat_circular_progress_bar").setValue(
                    load_stat_percents(type_habit))

    def update_tab(self):
        current_tab = self.tab_widget.currentWidget()
        print(current_tab.objectName())
        if current_tab.objectName() == "statistics_tab":
            current_tab = self.tab_stat_widget.currentWidget()
            if current_tab.objectName() == "year_tab":
                self.generate_chart(current_tab)         
            elif current_tab.objectName() == "month_tab":
                self.generate_chart(current_tab)
            elif current_tab.objectName() == "day_tab":
                self.generate_chart(current_tab)
        elif current_tab.objectName() == "good_habits_tab":
            self.generate_habit_tab(current_tab, type_habit="good_habits")
        elif current_tab.objectName() == "bad_habits_tab":
            self.generate_habit_tab(current_tab, type_habit="bad_habits")

    def open_adding_habit_dialog(self, habit_class):
        from dialogs.adding_habit import AddingHabit
        dialog = AddingHabit(self, habit_class=habit_class)
        dialog.setGeometry(150, 150, 400, 200)
        dialog.setFixedSize(dialog.size())
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.update_tab()

    def create_tray_icon(self):
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("blue")))
        painter.drawEllipse(0, 0, 32, 32)
        painter.end()
        icon = QtGui.QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setVisible(True)

    def show_system_notification(self):
        self.tray_icon.showMessage(
            "Мое приложение",
            "Это системное уведомление!\nОно появится в области уведомлений.",
            QtWidgets.QSystemTrayIcon.Information,
            5000
        )


if __name__ == "__main__":
    update_global_stat()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
