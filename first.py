import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QBarSeries, QBarSet, QBarCategoryAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF
import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, 
                               QGraphicsView, QGraphicsEllipseItem,
                               QGraphicsRectItem, QGraphicsTextItem,
                               QVBoxLayout, QWidget, QPushButton)
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtCore import Qt, QTimer


class ChartExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QChart Пример")
        self.setGeometry(100, 100, 1000, 700)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Создаем линейный график
        self.create_line_chart()
        layout.addWidget(self.chart_view1)
        
        # Создаем столбчатую диаграмму
        self.create_bar_chart()
        layout.addWidget(self.chart_view2)
    
    def create_line_chart(self):
        # Создаем серии данных
        series1 = QLineSeries()
        series1.setName("Синус")
        
        series2 = QLineSeries()
        series2.setName("Косинус")
        
        # Заполняем данными
        for i in range(0, 360, 10):
            x = i / 57.3  # Конвертируем в радианы
            series1.append(x, (i % 360) / 100.0)  # Простая линейная функция
            series2.append(x, 0.5 + 0.3 * (i % 180) / 180.0)  # Другая функция
        
        # Создаем график
        chart = QChart()
        chart.addSeries(series1)
        chart.addSeries(series2)
        chart.setTitle("Линейные графики")
        chart.createDefaultAxes()
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        # Создаем вид для графика
        self.chart_view1 = QChartView(chart)
        self.chart_view1.setRenderHint(QPainter.Antialiasing)
    
    def create_bar_chart(self):
        # Создаем наборы данных
        set1 = QBarSet("Продукт A", color=QColor("#3f8f3d"))
        set2 = QBarSet("Продукт B", color=QColor("#B10F0F"))
        
        # Данные
        set1 << 12 << 15 << 18 << 20 << 17
        set2 << 8 << 12 << 14 << 16 << 15
        
        # Создаем серию
        series = QBarSeries()
        series.append(set1)
        series.append(set2)
        
        # Создаем график
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Продажи по продуктам")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Создаем оси
        categories = ["Янв", "Фев", "Мар", "Апр", "Май"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        # Создаем вид для графика
        self.chart_view2 = QChartView(chart)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartExample()
    window.show()
    sys.exit(app.exec())