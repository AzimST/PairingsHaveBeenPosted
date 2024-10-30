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

from main import run_tournament,gets_pairs,print_pairings

class CustomButton(QPushButton):
    widgetadded = Signal(QWidget)

    def __init__(self):
        super().__init__()

        self.setText("Add Widget")
        self.clicked.connect(self.add_widget)

    def add_widget(self):
        # print(self.parent().parent())
        
        playerSection = self.parent().parent().parent().playersSection
        name = playerSection.nameInput.text()

        if name:
            # print(name)
            if self._is_name_unique(name):
                widget = CustomPlayerWidget(name)
                self.widgetadded.emit(widget)
                self._save_name(name)
            else:
                playerSection.info_label.setText("Bu isim zaten var lutfen baska bir isim gir")
                playerSection.info_label.setStyleSheet("background-color: red")
            # with open(f"{os.getcwd()}/deneme.txt","r+") as f:
            #     lines=f.readlines()
            #     print(lines,"lines")
            #     for line in lines:
            #         print(line,name)
            #         if line.rstrip() == name:
            #             playerSection.info_label.setText("Bu isim zaten var lutfen baska bir isim gir")
            #             playerSection.info_label.setStyleSheet("background-color: red")
            #             break
            #         else:
            #             widget = CustomPlayerWidget(name)
            #             self.widgetadded.emit(widget)
            #             f.write(name+"\n")
            #             break
                    
            playerSection.nameInput.clear()

        else:
            playerSection.info_label.setText("Lutfen isim gir " + "ISIM GIR PEZEVENG")
            playerSection.info_label.setStyleSheet("background-color: red")

    def _is_name_unique(self, name:str):
        with open(f"{os.getcwd()}/deneme.txt", "r") as f:
            return name.rstrip() not in [line.strip() for line in f.readlines()]

    def _save_name(self, name):
        with open(f"{os.getcwd()}/deneme.txt", "a") as f:
            f.write(f"{name}\n")


class CustomScroll(QScrollArea):
    def __init__(self,folder_path="null",fixedHeight=500):
        super().__init__()

        self.main_widget = QWidget()
        self.main_list = QVBoxLayout()
        self._load_existing_widgets()
        self._configure_scroll_area(fixedHeight)


    def _load_existing_widgets(self):
        with open(f"{os.getcwd()}/deneme.txt","r") as f:
            for line in f.readlines():
                self.add_widget(CustomPlayerWidget(line.rstrip()))

    def _configure_scroll_area(self,fixedHeight):
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
    clicked = Signal()

    def __init__(self,player_name="null",control = 1):
        super().__init__()
        self.control = control
        if isinstance(player_name,str):
            self.player = Player(player_name)
        elif isinstance(player_name,Player):
            self.player = player_name

        layoutVertical = QVBoxLayout()

        self.file_name = QLabel(f"{self.player.name}", alignment=Qt.AlignCenter)
        layoutVertical.addWidget(self.file_name)
        # self.frame = QFrame(self)
        # self.frame.setLayout(layoutVertical)
        # QFrame kullanarak bir kutu oluştur
        
        
        self.setLayout(layoutVertical)


    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
    
    def set_selected(self,selected):
        if selected:
            self.setStyleSheet("background-color: green")
        else:
            self.setStyleSheet("background-color: red")

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton and self.control ==1 :
    #         # Tıklama olduğunda Player özelliklerini yazdır.
    #         # Burada `player` özelliklerini gösteriyoruz.
    #         print(f"Player Name: {self.player.name}")
    #         print(f"Player Other Feature: {self.player}")  # Varsayım: 'Player' sınıfında özellik var.
    #         # Örneğin, bir QLabel güncellemesi ile ekrana da yazdırabilirsiniz.
    #         self.show_player_details()

    #     if event.button() == Qt.LeftButton and self.control ==2 :
    #         # Tıklama olduğunda Player özelliklerini yazdır.
    #         # Burada `player` özelliklerini gösteriyoruz.
    #         print(f"Player Name: {self.player.name}")
    #         print(f"Player Other Feature: {self.player}")  # Varsayım: 'Player' sınıfında özellik var.
    #         # Örneğin, bir QLabel güncellemesi ile ekrana da yazdırabilirsiniz.
    #         # self.show_player_details()

    def show_player_details(self):
        # Player özelliklerini ekrana yazdırmak için bir QLabel kullanılabilir.
        details = f"Player Name: {self.player.name}\n Player Feature: {self.player}"
        # Ekrandaki uygun label'ı güncelleyebilir veya yeni bir pencere açabilirsiniz.
        self.parent().parent().parent().parent().info_label.setText(details)    




# Yeni MainWidget sınıfı
class PlayersSectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nameInput = QLineEdit(placeholderText="Lütfen İsminizi Buraya Giriniz.")
        self.info_label = QLabel("Lütfen isminizi giriniz ve kaydet butonuna basınız",wordWrap=True,alignment=Qt.AlignCenter)
        self.playerListArea = CustomScroll()
        self.startButton = StartButton()
        self.save_button = CustomButton()

        self.save_button.widgetadded.connect(self.playerListArea.add_widget)

        self._setup_layout()

        self.setLayout(self.vertical_layout)

    def _setup_layout(self):
        self.vertical_layout = QVBoxLayout()
        
        self.vertical_layout.addWidget(self.playerListArea)
        self.vertical_layout.addWidget(self.info_label)
        self.vertical_layout.addWidget(self.nameInput)
        self.vertical_layout.addWidget(self.save_button)
        self.vertical_layout.addWidget(self.startButton)

        self.vertical_layout.setSpacing(5)

    def get_player_list(self):
        return [line.strip() for line in open(f"{os.getcwd()}/deneme.txt").readlines()]

    
    def get_scroll_area_widgets(self):
        # Ana widget'ı scrollArea'dan al
        content_widget = self.playerListArea.widget()  # QScrollArea içindeki ana widget

        # Alt elemanlara erişim
        if content_widget is not None:
            player_list = []
            # print(content_widget.findChildren(CustomPlayerWidget),"dsadsa")
            for i in content_widget.findChildren(CustomPlayerWidget):
                player_list.append(i.player)
            return player_list  # QScrollArea içindeki tüm alt widget'ları döndürür
        return []


    

class StartButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setText("Start")
        self.clicked.connect(self.start_tournament)

    def start_tournament(self):
        player_list = self.parent().get_scroll_area_widgets()
        
        if len(player_list)< 4:
            self.parent().info_label.setText("En az 4 oyuncu olmalıdır")
            self.parent().info_label.setStyleSheet("background-color: red")
            return

        # print(player_list)

        self.parent().info_label.setText("Turnuva başladı")
        self.parent().info_label.setStyleSheet("background-color: none")

        pair=gets_pairs(player_list,1)        
        self.parent().parent().parent().infoTabel.updateTable(pair)
        print_pairings(pair)


class TournemantInfoTable(QWidget):
    def __init__(self):
        super().__init__()
        self.scrollArea = QScrollArea(self)
        self.inner_widget = QWidget()
        self.layout_main = QVBoxLayout(self)
        self.tournementPairing = QGridLayout()

        self.min_table_size = (150, 100)
        self.max_table_size = (250, 200)

        self._setup_ui()


    def _setup_ui(self):
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.inner_widget)
        self.layout_main.addWidget(self.scrollArea)
        self.inner_widget.setLayout(self.tournementPairing)
  
    def updateTable(self,pairs):


        # Mevcut tabloyu temizle
        for i in reversed(range(self.tournementPairing.count())): 
            widget_to_remove = self.tournementPairing.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
        
        # Gelen veriye göre tabloyu güncelle
        for index, table in enumerate(pairs):

            row, col = divmod(index, 3)
            tournement_widget = TournementTable(table_info=table,table_number=index+1)
            self.tournementPairing.addWidget(tournement_widget, row, col)

        self.adjustGridLayout()
    
    def adjustGridLayout(self):
        available_width = self.scrollArea.width()
        table_width = self.min_table_size[0]
        columns = max(1, available_width // table_width)

        for i in range(self.tournementPairing.count()):
            widget = self.tournementPairing.itemAt(i).widget()
            widget.setFixedSize(*self.max_table_size if columns > 3 else self.min_table_size)




class TournementTable(QWidget):
    def __init__(self,table_info: list = ["12deneme","deneme12"],table_number=0):
        super().__init__()
        self.isTouch = False
        self._setup_ui(table_info,table_number)


    def _setup_ui(self, table_info, table_number):
        layoutVertical = QVBoxLayout()

        self.title = QLabel(f"Table {table_number+1}")
        layoutVertical.addWidget(self.title, alignment=Qt.AlignCenter)

        self.player1 = CustomPlayerWidget(table_info[0],2)
        self.player2 = CustomPlayerWidget(table_info[1],2)

        
        self.player1.clicked.connect(lambda: self.uptade_selection(self.player1))
        self.player2.clicked.connect(lambda: self.uptade_selection(self.player2))

        layoutVertical.addWidget(self.player1)
        layoutVertical.addWidget(self.player2)

        # QFrame kullanarak bir kutu oluştur
        self.frame = QFrame(self)
        
        self.frame.setLayout(layoutVertical)

        # Ana layout'a frame ekle
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame)
        
        self._set_playerWidgets()
        
        self.setLayout(main_layout)

    def _set_playerWidgets(self):
        self.player1.setStyleSheet("""
                border: 1px solid gray;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: 2px;  /* Köşeleri yuvarlar */
            QLabel {
                border: none; /* QLabel'lara kenarlık eklenmez */
            }
        """)

        self.player2.setStyleSheet("""
                border: 1px solid gray;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: 2px;  /* Köşeleri yuvarlar */
            QLabel {
                border: none; /* QLabel'lara kenarlık eklenmez */
            }
        """)
        self.frame.setStyleSheet("""
            QFrame {
                border: 1px solid gray;  /* Tüm dış çerçeveye kenarlık ekler */
                border-radius: 2px;  /* Köşeleri yuvarlar */
                           
            }
            QLabel {
                border: none; /* QLabel'lara kenarlık eklenmez */
            }
        """)

    def uptade_selection(self,selected_player):
        self.player1.set_selected(selected_player==self.player1)
        self.player2.set_selected(selected_player==self.player2)

    def mousePressEvent(self, event: QMouseEvent):
        # self.setStyleSheet("background-color: green")
        self.setStyleSheet("""
                           
                            QFrame {
                                background-color: rgba(100, 75, 255, 100)

                            }
                            QLabel {
                                background-color: none;

                                border: none; /* QLabel'lara kenarlık eklenmez */
                            }
                           """)  # Yarı saydam yeşil

        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yugioh Turnuva Ui Tasarim")
        self.setGeometry(100, 100, 1200, 800)
        self.playersSection = PlayersSectionWidget()
        self.infoTabel = TournemantInfoTable()
    

        self.horizantal_layout_main = QHBoxLayout()

        mainWidget = QWidget()

        self.playersSection.setFixedWidth(300)

        self.horizantal_layout_main.addWidget(self.playersSection)
        self.horizantal_layout_main.addWidget(self.infoTabel)

        mainWidget.setLayout(self.horizantal_layout_main)
        self.setCentralWidget(mainWidget)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
