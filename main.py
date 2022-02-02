import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.ratio = 1

        self.initUI()

    def getImage(self):
        map_params = {
            'l': 'map',
            'll': '37.6208,55.7539',
            'spn': f'{1 * self.ratio},{1 * self.ratio}'
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, map_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Угадай-ка город')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

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

        self.getImage()
        self.show_slide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
