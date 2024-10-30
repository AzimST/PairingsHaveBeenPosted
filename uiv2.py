import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QHBoxLayout,
    QVBoxLayout, QLineEdit, QWidget, QLabel, QScrollArea,
    QFrame, QGridLayout
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, Signal

from Player import Player
from main import run_tournament, gets_pairs, print_pairings

class CustomButton(QPushButton):
    widget_added = Signal(QWidget)

    def __init__(self):
        super().__init__("Add Widget")
        self.clicked.connect(self.add_widget)

    def add_widget(self):
        player_section = self.parent().parent().parent().players_section
        name = player_section.name_input.text()

        if name:
            if self._is_name_unique(name):
                widget = CustomPlayerWidget(name)
                self.widget_added.emit(widget)
                self._save_name(name)
            else:
                player_section.set_info("Bu isim zaten var, lütfen başka bir isim giriniz", "red")
            player_section.name_input.clear()
        else:
            player_section.set_info("Lütfen isim giriniz", "red")

    def _is_name_unique(self, name):
        with open(f"{os.getcwd()}/deneme.txt", "r") as f:
            return name not in [line.strip() for line in f.readlines()]

    def _save_name(self, name):
        with open(f"{os.getcwd()}/deneme.txt", "a") as f:
            f.write(f"{name}\n")


class CustomScroll(QScrollArea):
    def __init__(self, fixed_height=500):
        super().__init__()
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self._load_existing_widgets()
        self._configure_scroll_area(fixed_height)

    def _load_existing_widgets(self):
        with open(f"{os.getcwd()}/deneme.txt", "r") as f:
            for line in f.readlines():
                self.add_widget(CustomPlayerWidget(line.strip()))

    def _configure_scroll_area(self, fixed_height):
        self.setFixedHeight(fixed_height)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)

    def add_widget(self, widget):
        if isinstance(widget, QWidget):
            self.main_layout.addWidget(widget)


class CustomPlayerWidget(QWidget):
    clicked = Signal()

    def __init__(self, player_name="null", control=1):
        super().__init__()
        self.player = Player(player_name)
        self.control = control
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.file_name = QLabel(self.player.name, alignment=Qt.AlignCenter)
        layout.addWidget(self.file_name)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.setStyleSheet("background-color: green" if selected else "background-color: red")


class PlayersSectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.name_input = QLineEdit(placeholderText="Lütfen İsminizi Buraya Giriniz.")
        self.info_label = QLabel("Lütfen isminizi giriniz ve kaydet butonuna basınız", wordWrap=True)
        self.player_list_area = CustomScroll()
        self.save_button = CustomButton()
        self.start_button = StartButton()

        self.save_button.widget_added.connect(self.player_list_area.add_widget)

        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.player_list_area)
        layout.addWidget(self.start_button)

    def set_info(self, message, color):
        self.info_label.setText(message)
        self.info_label.setStyleSheet(f"color: {color}")

    def get_player_list(self):
        return [line.strip() for line in open(f"{os.getcwd()}/deneme.txt").readlines()]


class StartButton(QPushButton):
    def __init__(self):
        super().__init__("Start")
        self.clicked.connect(self.start_tournament)

    def start_tournament(self):
        player_list = self.parent().get_player_list()
        if len(player_list) < 4:
            self.parent().set_info("En az 4 oyuncu olmalıdır", "red")
            return

        self.parent().set_info("Turnuva başladı", "green")
        pairs = gets_pairs(player_list, 1)
        self.parent().parent().info_table.update_table(pairs)
        print_pairings(pairs)


class TournemantInfoTable(QWidget):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea(self)
        self.inner_widget = QWidget()
        self.layout_main = QVBoxLayout(self)
        self.tournament_pairing_layout = QGridLayout()

        self._setup_ui()

    def _setup_ui(self):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.inner_widget)
        self.inner_widget.setLayout(self.tournament_pairing_layout)
        self.layout_main.addWidget(self.scroll_area)

    def update_table(self, pairs):
        for i in reversed(range(self.tournament_pairing_layout.count())):
            widget = self.tournament_pairing_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for index, table in enumerate(pairs):
            row, col = divmod(index, 3)
            self.tournament_pairing_layout.addWidget(TournementTable(table, index + 1), row, col)


class TournementTable(QWidget):
    def __init__(self, table_info, table_number):
        super().__init__()
        self._setup_ui(table_info, table_number)

    def _setup_ui(self, table_info, table_number):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Table {table_number}", alignment=Qt.AlignCenter))
        self.player1 = CustomPlayerWidget(table_info[0], control=2)
        self.player2 = CustomPlayerWidget(table_info[1], control=2)
        self.player1.clicked.connect(lambda: self._update_selection(self.player1))
        self.player2.clicked.connect(lambda: self._update_selection(self.player2))
        layout.addWidget(self.player1)
        layout.addWidget(self.player2)
        frame = QFrame(self)
        frame.setLayout(layout)
        frame.setStyleSheet("QFrame { border: 1px solid gray; border-radius: 2px; }")
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def _update_selection(self, selected_player):
        self.player1.set_selected(selected_player == self.player1)
        self.player2.set_selected(selected_player == self.player2)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yugioh Turnuva Ui Tasarim")
        self.setGeometry(100, 100, 1200, 800)
        self.players_section = PlayersSectionWidget()
        self.info_table = TournemantInfoTable()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.players_section)
        main_layout.addWidget(self.info_table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
