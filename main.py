import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.ratio = 1
        self.start_long = 37.6208
        self.start_lat = 55.7539

        self.initUI()

    def getImage(self, point=None):
        map_params = {
            'l': 'map',
            'll': f'{self.start_long},{self.start_lat}',
            'spn': f'{1 * self.ratio},{1 * self.ratio}'
        }
        if point:
            map_params["pt"] = f"{point},pm2rdl"

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

        self.search_line = QLineEdit(self)
        self.search_line.move(30, 485)
        self.search_line.resize(450, 30)
        self.search_line.setStyleSheet("""QLineEdit{
                                              border: 1px solid #2c7873;
                                          }
                                          QLineEdit:hover{
                                              border: 1px solid #545454;
                                          }""")

        self.search_button = QPushButton("Искать", self)
        self.search_button.move(500, 479)
        self.search_button.resize(80, 40)
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

    def search_place(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.search_line.text(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()

        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        toponym_coordinates = toponym["Point"]["pos"]

        toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")

        self.start_long, self.start_lat = toponym_longitude, toponym_lattitude

        self.getImage(point=",".join([toponym_longitude, toponym_lattitude]))
        self.show_slide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
