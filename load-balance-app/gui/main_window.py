from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLabel, QCheckBox, QSystemTrayIcon, QMenu
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction
from core.adapters import AdapterService
from core.lb_engine import LoadBalancerService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load Balance Windows")
        self.resize(600, 400)

        self.adapter_service = AdapterService()
        self.lb_service = LoadBalancerService()

        self.init_ui()
        self.init_tray()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_stats)
        self.refresh_timer.start(1000)

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)

        # Adapter table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Adapter", "MAC", "Speed", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Controls
        controls = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.refresh_adapters)
        self.btn_start = QPushButton("Start LB")
        self.btn_start.clicked.connect(self.toggle_lb)
        controls.addWidget(self.btn_refresh)
        controls.addWidget(self.btn_start)
        layout.addLayout(controls)

        self.setCentralWidget(central)
        self.refresh_adapters()

    def init_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("assets/icon.ico"))
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def refresh_adapters(self):
        adapters = self.adapter_service.list_adapters()
        self.table.setRowCount(len(adapters))
        for row, adapter in enumerate(adapters):
            self.table.setItem(row, 0, QTableWidgetItem(adapter["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(adapter["mac"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(adapter["speed"])))
            self.table.setItem(row, 3, QTableWidgetItem(adapter["status"]))

    def refresh_stats(self):
        stats = self.lb_service.get_stats()
        self.setWindowTitle(f"Load Balance Windows – {stats}")

    def toggle_lb(self):
        if self.lb_service.is_running():
            self.lb_service.stop()
            self.btn_start.setText("Start LB")
        else:
            self.lb_service.start()
            self.btn_start.setText("Stop LB")
