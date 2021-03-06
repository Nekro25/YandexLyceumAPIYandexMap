import os
import sys

import requests
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QRadioButton

SCREEN_SIZE = [600, 650]


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.ratio = 1
        self.start_long = 37.6208
        self.start_lat = 55.7539
        self.layer = 'map'
        self.check_click_for_index = False
        self.point = None
        self.initUI()

    def getImage(self):
        map_params = {
            'l': self.layer,
            'll': f'{self.start_long},{self.start_lat}',
            'spn': f'{1 * self.ratio},{1 * self.ratio}'
        }
        if self.point:
            map_params["pt"] = f"{self.point},pm2rdl"

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, map_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(300, 100, *SCREEN_SIZE)
        self.setWindowTitle('Maps API')
        self.setStyleSheet("""background-color: #CCCDEC""")

        self.image = QLabel(self)
        self.layer_map_btn = QRadioButton(self)
        self.layer_map_btn.move(30, 452)
        self.layer_map_btn.resize(100, 30)
        self.layer_map_btn.setText('Карта')
        self.layer_map_btn.setChecked(True)
        self.layer_map_btn.clicked.connect(self.set_layer)
        self.layer_map_btn.setFocusPolicy(Qt.NoFocus)

        self.layer_sat_btn = QRadioButton(self)
        self.layer_sat_btn.move(260, 452)
        self.layer_sat_btn.resize(100, 30)
        self.layer_sat_btn.setText('Спутник')
        self.layer_sat_btn.clicked.connect(self.set_layer)
        self.layer_sat_btn.setFocusPolicy(Qt.NoFocus)

        self.layer_hib_btn = QRadioButton(self)
        self.layer_hib_btn.move(470, 452)
        self.layer_hib_btn.resize(100, 30)
        self.layer_hib_btn.setText('Гибрид')
        self.layer_hib_btn.clicked.connect(self.set_layer)
        self.layer_hib_btn.setFocusPolicy(Qt.NoFocus)

        self.show_index_btn = QPushButton(self)
        self.show_index_btn.move(30, 590)
        self.show_index_btn.resize(80, 30)
        self.show_index_btn.setText('индекс on/off')
        self.show_index_btn.clicked.connect(self.check_for_index)
        self.show_index_btn.setStyleSheet("""QPushButton{
                                                        color: #021c1e;
                                                        border: 1px solid #2c7873;
                                                        border-radius: 20;
                                                    }
                                                    QPushButton:pressed{
                                                        background-color: #a6a7ad;
                                                        color: #021c1e;
                                                        border: 1px solid #2c7873;
                                                        border-radius: 20;
                                                    }""")

        self.reset_btn = QPushButton(self)
        self.reset_btn.move(490, 535)  # Изменить местоположение кнопки
        self.reset_btn.resize(100, 40)
        self.reset_btn.setText('Сброс')
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setStyleSheet("""QPushButton{
                                                color: #021c1e;
                                                border: 1px solid #2c7873;
                                                border-radius: 20;
                                            }
                                            QPushButton:pressed{
                                                background-color: #a6a7ad;
                                                color: #021c1e;
                                                border: 1px solid #2c7873;
                                                border-radius: 20;
                                            }""")

        self.search_line = QLineEdit(self)
        self.search_line.move(30, 485)
        self.search_line.resize(450, 30)
        self.search_line.setStyleSheet("""QLineEdit{
                                              border: 1px solid #2c7873;
                                          }
                                          QLineEdit:hover{
                                              border: 1px solid #545454;
                                          }""")
        self.search_line.editingFinished.connect(self.unfocus_line)

        self.output_address_line = QLineEdit(self)
        self.output_address_line.setEnabled(False)
        self.output_address_line.move(30, 540)
        self.output_address_line.resize(450, 30)
        self.output_address_line.setStyleSheet("""QLineEdit{
                                                              border: 1px solid #2c7873;
                                                          }
                                                          QLineEdit:hover{
                                                              border: 1px solid #545454;
                                                          }""")

        self.search_button = QPushButton("Искать", self)
        self.search_button.move(490, 479)
        self.search_button.resize(100, 40)
        self.search_button.clicked.connect(self.search_place)
        self.search_button.setStyleSheet("""QPushButton{
                                                color: #021c1e;
                                                border: 1px solid #2c7873;
                                                border-radius: 20;
                                            }
                                            QPushButton:pressed{
                                                background-color: #a6a7ad;
                                                color: #021c1e;
                                                border: 1px solid #2c7873;
                                                border-radius: 20;
                                            }""")

        self.getImage()
        self.show_slide()

    def show_slide(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def check_for_index(self):
        self.check_click_for_index = not self.check_click_for_index
        self.search_place()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.ratio / 1.5 > 0.001:
                self.ratio /= 1.5
        elif event.key() == Qt.Key_PageDown:
            if self.ratio * 1.5 < 90:
                self.ratio *= 1.5
        if event.key() == Qt.Key_Left:
            if 0 < self.start_long - self.ratio < 180:
                self.start_long -= self.ratio
        if event.key() == Qt.Key_Up:
            if -90 < self.start_lat + self.ratio < 90:
                self.start_lat += self.ratio
        if event.key() == Qt.Key_Right:
            if 0 < self.start_long + self.ratio < 180:
                self.start_long += self.ratio
        if event.key() == Qt.Key_Down:
            if -90 < self.start_lat - self.ratio < 90:
                self.start_lat -= self.ratio

        self.getImage()
        self.show_slide()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print(event.pos())

    def search_place(self):

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.search_line.text(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return

        json_response = response.json()

        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        toponym_coordinates = toponym["Point"]["pos"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
        toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
        try:
            toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except Exception:
            toponym_index = 'невозможно определить:('

        self.start_long, self.start_lat = float(toponym_longitude), float(toponym_lattitude)
        self.point = ",".join([toponym_longitude, toponym_lattitude])

        if self.check_click_for_index:
            self.output_address_line.setText(
                f'{toponym_address}, {toponym_index}')
        else:
            self.output_address_line.setText(toponym_address)
        self.getImage()
        self.show_slide()

    def unfocus_line(self):
        self.image.setFocus()

    def set_layer(self):
        if self.layer_map_btn.isChecked():
            self.layer = 'map'
        elif self.layer_sat_btn.isChecked():
            self.layer = 'sat'
        else:
            self.layer = 'sat,skl'

        self.getImage()
        self.show_slide()
        self.unfocus_line()

    def reset(self):
        self.ratio = 1
        self.start_long = 37.6208
        self.start_lat = 55.7539
        self.layer = 'map'
        self.point = None
        self.layer_map_btn.setChecked(True)
        self.search_line.setText('')
        self.output_address_line.setText('')
        self.getImage()
        self.show_slide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
