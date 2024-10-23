import sys
import os
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
            
            with open(f"{os.getcwd()}/deneme.txt","+a") as f:
                f.writelines(name+"\n")
            self.parent().parent().playersSection.nameInput.clear()

        else:
            self.info_label.setText("Lutfen isim gir " + "ISIM GIR PEZEVENG")

        widget = CustomPlayerWidget(name)
        self.widgetadded.emit(widget)

        # scroll_area.main_widget.layout().addWidget(widget)
        # scroll_area.main_list.addWidget


class CustomScroll(QScrollArea):
    def __init__(self,folder_path="null",fixedHeight=500):
        super().__init__()

        self.main_widget = QWidget()
        self.main_list = QVBoxLayout()

        with open(f"{os.getcwd()}/deneme.txt","r") as f:
            for line in f.readlines():
                self.add_widget(CustomPlayerWidget(line.rstrip()))


        # self.setFixedWidth(250)
        self.setFixedHeight(fixedHeight)
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
    def __init__(self,player_name="null",control = 1):
        super().__init__()
        self.control = control

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
        # frame.setStyleSheet("""
        #     QFrame {
        #         border: 1px solid black;  /* Tüm dış çerçeveye kenarlık ekler */
        #         border-radius: None;  /* Köşeleri yuvarlar */
                           
        #     }
        #     QLabel {
        #         border: None; /* QLabel'lara kenarlık eklenmez */
        #     }
        # """)

        # Ana layout'a frame ekle
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.control ==1 :
            # Tıklama olduğunda Player özelliklerini yazdır.
            # Burada `player` özelliklerini gösteriyoruz.
            print(f"Player Name: {self.player.name}")
            print(f"Player Other Feature: {self.player}")  # Varsayım: 'Player' sınıfında özellik var.
            # Örneğin, bir QLabel güncellemesi ile ekrana da yazdırabilirsiniz.
            self.show_player_details()

        if event.button() == Qt.LeftButton and self.control ==2 :
            # Tıklama olduğunda Player özelliklerini yazdır.
            # Burada `player` özelliklerini gösteriyoruz.
            print(f"Player Name: {self.player.name}")
            print(f"Player Other Feature: {self.player}")  # Varsayım: 'Player' sınıfında özellik var.
            # Örneğin, bir QLabel güncellemesi ile ekrana da yazdırabilirsiniz.
            # self.show_player_details()

    def show_player_details(self):
        # Player özelliklerini ekrana yazdırmak için bir QLabel kullanılabilir.
        details = f"Player Name: {self.player.name}\n Player Feature: {self.player}"
        # Ekrandaki uygun label'ı güncelleyebilir veya yeni bir pencere açabilirsiniz.
        self.parent().parent().parent().parent().info_label.setText(details)    



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

        self.horizantal_layout_main.addWidget(self.playersSection)
        self.infoTabel = TournemantInfoTable()

        self.infoTabel.setFixedWidth(800)
        self.infoTabel.setFixedHeight(600)
        self.horizantal_layout_main.addWidget(self.infoTabel)

        mainWidget.setLayout(self.horizantal_layout_main)
        self.setCentralWidget(mainWidget)


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

        self.startButton = startButton()

        self.button_mapping.setContentsMargins(5, 25, 5, 25)
        self.vertical_layout.addLayout(self.button_mapping)
        self.vertical_layout.addWidget(self.startButton)

        self.setLayout(self.vertical_layout)

class startButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setText("Start")
        self.clicked.connect(self.start_tournament)

    def start_tournament(self):
        ## TODO: Burda apiye post ile oyuncu verileri atilacak ve id da degisiklikler olcak mesela 
        # liste uzayacak diger butonlar gitcek ve yeni bir buton gelcek


        # os.system(f"python3 PairingsHaveBeenPosted/main.py")
        # self.setDisabled(True)

        secondPhase = SecondPlayersSectionWidget()
        secondPhase.setFixedWidth(350)
        print(self.parent().parent().parent())#.setCentralWidget(secondPhase)
        

        pass


# Yeni MainWidget sınıfı
class SecondPlayersSectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.vertical_layout = QVBoxLayout()

        self.tournementStartButton = QPushButton("Start Tournement")

        self.scrollArea = CustomScroll(fixedHeight=700)

        self.vertical_layout.addWidget(self.scrollArea)
        self.vertical_layout.addWidget(self.tournementStartButton)
        self.vertical_layout.setContentsMargins(25, 15, 15, 15)


        self.setLayout(self.vertical_layout)



class TournemantInfoTable(QWidget):
    def __init__(self):
        super().__init__()
        layoutVertical = QVBoxLayout()
        self.tournementPairing = QGridLayout()
        
        layoutVertical.addLayout(self.tournementPairing)
        self.tournementPairing.addWidget(TournementTable(),0,0)

        # self.tournementPairing.addWidget(TournementTable(),7,3)
        frame = QFrame(self)
                
        frame.setLayout(layoutVertical)
        frame.setStyleSheet("""
            QFrame {
                border: 1px solid gray;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: 2px;  /* Köşeleri yuvarlar */
                           
            }
            QLabel {
                border: none; /* QLabel'lara kenarlık eklenmez */
            }
        """)


        self.setLayout(layoutVertical)
    
    def updateTable(self,pairs):
        ## TODO :   burda gelen veriye gore bir widget tasarimi olcak her zaman ayni degil eeger 15 geldiyse mesela 5x3 12 geldiyse 4x3 olcak
        # 3 rowda yapilcak 
        self.tournementPairing.addWidget(TournementTable())
        pass



class TournementTable(QWidget):
    def __init__(self,table_info: list = ["12deneme","deneme12"]):
        super().__init__()
        self.isTouch = False

        layoutVertical = QVBoxLayout()

        self.player1 = CustomPlayerWidget(table_info[0],2)
        self.player2 = CustomPlayerWidget(table_info[1],2)

        layoutVertical.addWidget(self.player1)
        layoutVertical.addWidget(self.player2)

        # layoutVertical.setSpacing(15)

        # QFrame kullanarak bir kutu oluştur
        frame = QFrame(self)
        
        frame.setLayout(layoutVertical)
        frame.setStyleSheet("""
            QFrame {
                border: 1px solid gray;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: 2px;  /* Köşeleri yuvarlar */
                           
            }
            QLabel {
                border: none; /* QLabel'lara kenarlık eklenmez */
            }
        """)

        # Ana layout'a frame ekle
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setFixedWidth(200)
        self.setFixedHeight(150)
        self.setLayout(main_layout)

        # self.setLayout(layoutHorizontal)
    def mousePressEvent(self, event: QMouseEvent):

        if self.isTouch == False:
            self.isTouch = True
            self.setStyleSheet("background-color: red")
        
        elif self.isTouch == True:
            self.isTouch = False
            self.setStyleSheet("background-color: white")

        super().mousePressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
