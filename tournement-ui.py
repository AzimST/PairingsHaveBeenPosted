import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, 
    QHBoxLayout,QVBoxLayout,QLineEdit,
    QWidget, QLabel,QScrollArea,QFrame
    ,QGridLayout
    
    
    )
import sqlite3 as sql
from PySide6.QtGui import QPixmap, QTouchEvent, QMouseEvent
from Player import Player 

from PySide6.QtCore import Qt, Signal

class CustomButton(QPushButton):
    widgetadded = Signal(QWidget)

    def __init__(self):
        super().__init__()

        self.setText("Add Widget")
        self.clicked.connect(self.add_widget)

    def add_widget(self):
        # print(self.parent().parent())
        name = self.parent().parent().playersSection.nameInput.text()

        if name:
            
            with open("deneme.txt","+a") as f:
                f.writelines(name+"\n")
            self.parent().parent().playersSection.nameInput.clear()

        else:
            self.info_label.setText("Lutfen isim gir " + "ISIM GIR PEZEVENG")

        widget = CustomPlayerWidget(name)
        self.widgetadded.emit(widget)

        # scroll_area.main_widget.layout().addWidget(widget)
        # scroll_area.main_list.addWidget


class CustomScroll(QScrollArea):
    def __init__(self,folder_path="null"):
        super().__init__()

        self.main_widget = QWidget()
        self.main_list = QVBoxLayout()

        with open("deneme.txt") as f:
            for line in f.readlines():
                self.add_widget(CustomPlayerWidget(line.rstrip()))


        # self.setFixedWidth(250)
        self.setFixedHeight(300)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.main_widget.setLayout(self.main_list)
        self.setWidget(self.main_widget)
        
    def add_widget(self, custom_widget):

        if isinstance(custom_widget, QWidget):  # Ensure it is a QWidget
            self.main_list.addWidget(custom_widget)
        if isinstance(custom_widget, str):

            self.main_list.addWidget(CustomPlayerWidget(custom_widget))

class CustomPlayerWidget(QWidget):
    def __init__(self,player_name="null"):
        super().__init__()

        self.player = Player(player_name)

        layoutVertical = QVBoxLayout()
        layoutHorizontal = QHBoxLayout()

        self.file_name = QLabel(f"{self.player.name}")
        self.file_name.setAlignment(Qt.AlignCenter)


        layoutVertical.addWidget(self.file_name)

        # layoutVertical.setSpacing(5)

        #TODO RESIM SONRADAN EKLENECEK
        # self.image_viewer = QLabel(self)
        # pixmap = QPixmap(f"{image_path}")
        # scaled_pixmap = pixmap.scaled(125, 125, Qt.KeepAspectRatio)

        # self.image_viewer.setPixmap(scaled_pixmap)
        # # self.image_viewer.resize(360, 360)
        # self.image_viewer.setFixedSize(125, 100)

        # layoutHorizontal.addWidget(self.image_viewer)


        layoutHorizontal.addLayout(layoutVertical)


    

        # QFrame kullanarak bir kutu oluştur
        frame = QFrame(self)
        frame.setLayout(layoutHorizontal)
        frame.setStyleSheet("""
            QFrame {
                border: 1px solid black;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: None;  /* Köşeleri yuvarlar */
                           
            }
            QLabel {
                border: None; /* QLabel'lara kenarlık eklenmez */
            }
        """)

        # Ana layout'a frame ekle
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Tıklama olduğunda Player özelliklerini yazdır.
            # Burada `player` özelliklerini gösteriyoruz.
            print(f"Player Name: {self.player.name}")
            print(f"Player Other Feature: {self.player}")  # Varsayım: 'Player' sınıfında özellik var.
            # Örneğin, bir QLabel güncellemesi ile ekrana da yazdırabilirsiniz.
            self.show_player_details()

    def show_player_details(self):
        # Player özelliklerini ekrana yazdırmak için bir QLabel kullanılabilir.
        details = f"Player Name: {self.player.name}\nPlayer Feature: {self.player}"
        # Ekrandaki uygun label'ı güncelleyebilir veya yeni bir pencere açabilirsiniz.
        self.parent().parent().setText(details)    



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yugioh Turnuva Ui Tasarim")
        self.setGeometry(100, 100, 1200, 800)
        
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout_2 = QVBoxLayout()
        self.horizantal_layout_main = QHBoxLayout()

        self.button_mapping = QGridLayout()


        mainWidget = QWidget()
        widgetTournamentInfoSection = QWidget()


        widgetTournamentInfoSection


        self.playersSection = PlayersSectionWidget()
        self.playersSection.setFixedWidth(350)

        self.setCentralWidget(self.playersSection)


    def save_name(self):
        pass



# Yeni MainWidget sınıfı
class PlayersSectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.vertical_layout = QVBoxLayout()
        self.button_mapping = QGridLayout()

        self.scrollArea = CustomScroll()

        self.vertical_layout.addWidget(self.scrollArea)

        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText("Lütfen İsminizi Buraya Giriniz.")

        self.info_label = QLabel("Lütfen isminizi giriniz ve kaydet butonuna basınız")
        self.info_label.setWordWrap(True)

        self.save_button = CustomButton()
        self.save_button.widgetadded.connect(self.scrollArea.add_widget)

        self.vertical_layout.addWidget(self.info_label)
        self.vertical_layout.addWidget(self.nameInput)
        self.vertical_layout.addWidget(self.save_button)
        self.vertical_layout.setSpacing(5)

        # Grid'e butonları ekleyelim
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")
        button4 = QPushButton("Button 4")

        self.startButton = QPushButton("Start")

        self.button_mapping.addWidget(button1, 0, 0)
        self.button_mapping.addWidget(button2, 0, 1)
        self.button_mapping.addWidget(button3, 1, 0)
        self.button_mapping.addWidget(button4, 1, 1)

        self.button_mapping.setContentsMargins(5, 25, 5, 25)
        self.vertical_layout.addLayout(self.button_mapping)
        self.vertical_layout.addWidget(self.startButton)

        self.setLayout(self.vertical_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
